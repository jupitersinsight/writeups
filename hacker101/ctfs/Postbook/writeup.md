# Postbook

**Difficulty**: Easy  
**Skills**: Web  
**Number of Flags**: 7
_____

### Flag 0

Try to access as an already existing user (after you create a new user you will see posts from authors **admin** and **user**) returns the warning message:  

_You've entered a wrong username/password combination. Please do not hack our system because it is insanely illegal. We will report you to PETA if you continue. Nothing is logged, but we ask you kindly not to try anything malicious._

Since nothing is logged and there is no account lockout, we can enumerate the user password... which is **password**.  
Log-in and retrieve the flag.  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/d03097a5-a8e1-41f7-8956-244fdd3846f9" width=450 height=auto>

_____

### Flag 1

In the home page there are two posts, one identified with id **1** and the other with id **3**.  
Capture the GET request for a post and repeat it using BurpRepeater changind the id from 1 or 3 to **2** and grab the flag.  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/c6c913f7-34a2-4d01-bacd-41b413970b48" width=900 height=auto>

_____

### Flag 2

The write-post form as a hidden value which is embedded in the post request as one of the parameters to publish the post as the current user.  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/19ebded1-d37a-4808-ad4b-603b8f0f113d" width=900 heght=auto>  

Write the post and chage the user_id to **1** and send the request. The post is uploaded and published as admin.  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/cbd07afc-dc6f-4e51-8b70-bdf613a6366d" width=450 height=auto>  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/d2588964-0d84-45ac-a8b9-5f093983efd4" width=850 height=auto>  

_____

### Flag 3

Flag 3 is found on post #945

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/d00c7ee6-e731-495d-8c61-25f8cd18a573)" width=900 heigth=auto>

_____

### Flag 4

Edit another user's post to get flag #4

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/3a043a14-e681-4f4e-9f9a-0092910bcfff" widht=900 height=auto>

_____





