<?php

$to 		= 'demo@demo.com';
$headers	= 'FROM: "'.$email.'"';

//All form values
$name 		= 	$_POST['name'];
$email 		= 	$_POST['email'];
$msg 		= 	$_POST['msg'];
$output 	= 	"Name: ".$name.
				"\nEmail: ".$email.
				"\n\nMessage: ".$msg;

$send		= mail($to, $name, $output, $headers);