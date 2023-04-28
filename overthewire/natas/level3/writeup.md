# Level 3

## Software used
- Google Chrome + FoxyProxy
- Burpsuite Community

## Hint

<img src="https://user-images.githubusercontent.com/110602224/235248012-eca9132c-ae01-4dc5-8b70-1255203b8999.png" width=600 height=auto>

## Solution

Intercept request for http://natas3.natas.labs.overthewire.org in Burpsuite, as can be seen in the response there is nothing in the root page.

<img src="https://user-images.githubusercontent.com/110602224/235248995-9eb118fc-e414-41ed-a520-3288c46fd9c6.png" width=900 height=auto>

Send the request to the Burpsuite module **Repeater** and send a new request but this time for **/robots.txt**.

<img src="https://user-images.githubusercontent.com/110602224/235249483-f159a203-c627-455b-8ff6-ddf20cf3f958.png" width=900 height=auto>

The file robots.txt contains information about a disallowed folder that should remain hidden, **/s3cr3t/**.  
**Note** Sending a request for the hidden resource **/s3cret** returns a response with status code **301 Moved permanently**, while **/s3cr3t/** returns a response with status code **200 OK**.  

<img src="https://user-images.githubusercontent.com/110602224/235250393-6a7198a0-ff84-4c9a-b9f4-d8ed4c64bf65.png" width=900 height=auto>

In the hidden folder there is the file **users.txt** which contains the password for the next level: **tKOcJIbzM4lTs8hbCmzn5Zr4434fGZQm**.  

<img src="https://user-images.githubusercontent.com/110602224/235251031-6ae09d3d-bebe-4b69-83aa-a8d0f82edc99.png" width=900 height=auto>
