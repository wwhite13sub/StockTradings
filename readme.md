# Hosting: https://carstocks.herokuapp.com/

NAME: Wanda White
OVERVIEW/DESCRIPTION: Project is to develop a paper trading website. The site is to be used by anyone who is interested in a paper trading that will grant an initial cash amount and allow user to purchase/sell two stocks. It will save all user registration and transaction data from one login session to another. The website has five main pages: 1) Registration "Sign Up" page, 2) Login page, 3) Reset page, 4) Main Portfolio Page with ability to purchase or sell TSLA or BMW, 5) Transaction History page. The site should have all functionality on both desktop and mobile devices and should be accessed via a hosting web site.


DETAILS ON HOW TO USE IT OR WHAT FUNCTIONALITY IS OFFERED: 
a) Site users will access website via internet by entering site address. 
b) On Sign Up page, user will create a unique user id and enter a password for the user id. A cash account balance of $5,000.00 will be granted to the user. User will then be sent to Login page. 
c) On Login page, user will enter user id and password. User id and password will be validated against values in table. Once validated, user will be taken to Portfolio Summary Page. 
d) On Portfolio Summary page, users will be able to view
current cash balance,
number shares TSLA stock,
current price TSLA stock,
current balance for TSLA (#shares times current price),
number shares BMW stock,
current price BMW stock,
current balance for BMW (#shares times current price)
total portfolio amount (cash balance + TSLA balance + BMW balance e) On Portfolio Summary page, user will select TSLA or BMW and two popup charts will be displayed:
line chart with stock close price for last three months
chart with open, high, low, on first day of month for last three months 
f) On Portfolio Summary page, user will select Buy/Sell for TSLA or BMW and popup will:
    display current price
    allow sell based on current stock quantity OR allow buy based on current cash balance and current stock price
once buy or sell is completed the page will automatically refresh the Portfolio Summary 
g) On Transaction History page, user will
view, all buy/sell transactions and current days BMW or TSLA stock price by hour
user will click on reset to be directed to Reset page 
h) On Reset page, uses will be able to reset (which will delete all transactions and the cash account balance will be set to $5,000.00). User will then be sent to Portfolio Summary Page. 
i) Site users will be able to do anything on mobile device that can be done on desktop. 
j) From one login session to another, all transactions completed by a user will be stored until user initiates Reset.


TECHNOLOGIES USED: Python Django, html, css custom rules, JavaScript, ESLint, Bootstrap, DesignIO, GitHub, HOSTING SITE: Heroku

IDEAS FOR FUTURE IMPROVEMENT: a) Improve user experience by allowing user to select from more than just two stocks to add to the portfolio. b) Improve user experience by allowing user to change password. c) Improve user experience by allowing user to reset password (if it is forgotten) by answering pre-answered questions with the correct answers.
d) Improve user experience by allowing user to enter a price target for a purchase/sell transaction. e) Improve user experience by displaying total portfolio balance by day for user requested time periods

INSTALLATION INSTRUCTIONS: a)Use browser of choice (for example Chrome). b)Go to Github.com and select StockTradings and clone repository. c)Open in code editor(for example Visual Studio Code). d)Execute application in terminal with python manage.py runserver command e)Application will display on local host.

EXECUTION INSTRUCTIONS: a) Go to go to  https://carstocks.herokuapp.com/ in browser, you will be directed to home page. 

b) Click on "Signup" on the navigation bar to create user account. c) Create user name and password.
    Click on "Sign up" button to confirm and you will be directed to login page.
d) Log in with created user id and password.
    Click "Log in" button to confirm you will be directed to home page. e) To purchase or sell stock click on "PORTFOLIO" on the navigation bar.
    Click on "TSLA" or "BMW.DE".
    Increase or decrease the number of stocks. 
    Click on "Buy" or "Sell".
f.) To view transaction history click on "Transactions" on the navigation bar. 
g) To reset account click on "Reset Account" link within "Transactions" page.
  you will be directed to Reset Account page, click on "Reset Account" to confirm.
h.) To log out click on "Logout" on navigation bar.
About

## USER STORIES

1.	As a paper trading user, I want to access a web application sign up page, where I can create my unique user id and a password so that my initial $5,000.00 cash allocation will be recorded as a transaction associated to my user id and immediately after successful registration.

2.	As a paper trading user, I want to access a web application login page, where I can enter my user id and password so that it will be verified and immediately after successful login, the summary portfolio page is displayed. 

3.	As a paper trading user, I want to access a web application reset page where I can initiate reset so that all my portfolio transactions are deleted, I am given a new initial $5,000.00 cash allocation and immediately after successful reset, the summary portfolio page is displayed.


4.	As a paper trading user, I want to access a web application portfolio page so that I can view my cash balance, BMW shares, BMW CURRENT share price, BMW account value (# shares times current share price), TSLA shares, TSLA CURRENT share price, TSLA account value (# shares times current share price) and total portfolio value.

5.	As a paper trading user, I want to access a web application portfolio page and click on BMW or TSLA so that on that same page, a daily price chart (over three months prior to current date) for the selected stock is displayed.      

6.	As a paper trading user, I want to access a web application portfolio page and click on a BUY/SELL indicator for either BMW or TSLA so that on that same page, I will be able to either 1) buy the selected stock dependent on my cash balance or 2) sell selected stock (dependent on my number of current shares) and immediately after a successful transaction the summary portfolio page with refreshed data is displayed.        

7.	As a paper trading user, I want to access a web application transaction page with two charts so that I can view:  1) all transactions for my account (date, time, transaction, stock, quantity, share price and cash impact) and 2) a line chart displaying the daily total value of my account since my initial $5,000.00 cash was allocated, thru the end of prior month.

8.	As a paper trading user, I want to access the web application on a mobile app so that I can do everything on my mobile app that I can do on a desktop. 

9.	As a paper trading user, I want to access the web application from a hosted web site so that I can access it by entering:  https://carstocks.herokuapp.com/
