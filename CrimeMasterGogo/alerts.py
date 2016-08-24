'''
Created on 12-Mar-2015

@author: kiev
'''

#!/usr/bin/python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback
import logging
import os
TO = []
email_sender = 'Automation@quadanalytix.com'

logger = logging.getLogger(__name__)
def sendEmail(SUBJECT,htmlFile,emailTOList):
    
    passwd='AFFb-88512'
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email_sender, passwd)
    
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email_sender
    emailTOList += TO
    emailTOList = list(set(emailTOList))
    msg['To'] = ','.join(email for email in emailTOList if email != '')
    with open(htmlFile,'r') as htmlFileDesc:
        html=htmlFileDesc.read()
    part = MIMEText(html, 'html')
    msg.attach(part)
    
    
    try:
        logger.info ('Email drafted,sending now to '+msg['To'])
        server.sendmail(email_sender, emailTOList,  msg.as_string())
        logger.info ('email sent')
    except:
        var = traceback.format_exc()
        logger.error(var)
        logger.error('error sending mail')
    
    server.quit()

def snsAlert(access_key,secret_key,topic,message,subject,region='us-west-2'):
    from boto import sns
    conn = sns.connect_to_region(region, aws_access_key_id=access_key,aws_secret_access_key=secret_key)
    conn.publish(topic, message, subject)

if __name__ == "__main__": 
    import argparse
    parser = argparse.ArgumentParser(description='Email sending program')
    parser.add_argument('-s','--subject', help='Subject of mail',required = True)
    parser.add_argument('-f','--file', help='file to be sent',required = True)
    parser.add_argument('-t','--to', help='comma separated list of users email to be sent to or SNS Alter topic')
    parser.add_argument('-secret','--secret_key', help='secret Key for SNS') 
    parser.add_argument('-access','--access_key', help='access  Key for SNS')
    args = vars(parser.parse_args())
    msg = ''
    if ( args['secret_key'] and args['access_key'] )  :
        if os.path.exists(args['file']) :
            with open(args['file'],'r') as htmlFileDesc:
                msg = htmlFileDesc.read()
        if msg == '' :
            snsAlert(args['access_key'],args['secret_key'],args['to'],args['file'],args['subject'])
        else :
            snsAlert(args['access_key'],args['secret_key'],args['to'],msg,args['subject'])
    else :
        sendEmail(args['subject'],args['file'],args['to'].split(','))
