# Level 6

## Software used
- Google Chrome + FoxyProxy extension
- Busrpsuite Community

## Hint

<img src="https://user-images.githubusercontent.com/110602224/235361956-c4a9d767-61d8-44ee-9caa-305fc8a8d25b.png" width=600 height=auto>

## Solution

Let's inspect the source code just clicking the **View sourcecode** link.

<img src="https://user-images.githubusercontent.com/110602224/235362094-8b15b4c9-f54f-4df2-bc78-0828f24eddd6.png" width=600 height=auto>

As we can see there is a file called **secret.inc** which is included in the PHP code.
Sending a **GET** request for **/includes/secret.inc** in Burpsuite (module Repeater) returns its content which is the secret, **FOEIUWGHFEEUHOFUOIU**.

<img src="https://user-images.githubusercontent.com/110602224/235362485-c8e40664-0116-4aaf-9843-9986d491da5e.png" width=900 height=auto>

Submit the secret and retrieve the password for the next level: **jmxSiH3SP6Sonf8dv66ng8v1cIEdjXWr**

<img src="https://user-images.githubusercontent.com/110602224/235362757-d171ee61-a1cf-40a8-8b55-86b446cc7554.png" width=600 height=auto>
