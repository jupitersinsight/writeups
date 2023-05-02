# Level 10

## Software used
- Google Chrome

## Hints

```php
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    if(preg_match('/[;|&]/',$key)) {
        print "Input contains an illegal character!";
    } else {
        passthru("grep -i $key dictionary.txt");
    }
}
?>
```

## Solution

GREP can search for a given pattern on multiple files, so all we need to do is using the "payload": **a /etc/natas_webpass/natas11**

<img src="https://user-images.githubusercontent.com/110602224/235717843-85c7b06d-a5c9-4172-9e55-efd69794ad4e.png" width=600 height=auto>

If the pattern (in this case 'a') does match with the content of the files, results are printed on screen.  
Remember that the grep command uses the -i option. From grep man page:  
**-i, --ignore-case  
      Ignore case distinctions in patterns and input data, so that characters that differ only in case match each other.**
              
If the password is not printed on screen, change the pattern to another character.
Since letter 't' is not in the password, the match does not occur and the password is not returned as valid result.  
<img src="https://user-images.githubusercontent.com/110602224/235719433-ab7fc14d-ab6a-4a25-85a2-6d81a00d280e.png" width=600 height=auto>

Password: **1KFqoJXi6hRaPluAmk8ESDW4fSysRoIg**



