#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<arpa/inet.h>
#include<sys/socket.h>
#include<string.h>
#include<fcntl.h>
#include<sys/stat.h>
#include<dirent.h>
#include<pthread.h>

#define MAX_CLIENTS 1024
#define ROOT_DIR "./webroot"

typedef struct {
    char ip[INET_ADDRSTRLEN];
    char host[255];
    char user_agent[1024];
    int count;
} ClientAccess;

ClientAccess clients[MAX_CLIENTS];
int client_count = 0;
pthread_mutex_t client_mutex = PTHREAD_MUTEX_INITIALIZER; // Mutex for thread safety

char* get_header_field(char* request, char* field_name);
void record_client_access(char *ip, char *host, char *user_agent);
void serve_file(int sock, char *filepath);

void error_handling(char *message) {
    fputs(message, stderr);
    fputc('\n', stderr);
    exit(1);
}

void* handle_client(void* arg) {
    int clnt_sock = *((int*) arg);
    free(arg);

    char request[2048];
    read(clnt_sock, request, sizeof(request) - 1); // Ensure null-termination

    char* host = get_header_field(request, "Host");
    char* user_agent = get_header_field(request, "User-Agent");

    char clnt_ip[INET_ADDRSTRLEN];
    struct sockaddr_in clnt_addr;
    socklen_t clnt_addr_size = sizeof(clnt_addr);
    getpeername(clnt_sock, (struct sockaddr*)&clnt_addr, &clnt_addr_size);
    inet_ntop(AF_INET, &(clnt_addr.sin_addr), clnt_ip, INET_ADDRSTRLEN);

    record_client_access(clnt_ip, host ? host : "Unknown", user_agent ? user_agent : "Unknown");

    // Use mutex to safely read client_count and client data
    pthread_mutex_lock(&client_mutex);
    printf("Client IP: %s, Host: %s, Browser: %s (Total Accesses: %d)\n", clnt_ip, host, user_agent, clients[client_count - 1].count);
    pthread_mutex_unlock(&client_mutex);

    char *method = strtok(request, " ");
    char *filepath = strtok(NULL, " ");

    if (method && filepath && strcmp(method, "GET") == 0) {
        serve_file(clnt_sock, filepath);
    } else {
        char response[] = "HTTP/1.1 400 BAD REQUEST\r\n"
                          "Content-Type: text/html\r\n"
                          "Connection: close\r\n"
                          "Content-Length: 11\r\n\r\n"
                          "Bad Request";
        write(clnt_sock, response, sizeof(response) - 1); // No need for strlen here
    }

    free(host); // Safe to free even if NULL
    free(user_agent); // Safe to free even if NULL
    close(clnt_sock);
    return NULL;
}

void record_client_access(char *ip, char *host, char *user_agent) {
    pthread_mutex_lock(&client_mutex); // Mutex lock

    for (int i = 0; i < client_count; i++) {
        if (strcmp(clients[i].ip, ip) == 0) {
            clients[i].count++;
            pthread_mutex_unlock(&client_mutex); // Mutex unlock before return
            return;
        }
    }

    // Ensure we don't exceed the client array's size
    if (client_count < MAX_CLIENTS) {
        strncpy(clients[client_count].ip, ip, INET_ADDRSTRLEN - 1);
        strncpy(clients[client_count].host, host, sizeof(clients[client_count].host) - 1);
        strncpy(clients[client_count].user_agent, user_agent, sizeof(clients[client_count].user_agent) - 1);
        clients[client_count].count = 1;
        client_count++;
    }

    pthread_mutex_unlock(&client_mutex); // Mutex unlock
}

void serve_directory(int sock, char *dirpath) {
    char response[4096];
    char body[2048] = "<!DOCTYPE html><html><head><title>Directory Listing</title></head><body><ul>";

    DIR *dir = opendir(dirpath);
    if (!dir) {
        snprintf(response, sizeof(response),
                 "HTTP/1.1 500 INTERNAL SERVER ERROR\r\n"
                 "Content-Type: text/html\r\n"
                 "Content-Length: 21\r\n\r\n"
                 "Internal Server Error");
        write(sock, response, strlen(response));
        return;
    }

    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        // Use strncat for buffer overflow protection
        strncat(body, "<li><a href=\"", sizeof(body) - strlen(body) - 1);
        strncat(body, entry->d_name, sizeof(body) - strlen(body) - 1);
        strncat(body, "\">", sizeof(body) - strlen(body) - 1);
        strncat(body, entry->d_name, sizeof(body) - strlen(body) - 1);
        strncat(body, "</a></li>", sizeof(body) - strlen(body) - 1);
    }
    closedir(dir);

    strncat(body, "</ul></body></html>", sizeof(body) - strlen(body) - 1);
    snprintf(response, sizeof(response),
             "HTTP/1.1 200 OK\r\n"
             "Content-Type: text/html\r\n"
             "Content-Length: %lu\r\n\r\n%s", strlen(body), body);

    write(sock, response, strlen(response));
}

void serve_file(int sock, char *filepath) {
    if (strcmp(filepath, "/") == 0) {
        char index_path[512];
        snprintf(index_path, sizeof(index_path), "%s/index.html", ROOT_DIR);
        if (access(index_path, F_OK) != -1) {
            serve_file(sock, "/index.html");
            return;
        } else {
            serve_directory(sock, ROOT_DIR);
            return;
        }
    }
    char response[1024];
    char path[512];
    snprintf(path, sizeof(path), "%s%s", ROOT_DIR, filepath);

    int fd = open(path, O_RDONLY);
    if (fd == -1) {
        snprintf(response, sizeof(response),
                 "HTTP/1.1 404 NOT FOUND\r\n"
                 "Content-Type: text/html\r\n"
                 "Content-Length: 9\r\n\r\n"
                 "Not Found");
        write(sock, response, strlen(response));
        return;
    }

    struct stat st;
    stat(path, &st);
    int file_size = st.st_size;
    snprintf(response, sizeof(response),
             "HTTP/1.1 200 OK\r\n"
             "Content-Length: %d\r\n\r\n", file_size);
    write(sock, response, strlen(response));

    char buffer[1024];
    int bytes_read;
    while ((bytes_read = read(fd, buffer, sizeof(buffer))) > 0) {
        write(sock, buffer, bytes_read);
    }
    close(fd);
}

char* get_header_field(char* request, char* field_name) {
    char* start = strstr(request, field_name);
    if (!start) {
        return NULL;
    }
    start += strlen(field_name) + 2; // +2 for ": "
    char* end = strstr(start, "\r\n");
    if (!end) {
        return NULL;
    }
    int length = end - start;
    char* result = malloc(length + 1);
    strncpy(result, start, length);
    result[length] = '\0';
    return result;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage : %s <port>\n", argv[0]);
        exit(1);
    }

    printf("\033[32mServer started!\033[0m\n");
    printf("Visit: \033[4mhttp://localhost:%s\033[0m\n", argv[1]);

    int serv_sock = socket(PF_INET, SOCK_STREAM, 0);
    if (serv_sock == -1) {
        error_handling("socket() error");
    }

    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(atoi(argv[1]));

    if (bind(serv_sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) == -1) {
        error_handling("bind() error");
    }

    if (listen(serv_sock, 5) == -1) {
        error_handling("listen() error");
    }

    while (1) {
        struct sockaddr_in clnt_addr;
        socklen_t clnt_addr_size = sizeof(clnt_addr);
        int* clnt_sock_ptr = malloc(sizeof(int));
        *clnt_sock_ptr = accept(serv_sock, (struct sockaddr*)&clnt_addr, &clnt_addr_size);
        if (*clnt_sock_ptr == -1) {
            error_handling("accept() error");
        }

        pthread_t thread_id;
        pthread_create(&thread_id, NULL, handle_client, clnt_sock_ptr);
        pthread_detach(thread_id);
    }

    close(serv_sock);
    return 0;
}

