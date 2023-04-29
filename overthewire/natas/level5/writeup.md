# Level 5

## Software used
- Google Chrome + FoxyProxy
- Burpsuite Community

## Hint

<img src="https://user-images.githubusercontent.com/110602224/235320302-5b1477c2-ba56-41cc-bb3f-2c9ec8623503.png" width=600 height=auto>

## Solution

Inspecting the GET request for the root page (**GET /**) we can see that the web application uses a **Set-Cookie** header to set a cookie to determine which users are logged-in and which users are not logged-in: **Set-Cookie: loggedin=0**.    

<img src="https://user-images.githubusercontent.com/110602224/235320470-88ef9c2a-fedd-4e1b-ba1b-2af960874a42.png" width=900 height=auto>

Using the module **Repeater** and changing the value of the cookie from **0** to **1**, the web application returns the password for the next level.

<img src="https://user-images.githubusercontent.com/110602224/235320554-d39eeb60-e779-42e9-9c79-f280baad7d00.png" width=900 height=auto>

The password for the next level is: **fOIvE0MDtPTgRhqmmvvAOt2EfXR6uQgR**
