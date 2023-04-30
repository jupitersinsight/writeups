# Level 8

## Software used
- Google Chrome + FoxyProxy Extension
- Burpsuite Community
- Python

## Hint
_(sourcecode)_

<img src="https://user-images.githubusercontent.com/110602224/235363893-0907fbda-23ca-4096-9159-218fb7a0e78b.png" width=600 height=auto>

## Solution

Let's break down the **encodeSecret** function:
- [base64_encode](https://www.php.net/manual/en/function.base64-encode.php): encodes the given string with base64
- [strrev](https://www.php.net/manual/en/function.strrev.php): returns string, reversed
- [bin2hex](https://www.php.net/manual/en/function.bin2hex.php): returns an ASCII string containing the hexadecimal representation of string. The conversion is done byte-wise with the [high-nibble](https://en.wikipedia.org/wiki/Nibble) first.

Decode using Burpsuite (manual string reverse):
- Decode as **ASCII hex**
- Manually reverse the base64 string
- Decode as **base4**

<img src="https://user-images.githubusercontent.com/110602224/235365200-4fa62ff0-67c2-4c5d-bd8b-212a33710764.png" width=900 height=auto>

Decode using python:

```python
# IMPORT BASE64 MODULE
import base64

# HEX DECODE THE HEX ENCODED STRING
hex_decoded_string = bytes.fromhex('3d3d516343746d4d6d6c315669563362').decode('UTF-8')

# REVERSE THE BASE64 ENCODED STRING
rev_string = hex_decoded_string[::-1]

# BASE64 DECODE THE BASE64 ENCODED STRING
b64decoded_string = base64.b64decode(rev_string).decode('ascii')
print(b64decoded_string)
```

Submit the secret **oubWYf2kBq** and retrieve the password for the next level, which is: **Sda6t0vkOPkM8YeOZkAGVhFoaplvlJFd**
<img src="https://user-images.githubusercontent.com/110602224/235365517-baa76380-564c-4e6e-b896-f969c453f349.png" width=600 height=auto>




