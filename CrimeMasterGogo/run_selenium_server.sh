ps -ef | grep sele | grep -v grep | grep -vi screen | awk '{print $2}' | xargs kill -9
ps -ef | grep -i chrome |  grep -vi screen  | awk '{print $2}' | xargs kill -9

while [ 1 ]
	do
      if [ `uname -a | awk '{print $1}'` == 'Darwin' ]
        then
            os='mac'
        else 
            os='ubuntu'
        fi
       echo java -Dwebdriver.chrome.driver=./extensions/$os/chromedriver -jar ./extensions/jars/selenium-server-standalone-3.0.0-beta1.jar 
	  java -Dwebdriver.chrome.driver=./extensions/$os/chromedriver -jar ./extensions/jars/selenium-server-standalone-3.0.0-beta1.jar >selenium.log &
	  sleep 86400
	  ps -ef | grep sele |  grep -vi screen | awk '{print $2}' | xargs kill -9
	  ps -ef | grep -i chrome |  grep -vi screen  | awk '{print $2}' | xargs kill -9

	done
