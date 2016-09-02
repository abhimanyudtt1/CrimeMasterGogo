#!/usr/bin/env bash

# Author : abhimanyu Dutta
# email : adutta@quadanalitix.com

# This is a script to install Gogo on to a Mac environment 
# by the end of script execution GoGo will be all set to run directly 


# Checking if the script is run as root 
if [ $EUID -ne 0 ] 
    then
        echo "Please Run installer script as a sudo user."
        echo "The script needs to install multiple packages, hence sudo access is required "
        echo "Syntax : sudo $0 "
        exit 127 
    fi


which easy_install

if [ $? -ne 0 ]
    then
        curl https://bootstrap.pypa.io/ez_setup.py -o - | sudo python
    else 
        echo "Easy install present already moving ahead.. "
    fi



which pip

if [ $? -ne 0 ]
    then
        sudo easy_install pip
    else 
        echo "Pip present already moving ahead.. "
    fi

sudo pip install selenium

# Entering configs now 
echo
echo
echo

echo "Please enter the setup details below[ brackets contain default values ]: "
echo

echo -n "Enter config file Name[config.conf]: "
read conf
echo -n "Enter the URL on which test needs to be done[https://app.stg.quadanalytix.com]: "
read url
echo -n "Enter remote server IP [ 127.0.0.1 ]: "
read ip
echo -n "Enter start Time [3-08-2015][dd-mm-yyy]: "
read startTime
echo -n "Enter End Time [13-09-2015][dd-mm-yyy]: "
read endTime
echo -n "Enter Email address [test@test.com]: " 
read email
echo -n "Enter password [test]: "
read password
echo -n "Timeout ( max time to wait for each call ) [60]: "
read timeWait

if [ -z $conf ]
    then
        conf='config.conf'
    fi

if [ -z $url ] 
    then
        url='https://app.stg.quadanalytix.com'
    fi

if [ -z $ip ]
    then
        ip='127.0.0.1'
    fi

if [ -z $startTime ]
    then
        startTime='3-08-2015'
    fi

if [ -z $endTime ]
    then
        endTime='13-09-2015'
    fi

if [ -z $email ]
    then
        email='test@test.com'
    fi

if [ -z $password ]
    then
        password='test'
    fi

if [ -z $timeWait ]
    then
        timeWait=60
    fi


echo "path = ./TestSuit" > $conf
echo "URL = $url" >> $conf
echo "chromeDriver = ./extensions/mac/chromedriver" >>$conf
echo "remote_location = $ip" >> $conf
echo "startTime = $startTime" >> $conf
echo "endTime = $endTime " >> $conf
echo "email = $email " >> $conf
echo "password = $password " >> $conf
echo "timeWait = $timeWait " >> $conf
echo "TestResult = ./result" >> $conf

echo 
echo "Setup coomplete. Please use start.py for running Gogo framework"

