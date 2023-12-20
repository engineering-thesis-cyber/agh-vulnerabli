# Lab2 - DSVW

### Prerequisites

We strongly recommend installing Burp Suite before doing lab exercises. Using this tool will help you with the challenges and allow you to tamper with the requests easily.

### Exercise 1 - Stored Cross-Site Scripting

1. Click the ***vulnerable*** link next to the exercise ***Cross-Site Scripting (stored)***.
2. Try to input a comment that will include some script.

<details><summary>Reveal Solution</summary>
Putting <em><b>&ltscript&gtalert()&lt/script&gt</em></b> in the comment field will result in the script being executed each time someone visits the page where the comment was put.

</details>

#### How to prevent the issue

To prevent this issue you should make sure that sanitization of any user input is being done. Additionally, many modern frameworks already support XSS protection, so do not use outdated components in your applications.
**Reference:** *https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html*


### Exercise 2 - XML External Entity 

1. Click the ***vulnerable*** link next to the exercise ***XML External Entity (local)***.
2. Investigate the URL of the page. Try to tamper with parameter ***xml*** to exploit the vulnerability.

<details><summary>Reveal Solution</summary>
The correct solution is putting <em><b>!DOCTYPE example [&lt;!ENTITY xxe SYSTEM &quot;file:///etc/passwd&quot;&gt;]&gt;&lt;root&gt;%26xxe;&lt;/root&gt;</em></b> in the <em><b>xml</em></b> parameter. You have created an external entity called <em><b>xxe</em></b> that points to some internal resource that you should not have access to. Then you called it by <em><b>%26xxe;</em></b>. You needed to URL-encode <em><b>&</em></b> symbol as it also means appending a new parameter in the URL. If you didn't encode it, it would result in an error.
</details>

#### How to prevent the issue

This issue appears often when using the default, often insecure configurations of XML parser. The ultimate solution is external entities and external document-type declarations.

**Reference:** *https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html*

<em><b></em></b>


### Exercise 3 - Arbitrary Code Execution

1. Click the ***vulnerable*** link next to the exercise ***Arbitrary Code Execution***.
2. Investigate the URL of the page. Try to tamper with the parameter **domain** to exploit the vulnerability.

<details><summary>Reveal Solution</summary>
The correct solution is to append <em><b>; [command]</em></b> to the parameter in the URL. You can use any Linux command after ending the previous one, which is nslookup. <em><b>;</em></b> ends the current command.
</details>

#### How to prevent the issue

To prevent the issue, avoid calling OS commands directly. If that's not possible, use parametrization and validate the user input.

**Reference:** *https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html*

### Exercise 4 - HTTP Header Injection

1. Click the ***vulnerable*** link next to the exercise ***HTTP Header Injection (phishing)***.
2. Investigate the URL of the page. Try to tamper with the parameter **charset** to exploit the vulnerability. You can see that this parameter sets the encoding of the page by adding a new header.

<details><summary>Reveal Solution</summary>
You can see that this parameter sets the encoding of the page by adding it to the Content-Type header in response.
<br><img src="./static/assets/writeups/lab2.4.1.png"> <br>
The correct solution is <em><b>%0D%0A%0D%0A&lt;%20DOCTYPE%20html&gt;&lt;html&gt;&lt;head&gt;&lt;title&gt;test&lt;%2Ftitle&gt;&lt;%2Fhead&gt;&lt;%2Fhtml&gt;</em></b>. After setting the charset, you can add CRLF (%0D%0A%0D%0A) that is required in HTTP request after last header and append anything you would like to have displayed in the response body. In the example, it is setting up the title of the webpage to <em><b>test</em></b>, but you can e.g. create a form that would be useful in a phishing campaign.
<br><img src="./static/assets/writeups/lab2.4.2.png"> <br>
</details>

#### How to prevent the issue

The best prevention technique is to not use user input directly inside response headers. If that is not possible, you should always use a function to encode the CRLF special characters. Another good web application security best practice is to update your programming language to a version that does not allow CR and LF to be injected inside functions that set HTTP headers.

**Reference:** *https://www.invicti.com/learn/crlf-injection/*