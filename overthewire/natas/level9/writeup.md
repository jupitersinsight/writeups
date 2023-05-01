# Level 9

## Software used
- Google Chrome + FoxyProxy extension
- Burpsuite Community

## Hint
(sourcecode)
```php
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    passthru("grep -i $key dictionary.txt");
}
?>
```

## Solution

This website offers a search function which returns words containing user-supplied string if not empty. 
<img src="https://user-images.githubusercontent.com/110602224/235471474-02c833d7-2a05-4ae9-a7a5-8098689f1336.png" width=600 height=auto>

Example submitting the word _friend_.

<img src="https://user-images.githubusercontent.com/110602224/235471696-954f41ea-9164-40a7-b713-48d7d776fb07.png" width=600 height=auto>

By inspecting the sourcecode of the search function, we can see that, when the user supplied input is not empty, it is directly embedded in a shell command.  
Since there is no filter in action, this is a easy exploitation of an [OS Command Injection vulnerability](https://owasp.org/www-community/attacks/Command_Injection).

Let's breakdown the PHP function:
- [array_key_exists](https://www.php.net/manual/en/function.array-key-exists.php): returns true if the given key is set in the array. key can be any value possible for an array index  
- [$\_REQUEST](https://www.php.net/manual/en/reserved.variables.request.php): an associative array that by default contains the contents of $_GET, $_POST and $_COOKIE
- [passthru](https://www.php.net/manual/en/function.passthru): similar to the exec() function in that it executes a command

Inject the command to read the password for the next level at **/etc/natas_webpass/natas10**: ```; cat /etc/natas_webpass/natas10;```  
The web server will execute the following list of commands ```grep -i ; cat /etc/natas_webpass/natas10; dictionary.txt``` where ```;``` instructs the server to execute the next command regardless of the outcome of the previous command.  

Injecting the command in the input field returns the password: **D44EcsFkLxPIkAAKLosx8z3hxX1Z4MCE**  
<img src="https://user-images.githubusercontent.com/110602224/235476589-964678cb-116e-4f38-a739-39a00345ad94.png" width=600 height=auto>

Using Burpsuite's module **Repeater** we need to URL-encode to avoid breaking the URL syntax (shortcut to URL-encode is **CTRL+U** on highlighted text).
<img src="https://user-images.githubusercontent.com/110602224/235477216-03b5a27b-1c34-463b-8182-4eca439a3ef6.png" width=900 height=auto>


