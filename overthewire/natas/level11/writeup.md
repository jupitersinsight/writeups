# Level 11

## Software used
- Google Chrome + FoxyProxy
- Burspsuite Community
- [onlinephp.io](https://onlinephp.io/)

## Hint
(source code)

```php
<?

$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");

function xor_encrypt($in) {
    $key = '<censored>';
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

function loadData($def) {
    global $_COOKIE;
    $mydata = $def;
    if(array_key_exists("data", $_COOKIE)) {
    $tempdata = json_decode(xor_encrypt(base64_decode($_COOKIE["data"])), true);
    if(is_array($tempdata) && array_key_exists("showpassword", $tempdata) && array_key_exists("bgcolor", $tempdata)) {
        if (preg_match('/^#(?:[a-f\d]{6})$/i', $tempdata['bgcolor'])) {
        $mydata['showpassword'] = $tempdata['showpassword'];
        $mydata['bgcolor'] = $tempdata['bgcolor'];
        }
    }
    }
    return $mydata;
}

function saveData($d) {
    setcookie("data", base64_encode(xor_encrypt(json_encode($d))));
}

$data = loadData($defaultdata);

if(array_key_exists("bgcolor",$_REQUEST)) {
    if (preg_match('/^#(?:[a-f\d]{6})$/i', $_REQUEST['bgcolor'])) {
        $data['bgcolor'] = $_REQUEST['bgcolor'];
    }
}

saveData($data);



?>

<h1>natas11</h1>
<div id="content">
<body style="background: <?=$data['bgcolor']?>;">
Cookies are protected with XOR encryption<br/><br/>

<?
if($data["showpassword"] == "yes") {
    print "The password for natas12 is <censored><br>";
}

?>

<form>
Background color: <input name=bgcolor value="<?=$data['bgcolor']?>">
<input type=submit value="Set color">
</form>
```

## Solution

First of all, let's breakdown the code.

[PHP Arrays](https://www.php.net/manual/en/language.types.array.php): An array in PHP is actually an ordered map. A map is a type that associates values to keys. This type is optimized for several different uses; it can be treated as an array, list (vector), hash table (an implementation of a map), dictionary, collection, stack, queue, and probably more.  

**$defaultdata** is an array in which the developer hardcoded default values.

The function **xor_encrypt** encrypts input data using [XOR Encryption Algorithm](https://en.wikipedia.org/wiki/XOR_cipher).
In the first half three variables are declared:
- ```$key = '<censored>';``` : to the variable $key is assigned the key to encrypt the plaintext and decrypt the ciphertext but it is <censored>
- ```$text = $in;```: user input assigned to the variable $text
- ``` $outText = '';```: empty variable

Then there is a for loop which performs XOR encryption for each character in turn.
- ```for($i=0;$i<strlen($text);$i++)```: "counter $i" is equal to 0, while $i is less than the user input length ([strlen](https://www.php.net/manual/en/function.strlen.php)) performs action, when action is performed increment the value of $i by 1
- ```$outText .= $text[$i] ^ $key[$i % strlen($key)];```: for character at index $i of $text perform XOR ([^](https://www.geeksforgeeks.org/php-bitwise-operators/)) with character of $key at index $i
- ```return $outText;```: return XORed value


The function **loadData**
- ```global $_COOKIE;```: global variable $\_COOKIE declaration
- ```$mydata = $def;```: argument passed to the function is assigned to the variable $mydata
- ```if(array_key_exists("data", $_COOKIE))```: [array_key_exists](https://www.php.net/manual/en/function.array-key-exists.php) - if the key "data" exists in $\_COOKIE perform next actions
    - ```$tempdata = json_decode(xor_encrypt(base64_decode($_COOKIE["data"])), true);```: the value of key "data" is base64-decoded, the decoded value is passed as argument to the function **xor_encrypt**, the returned value is jeson-decoded and then assigned to the variable $tempdata
- ```if(is_array($tempdata) && array_key_exists("showpassword", $tempdata) && array_key_exists("bgcolor", $tempdata))```: if the variable %tempdata is an array, and if the keys $showpassword and $bgcolor exist in the array, perform next actions
    - ```if (preg_match('/^#(?:[a-f\d]{6})$/i', $tempdata['bgcolor']))```: [preg_match](https://www.php.net/manual/en/function.preg-match.php) - if the regular expression matches the value of key bgcolor, perform next actions
        - ```$mydata['showpassword'] = $tempdata['showpassword'];```: assign value of key showpassword in array $tempdata to key showpassword in array $mydata
        - ```$mydata['bgcolor'] = $tempdata['bgcolor'];```: assign value of key bgcolor in array $tempdata to key bgcolor in array $mydata
- ```return $mydata;```: return array $mydata


The function **saveData** creates the cookie and send it to the client:
- ```setcookie("data", base64_encode(xor_encrypt(json_encode($d))))```: [setcookie](https://www.php.net/manual/en/function.setcookie.php) - the value passed as argument to the function is json-encoded, the result is passed as argument to the function xor_encrypt, the returned value is base64-encoded and set as value of "data" in the cookie


**$data = loadData($defaultdata);**: the result of the function loadData is assigned to the variable data


```if(array_key_exists("bgcolor",$_REQUEST))```: [$\_REQUEST](https://www.php.net/manual/en/reserved.variables.request.php): if the key bgcolor exists in $\_REQUEST, perform next action  
- ```if (preg_match('/^#(?:[a-f\d]{6})$/i', $_REQUEST['bgcolor']))```: if the regular expression matches the value of key bgcolor, perorfm next action  
    - ```$data['bgcolor'] = $_REQUEST['bgcolor'];```: assign the value of key bgcolor in $\_REQUEST to the key bgcolor in array $data

**saveData($data);**: function saveData runw with argument $data(result from loadData)

In order to resolve the lab we need to forge a new cookie in which the key "showpassword" is set to "yes". To do that we are going to perform a **[known-plaintext attack](https://alamot.github.io/xor_kpa/)** against the web application.  
The consists in exploiting the XOR encryption algorithm for which:
1. plaintext ⊕ key = encrypted_text
2. encrypted_text ⊕ plaintext = key
3. encrypted_text ⊕ key = plaintext

Extract cookie from Chrome DevTools or Burpsuite Proxy
<img src="https://user-images.githubusercontent.com/110602224/236574429-18fbb292-38b5-4985-aefc-2fff77dd6305.png" width=200 height=auto>
                                         
Cookie == ciphertext or encrypted_text
$defaultData == plaintext
                                         
Point two = base64_decode(cookie) ⊕ json_encode($defaultData)

PHP script to find the key:
```php
<?php

$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");

function xor_encrypt($in) {
    $key = base64_decode("MGw7JCQ5OC04PT8jOSpqdmkgJ25nbCorKCEkIzlscm5oKC4qLSgubjY%3D");
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

$key = xor_encrypt(json_encode($defaultdata));

echo $key;

?>
```
$key == KNHLKNHLKNHLKNHLKNHLKNHLKNHLKNHLKNHLKNHLK (The key is repeated because of the for loop on every character).
    
Create a cookie to test whether the key is valid or not
Point one = base64_encode[json_encode($defaultData) ⊕ "KNHL"]
```php
<?php

$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");

function xor_encrypt($in) {
    $key = "KNHL";
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

$data = base64_encode(xor_encrypt(json_encode($defaultdata)));

echo $data;

?>
```
Cookie == MGw7JCQ5OC04PT8jOSpqdmkgJ25nbCorKCEkIzlscm5oKC4qLSgubjY=
    
So, now that we know that the key works, let's create a new cookie with "showpassword" set to "yes".
```php
<?php

$defaultdata = array( "showpassword"=>"yes", "bgcolor"=>"#ffffff");

function xor_encrypt($in) {
    $key = "KNHL";
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

$data = base64_encode(xor_encrypt(json_encode($defaultdata)));

echo $data;

?>
```
Cookie == MGw7JCQ5OC04PT8jOSpqdmk3LT9pYmouLC0nICQ8anZpbS4qLSguKmkz
    
In Burpsuite repeat a GET request for / using the new cookie and retrieve the password for the next level: **YWqo0pjpcXzSIl5NMAVxg12QxeC1w9QG**
<img src="https://user-images.githubusercontent.com/110602224/236577300-301f784c-ad31-42cc-a4a1-567692c1a5bc.png" width=900 height=auto>
