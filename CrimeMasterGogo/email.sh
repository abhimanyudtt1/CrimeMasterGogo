#!/usr/bin/env bash

x=`cat report.html | grep -A1 'Test Status'| tail -1 `

if [ `echo $x | grep -i passed | wc -l` -ge 1 ]
    then
        python alerts.py -t $1 -f $2 -s "UI Automation Report : Passed "
    else
        python alerts.py -t $1 -f $2 -s "UI Automation Report : Failed"
    fi
