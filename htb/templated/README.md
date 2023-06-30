**WIP**

Machine is vulnerable to SSTI (Server-Side Template Injection)  

Maintenance message in root webpage displays "Proudly powered by Flask/Jinja2".  
Requesting a non-existant resource from GET (using BurpSuite Repeater) results in an error message where the supplied input is passed as argument of a `<str></str>` HTML tag.  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/c227934a-13b5-4b32-aba2-f3af4b78d968" width=900 height=auto> 

Since it is already known that Flask and Jinja2 are being used, injecting a simple expression in legal Jinja2 syntax such as `{{ ... }}`  results in a valid response from the server  

<img src="https://github.com/jupitersinsight/writeups/assets/110602224/99696887-0598-44c6-9912-96b25d15488c" width=900 height=auto>
