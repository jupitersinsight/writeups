# Level 2

## Software used
- Google Chrome + FoxyProxy
- BurpSuite Community

## Hint

<img src="https://user-images.githubusercontent.com/110602224/234995748-cbf88104-ed73-4ac5-8898-8990f6d1f4a3.png" width=600 heigth=auto>

## Solution w/ BurpSuite

Passive capture through BurpSuite Proxy.  
Response to **GET /** does not contain any password as written in the hint message but...  

<img src="https://user-images.githubusercontent.com/110602224/234996389-ef4cb2fd-b9a2-475f-9c8e-4cc6fbc6330d.png" width=350 height=auto>

we can see that there is an image tag which loads a .png file from another directory, **files**.

Using the embedded tool _Repeater_ in BurpSuite we can alter the GET request to **/** and send a new request for **/files**.  
<img src="https://user-images.githubusercontent.com/110602224/234997373-0f7d6333-5360-419a-a53f-0c447b98887a.png" width=900 height=auto>

Since the server responded with a 301 status code we need to follow the redirection which results in a directory with two files: **files.png** and **users.txt**.  
<img src="https://user-images.githubusercontent.com/110602224/234998123-203d22c0-6fbd-457c-b523-665ec0cc5f69.png" width=900 height=auto>

The file **users.txt** might be of interest.  
<img src="https://user-images.githubusercontent.com/110602224/234998708-3be128b7-e4e3-4aa0-8951-e41dc47cca5b.png" width=900 height=auto>

As guessed, the file does contain interesting information like the password for the next level: **G6ctbMJ5Nb4cbFwhpMPSvxGHhQ7I6W8Q**

## Solution w/o BurpSuite

Inspecting the source code of the page reveals the existence of a directory named **files** from which a file .png is loaded.  

<img src="https://user-images.githubusercontent.com/110602224/234999405-9d012068-7f6f-49c8-95f2-842796834abe.png" width=300 height=auto>

Browsing to **/files** we find a short list of available resources, one of particular interest: **users.txt**  

<img src="https://user-images.githubusercontent.com/110602224/234999933-2c648e9b-e0a1-45bf-9e5b-a842ce10fe25.png" width=350 height=auto>

The file **users.txt** contains the password for the next level.  

<img src="https://user-images.githubusercontent.com/110602224/235000294-09d54da5-7bf2-405e-96d0-f7b5c55a0c15.png" width=350 height=auto>
