# Level 12

## Software used
- Google Chrome
- [phponline.io](https://onlinephp.io)

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


        if(filesize($_FILES['uploadedfile']['tmp_name']) > 1000) {
        echo "File is too big";
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

**Code analysis**

```php
function genRandomString() {
    $length = 10;
    $characters = "0123456789abcdefghijklmnopqrstuvwxyz";
    $string = "";

    for ($p = 0; $p < $length; $p++) {
        $string .= $characters[mt_rand(0, strlen($characters)-1)];
    }

    return $string;
}
```
The **genRandomString()** function aims at creating a 10-characters random string.  
[mt_rand](https://www.php.net/manual/en/function.mt-rand.php): generate a random value via the Mersenne Twister Random Number Generator  

```php
function makeRandomPath($dir, $ext) {
    do {
    $path = $dir."/".genRandomString().".".$ext;
    } while(file_exists($path));
    return $path;
}
```
The **makeRandomPath()** function creates a full directory/filename path.  
[file_exists](https://www.php.net/manual/en/function.file-exists.php): checks whether a file or directory exists  

```php
function makeRandomPathFromFilename($dir, $fn) {
    $ext = pathinfo($fn, PATHINFO_EXTENSION);
    return makeRandomPath($dir, $ext);
}
```
[pathinfo](https://www.php.net/manual/en/function.pathinfo.php): returns information about a file path (either an associative array or a string, depending on flags.)  
The PATHINFO_EXTENSION returns the extension of the file, example:
```php
<?php
  $fn = "test.txt";
  $ext = pathinfo($fn, PATHINFO_EXTENSION);
  echo $ext
?>
```
Print the extension _txt_.

The function **makeRandomPathFromFilename()** takes two arguments, a directory name and a filename. From the filename is derived its extension. 
The directory name and the extension are passed as arguments to the function **makeRandomPath()**.  

```php
if(array_key_exists("filename", $_POST)) {
    $target_path = makeRandomPathFromFilename("upload", $_POST["filename"]);


        if(filesize($_FILES['uploadedfile']['tmp_name']) > 1000) {
        echo "File is too big";
    } else {
        if(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $target_path)) {
            echo "The file <a href=\"$target_path\">$target_path</a> has been uploaded";
        } else{
            echo "There was an error uploading the file, please try again!";
        }
    }
} else {
```
The first if statement checks whether the key _filename_ exists in [$POST](https://www.php.net/manual/en/reserved.variables.post.php).  
If [array_key_exists](https://www.php.net/manual/en/function.array-key-exists.php) returns _True_, the function **makeRandomPathFromFilename** 
is called with arguments _upload_ (as directory name) and the value of key _filename_ in the array _$_POST_ (as filename).  
The results is then assigned to the variable _$target_path_.  

The second, nested, if statement checks whether the uploaded file is greater than 1000 bytes or not.  
The global variable [_$\_FILES_](https://www.php.net/manual/en/features.file-upload.post-method.php) contains all information about uploaded file like:
- ['uploadedfile']['tmp_name'] : The temporary filename of the file in which the uploaded file was stored on the server.  
If [filesize](https://www.php.net/manual/en/function.filesize.php) returns _True_ the application echoes the message 'File is to big' back to the user.  

If the file size is less than 1000 bytes the third and last nested if statement is run.  
[move_uploaded_file](https://www.php.net/manual/en/function.move-uploaded-file.php) moves the uploaded file to a new randomized target path.  

___

Testing the upload function using a small .jpeg image file and capturing the POST request and response in Burpsuite Proxy:
<img src="https://user-images.githubusercontent.com/110602224/236948230-b5c27164-c4d6-4914-b1e1-056900eb0069.png" width=900 height=auto>

The upload request is made through the POST method with Content-Type _multipart/form-data_.  

___






