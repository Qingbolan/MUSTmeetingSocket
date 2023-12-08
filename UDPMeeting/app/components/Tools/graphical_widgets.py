
class ExternalWindows:

    def __init__(self):
        pass

    # Default ip and port for debbuging
    _IP = "127.0.0.1"
    _Port = 5000
    # Text for the drawing text part!
    _Text = "WOW"
    _Nickname = "lol"

    # This temporary variable is used to get any other things we might need from the user
    # A little bit confusing but it works
    _Temp = ""

    # A flag to check whether you press the default exit button
    _Flag = False

    
    # Return methods for the protected variables!
    @classmethod
    def return_ip(cls):
        return cls._IP

    @classmethod
    def return_port(cls):
        return cls._Port

    @classmethod
    def return_text(cls):
        return cls._Text

    @classmethod
    def return_nickname(cls):
        return cls._Nickname

    @classmethod
    def return_temp(cls):
        return cls._Temp

if __name__ == '__main__':

    ExternalWindows.getValuesFromUser()
    print(ExternalWindows.return_ip())


    ExternalWindows.get_nickname_from_user()
    print(ExternalWindows.return_nickname())
