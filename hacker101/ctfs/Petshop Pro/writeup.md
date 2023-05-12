# Petshop Pro

**Difficulty**: Easy  
**Skills**: Web  
**Number of Flags**: 3
_____

Quick notes while testing:

- link pages uses RESTful syntax
- /login => 200 OK
    - username
    - password
    - invalid username/password: invalid username ... username enumeration?

_____

### Flag 0

Capturing requests in Burp Proxy shows that products are returned in an array style:  

```
[[0, {&#34;name&#34;: &#34;Kitten&#34;, &#34;desc&#34;: &#34;8\&#34;x10\&#34; color glossy photograph of a kitten.&#34;, &#34;logo&#34;: &#34;kitten.jpg&#34;, &#34;price&#34;: 8.95}]]
```

The first value is the **id** used to add prodcuts in the request GET **/add/{id}**. What follows is an array/dictionary which contains key/value pairs.

When checking out, a POST request is sent to **/checkout** with parameter **cart** in the message body.  
This parameter carries the array(s) of all items in the cart.  

Using Burp Repeater it is possible to tamper the data. In order to retireve the flag all prices must be set to 0.

_Values in **cart** parameter must be urlencoded_
<img src="" width=900 height=auto>