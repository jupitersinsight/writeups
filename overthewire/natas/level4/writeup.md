# Level 4

## Software used
- Google Chrome + FoxyProxy
- Burpsuite Community

## Hint
<img src="https://user-images.githubusercontent.com/110602224/235319385-036f9b18-f556-4e78-9ea5-f7765636c6b2.png" width=600 height=auto>

## Solution

The hint is pretty clear, the web server shows the password for the next level only to requests coming from _http://natas5.natas.labs.overthewire.org_.  
To trick the server, the **Referer** header is what we need to use. The [**Referer**](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer) header is used in web communications to inform the receiving host from where the request is coming from and can be used in access control rules (as in this lab).  

<img src="https://user-images.githubusercontent.com/110602224/235320044-52c34063-827e-4c3e-9e9a-0d0890ea83b0.png" width=900 height=auto>

The password for the next level is: **Z0NsrtIkJoKALBCLi5eqFfcRN82Au2oD**
