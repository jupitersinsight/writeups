# Level 7

## Software used
- Google Chrome + FoxyProxy extension
- Burpsuite Community

## Hint

<img src="https://user-images.githubusercontent.com/110602224/235362995-196116b7-c455-4161-b459-f479da124c0e.png" width=900 height=auto>

## Solution

We are going to exploit a directory traversal vulnerability.

We need to modify the query string in the URL and request the resource **/etc/natas_webpass/natas8**

<img src="https://user-images.githubusercontent.com/110602224/235363452-aae0f773-3ab2-4dd7-9099-9beaef9d242f.png" width=900 height=auto>

<img src="https://user-images.githubusercontent.com/110602224/235363648-08e2a29a-aeaf-477a-9cfd-40462ae2ce99.png" width=900 height=auto>

The password for the next level is: **a6bZCNYwdKqN5cGP11ZdtPg0iImQQhAB**
