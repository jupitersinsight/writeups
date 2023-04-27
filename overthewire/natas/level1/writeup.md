# Level 1

## Software used
- Google Chrome + FoxyProxy
- BurpSuite Community

## Hint

<img src="https://user-images.githubusercontent.com/110602224/234991688-638beb13-fc64-4b2c-8ab1-15e603519913.png" width=600 height=auto>

## Solution (w BurpSuite)

Passive capture through BurpSuite Proxy reveals the password to be hidden in a HTML comment which is **h4ubbcXrWqsTo7GGnnUMLppXbOogfBZ7**.

Response to request **GET /**  

<img src="https://user-images.githubusercontent.com/110602224/234992588-870e8986-9ec5-44c7-8d2f-681450c85dec.png" width=600 height=auto>

## Solution (w/ BurpSuite)

Any action associated with a right-click action triggers a listening event that make a pop up to appear.

<img src="https://user-images.githubusercontent.com/110602224/234993648-52710cf2-4be1-4b4b-a37d-c1f39fa20272.png" width=600 height=auto>

Opening Google Chrome's Developer Tools via F12 key, it is possible to inspect the web page properties and there lies the password.  

<img src="https://user-images.githubusercontent.com/110602224/234994345-b325624d-d07f-4386-858f-5cfd752373ac.png" width=600 heigth=auto>

     



