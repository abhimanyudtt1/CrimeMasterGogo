# CrimeMasterGogo
Author : Abhimanyu Dutta
email : Abhimanyu Dutta

OVERVIEW :

The frame work is a python based selenium web driver tool, It runs tests provided to it in the arguments. 
The TestSuit can contain multiple test suits in it recursively. Each of the test suits run in parallel with one driver assigned to one test suite.
This parallel execution is done with a test engine of unittest. 
Each of the test cases is a python script written as if its a unittest script. The script is inturn invoked by the framework itself


Framework made in python over selenium
To start the framework :
python ./start.py
Usage: start.py [options]

Options:
  -h, --help            show this help message and exit
  -t SUIT, --testSuit=SUIT
                        Give path of the test Suit folder here. Each folder in
                        itself will be treated as a sub testSuit.Each py file
                        will be taken up as testcase which may or may not have
                        smaller specs in it
  -c CONFIG, --config=CONFIG
                        To provide config files
  -v VARIABLE, --variable-list=VARIABLE
                        To define a file that will give a list of variables
                        that may or maynot be used in the check pointing
                        scripts
  -s TEST, --singleTest=TEST
                        To give a Single Test case to run
						
						
eg Config file :
path = ./TestSuit
URL = https://www.facebook.com
chromeDriver = ./extensions/chromedriver
remote_location = 127.0.0.1
startTime = 1438560000
endTime =   1441584000
email = test@test.com
password = test

timeWait = 10

eg variable file :
explore : '.nav-icon.icon-explore'
Cumulative_rating : '[quad-id="productRatings_insight"]'
clear_all_button : '.qq-filter-currentOptionsSelector .link.qq-filter-clearCurrentOptions'
email_tag : 'input[name="email"]'
password_tag : 'input[name="password"]'
submit : 'input[value="sign in"]'
cumulative_ratings : '[quad-id="productRatings_insight"]'


Usage :

The variables in the config files provided can be accessed directly in a test case using the following :
-----------------------------------
from src.config import parser
print parser.URL # Will print 'https://app.stg.quadanalytix.com/login' according to the example config.conf given above 

Similarly the varable file config can be accessed using the same parser class :
from src.config import parser
print parser.email_tag


There are some default APIs that can be used instead of the normal selenium calls, 
these are connected to the timeWait variable in the config.conf. 
These calls try to find,click,type,hower over an element till the timeout is reached and then raises appropriate errors 




To run remote server :
java -Dwebdriver.chrome.driver='./chromedriver' -jar ~/Downloads/selenium-server-standalone-3.0.0-beta1.jar
