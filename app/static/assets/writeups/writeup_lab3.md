# Lab3 - bWAPP

### Prerequisites

We strongly recommend installing Burp Suite before doing lab exercises. Using this tool will help you with the challenges and allow you to tamper with the requests easily.
Please create an account on the bWAPP website that was deployed on the platform. Set security level to *medium*.

### Exercise 1 - iFrame Injection

1. Go to ***Bugs*** tab, select ***iFrame Injection*** and click ***Hack*** button.
2. Investigate the URL of the page. Notice that the iframe is displaying *robots.txt* in the current page.

<details><summary>Reveal Solution</summary>
<em><b></em></b>
In this challenge the iframe takes three GET parameters in its URL: <em><b>ParamUrl</em></b>, <em><b>ParamWidth</em></b> and <em><b>ParamHeigh</em></b>. We can try to change the parameters and inject some payload.<br>
The solution can be adding <em><b>&quot;&gt;&lt;/iframe&gt;&lt;p&gt;test&lt;/p&gt;</em></b>
 to the last parameter. In this solution you escape the iframe by <em><b>&quot;&gt;&lt;/iframe&gt;</em></b> and append HTML you want to display on the page, in this example, a paragraph with text <em><b>test</em></b>.
</details>

#### How to prevent the issue

To prevent taking advantage of iframes by attacker, you must properly sanitize them. Make sure you use *sandbox* attribute - it adds a set of restrictions and prohibits all elements that could pose a security risk, including plugins, forms, scripts, outbound links, cookies, local storage, and access to the same-site page. You can also use *allow* atribute to whitelist allowed functionalities and use Content-Security-Policy header to protect against various injection attacks.

**Reference:** *https://www.reflectiz.com/blog/iframe-security/*

### Exercise 2 - OS Command Injection

1. Go to ***Bugs*** tab, select ***OS Command Injection*** and click ***Hack*** button.
2. Try to tamper with DNS lookup field to exploit Command Injection.

<details><summary>Reveal Solution</summary>
<em><b></em></b>
Correct solution is to use pipe to escape current command and append a new one e.g.: <em><b>| echo "test"</em></b>
</details>

#### How to prevent the issue

To prevent the issue, avoid calling OS commands directly. If that's not possible, use parametrization and validate the user input.

**Reference:** *https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html*


### Exercise 3 - Broken Authentication - Weak passwords

1. Go to ***Bugs*** tab, select ***Broken Auth. - Weak passwords*** and click ***Hack*** button. For this exercise change security level to *low*.
2. Try to log in as user *test*. Use this password list to conduct a successful brute force attack: *[pwd.txt](./static/assets/writeups/pwd.txt)*

<details><summary>Reveal Solution</summary>
<em><b></em></b>
Intercept the request when trying to log in with Burp Suite and send it to <em><b>Intruder</em></b>. Configure payload position for password parameter:
<br><img src="./static/assets/writeups/lab3.3.1.png"> <br>
Next, go to <em><b>Payloads</em></b> tab and paste passwords from provisted list to the payload list.
<br><img src="./static/assets/writeups/lab3.3.2.png"> <br>
Click <em><b>Start attack</em></b> and observe responses. Notice that for password <em><b>test</em></b> response includes a <em><b>Successful login!</em></b> message.
<br><img src="./static/assets/writeups/lab3.3.3.png"> <br>
</details>

#### How to prevent the issue

Ensure that your application requires minimum lenght of the password. Do not limit users in terms of which characters should they use in their passwords. Ensure password rotation when leaks occur.

**Reference:** *https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html*

### Exercise 4 - Session Management - Session ID in URL

1. Go to ***Bugs*** tab, select ***Session Mngt. - Session ID in URL*** and click ***Hack*** button. For this exercise change security level to *low*.
2. For this challenge you will need a second user created.
3. Try to access the page as second user, while being logged in as the first one.

<details><summary>Reveal Solution</summary>
<em><b></em></b>
Open another browser and log in as second user. Go again to the challenge page and note the PHPSESSID from the URL. Then go back to the browser where you are logged as the first user - intercept the request and change PHPSESSID in the URL - now you can see in the response that you are logged in as the second user.
</details>

#### How to prevent the issue

Session tokens should never be transmitted as URL parameter, becuse then it is very easy to "look someone over the shoulder" and note their session ID. Make sure that in your applications, session IDs are transmitted as a cookie via HTTPS protocol.

**Reference:** *https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html*


### Exercise 5 - Insecure DOR

1. Go to ***Bugs*** tab, select ***Insecure DOR (Order Tickets)*** and click ***Hack*** button. 
2. Try to order few tickets without any money being taken from your account.

<details><summary>Reveal Solution</summary>
<em><b></em></b>
Intercept the request of ordering the tickets. Note that each time you increase number of tickets, there is total price in the response. It is possible that application uses some variable to calculate the total price. Try adding <em><b>ticket_price</em></b> parameter to the request body.
<br><img src="./static/assets/writeups/lab3.5.1.png"> <br>
As you can see, due to improper access control, you were able to modify the price of the ticket.
</details>

#### How to prevent the issue

Insecure Direct Object Reference (IDOR) is a vulnerability that arises when attackers can access or modify objects by manipulating identifiers used in a web application's URLs or parameters. It occurs due to missing access control checks, which fail to verify whether a user should be allowed to access specific data. To mitigate IDOR, implement access control checks for each object that users may try to access. Avoid exposing such identifiers in request bodies and URL parameters.

**Reference:** *https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html*

