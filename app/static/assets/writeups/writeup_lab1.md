# Lab1 - WebGoat

### Prerequisites

We strongly recommend installing Burp Suite before doing lab exercises. Using this tool will help you with the challenges and allow you to tamper with the requests easily.
Please create an account on the WebGoat website that was deployed on the platform.

### Exercise 1 - SQL Injection

1. Go to ***(A3) Injection*** tab, select ***SQL Injection (into)*** and then select lesson no. 11.
2. Read the description of the challenge. In this challenge, you have to leverage the lack of string sanitization in the application. Analyze how SQL query is created. Notice that the application takes your input and inserts the values you have submitted into ***name*** and ***auth_tan*** variables.
4. Try creating a statement that always resolves to **true*****. Remember to close any additionally opened quotes so the statement does not result in an error.
<details><summary>Reveal Solution</summary>
The correct solution is putting any string in <em><b>name</em></b> variable and <em><b>' OR '1' = '1</em></b>  in <em><b>auth_tan</em></b> variable.
<br>
This works because you have expanded the <em>WHERE</em> statement by adding <em>OR</em> keyword and putting a true statement after it. It made the whole statement behind <em>WHERE</em> keyword true, and and resulted in displaying the requested data.

</details>


### Exercise 2 - SQL Injection (Advanced)

1. Go to ***(A3) Injection*** tab, select ***SQL Injection (advanced)*** and then select lesson no. 3.
2. Read the description of the challenge. In this task, you need to pull data from a different table than the one that has a vulnerability.
3. Investigate what is the SQL query by trying to input some value in form fields.
4. You can solve the challenge either by finishing the current query and appending a second one or by using UNION SELECT. If you choose the UNION SELECT solution, remember that statements within UNION must have the same number of columns.
<details><summary>Reveal Solution 1</summary>
The correct solution is putting <em><b>'; SELECT * FROM user_system_data;--</em></b> in <em><b>last_name</em></b> field. This worked because you closed the current query by appending <em><b>';</em></b> and added a second query that retrieves the data from the second table. Then you added <em><b>--</em></b> at the end of your payload to comment out the rest of the original query (closing quote).
</details>
<details><summary>Reveal Solution 2</summary>
Another correct solution is putting <em><b>' UNION SELECT 1, user_name, password, cookie, 'A', 'B', 1 from user_system_data;--</em></b> in <em><b>last_name</em></b>. You have successfully created a UNION SELECT statement. To make this work you had to list all columns that are present in the second table and append dummy ones to match the number of columns and data type in each one of the corresponding columns in the first table. Then you added <em><b>--</em></b> at the end of your payload to comment out the rest of the original query (closing quote).
</details>

#### How to prevent the issue

The key to avoiding SQL Injections in your application is to properly sanitize any data that was submitted by the user so it is never interpreted by your backed database. One way to do that is to use Parameterized** queries** whenever you need to retrieve something from an SQL database using user input. You simply pass user input values as parameters that are always treated literally and not interpreted by the SQL engine.

**Reference:** *https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html*
<em><b></em></b>


### Exercise 3 - Reflected Cross-Site Scripting

1. Go to ***(A3) Injection*** tab, select ***Cross-site scripting*** and then select lesson no. 7.
2. In this challenge, you have to identify, which input field may be vulnerable to XSS. 
3. Try to think about how the inputs are processed by the application and what types of inputs there may be.

<details><summary>Reveal Solution</summary>
The correct solution is putting <em><b>&ltscript&gtalert()&lt/script&gt</em></b> in the credit card number field. From all the information that the user inputs on this page, only the credit card number is reflected. As the application does not sanitize the inputs, it is possible to perform an XSS attack.
</details>

#### How to prevent the issue

To prevent this issue you should make sure that sanitization of any user input is being done. Additionally, many modern frameworks already support XSS protection, so do not use outdated components in your applications.
**Reference:** *https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html*


### Exercise 4 - Path Traversal

1. Go to ***(A3) Injection*** tab, select ***Path Traversal*** and then select lesson no. 5.
2. In this challenge, you have to retrieve a secret file using the path traversal vulnerability.
3. It might be useful to use **Burp Suite** in this challenge to see the server's responses and tamper with requests.
4. Intercept the request in Burp, send it to Repeater and try to tamper with it to retrieve the secret file.

<details><summary>Reveal Solution</summary>
By intercepting the requests with Burp, you can see that the server is telling you the path of the currently displayed file in the location header:<br>
<img src="./static/assets/writeups/lab1.4.1.png"> <br>
If you try to put this path in the URL of your GET request, you can observe that the server's response includes some directory listing, although there is no secret file. Also, you can observe that there are two .png extensions in the response - that means the app only takes the filename, without extension:<br>
<img src="./static/assets/writeups/lab1.4.2.png"> <br>
It turns out that you can traverse by changing the <em><b>id</em></b> parameter in your URL. However, if you try to use some special characters, it will not work as in this challenge there is some kind of character blacklisting applied. The solution to that is to simply URL-encode your payload.<br>
When you put <em><b>../../</em></b> in URL-encode form in <em><b>id</em></b> parameter, you can see <em><b>path-traversal-secret.jpg</em></b> file listed in the response.<br>
<img src="./static/assets/writeups/lab1.4.3.png"> <br>
Now we only need to retrieve this file. We can do that by calling its path, without the .png extension, as the application adds it.
<br><img src="./static/assets/writeups/lab1.4.4.png"> <br>
Now the response gives you a tip on what you should submit as a challenge solution in the field below the picture.
</details>

#### How to prevent the issue

To prevent path traversal issues, proper input validation must be applied. Any input that looks like a reference to the internal resources should not be accepted by the server.

**Reference:** *https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html*


### Exercise 5 - Spoofing an authentication cookie

1. Go to ***(A1) Broken Access Control*** tab, select ***Spoofing an authentication cookie*** and then select lesson no. 2.
2. In this challenge, you have to predict the value of the authentication cookie and log in as user Tom.
3. You have two sets of credentials - try to look into how the cookie is created by logging in to these accounts.
4. It might be useful to use some decoding tools like **CyberChef** (*https://gchq.github.io/CyberChef/*) in this challenge.

<details><summary>Reveal Solution</summary>
The format of the cookie suggests that it is Base64 encoded. After decoding it, it appears that it is in hexadecimal format. After converting it, you can see that the cookie value is some random string followed by the username spelled backward:
<br><img src="./static/assets/writeups/lab1.5.1.png"> <br>
Additionally, the "random" value is not that random - for both users, it is the same. Try to generate the cookie with the same approach for the username Tom:
<br><img src="./static/assets/writeups/lab1.5.2.png"> <br>
To solve the challenge, add a generated cookie to the login request:
<br><img src="./static/assets/writeups/lab1.5.3.png"> <br>
</details>

#### How to prevent the issue

While using session cookies in your application, you must remember that the cookie must be unpredictable, meaningless and long enough to prevent brute-force attacks. 

**Reference:** *https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html*


### Exercise 6 - Server-side Request Forgery

1. Go to ***(A10) Server-Side Request Forgery*** tab, select ***Server-Side Request Forgery*** and then select lesson no. 2.
2. In this challenge, you need to trick the server, so it displays an image of Jerry, instead of Tom.
3. Use **Burp Suite** to intercept the request and try to tamper with it.

<details><summary>Reveal Solution</summary>
As you can see, the server is calling a resource located in path <em><b>images/tom.png</em></b>:
<br><img src="./static/assets/writeups/lab1.6.1.png"> <br>
You can solve the challenge by changing it to <em><b>images/jerry.png</em></b>.
</details>

#### How to prevent the issue

To prevent SSRF vulnerabilities in web applications, it is recommended to use a whitelist of allowed domains, resources, and protocols from where the web server can fetch resources, validate the user input and try to limit user functions that control the server.

**Reference:** *https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html*

