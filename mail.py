# -*- coding: utf-8 -*-
import poplib
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import decode_header
import email
#import time
import tools

def check_email():
    try:
        mail = tools.load('data/mail.json')
        p = poplib.POP3(mail['pop']['server'])
        p.user(mail['pop']['user'])
        p.pass_(mail['pop']['pwd'])
        ret = p.stat()
        tools.sys_log(1,'login suecss!')
    except:
        print('Login failed!')
        sys.exit(1)
    lstr = p.top(ret[0], 0)
    strlist = []
    for x in lstr[1]:
            try:
                strlist.append(x.decode())
            except:
                try:
                    strlist.append(x.decode('gbk'))
                except:
                    strlist.append((x.decode('big5')))
    mm = email.message_from_string('\n'.join(strlist))
    sub = decode_header(mm['subject'])
    if sub[0][1]:
        submsg = sub[0][0].decode(sub[0][1])
    else:
        submsg = sub[0][0]
    print submsg
    if submsg.strip() == u'关机':
        tools.sys_log(2,'turn off!')
        return 0
    elif submsg.strip() == u'重启':
        tools.sys_log(2,'restart!')
        return 1
    p.quit()

#发送配置清单 
def send_email(str):
    mail = tools.load('data/mail.json')
    user = mail['stmp']['user']
    pwd = mail['stmp']['pwd']
    to = [str]
    msg = MIMEText('')
    msg['Subject'] = '已收到命令!'
    msg['From'] = user
    msg['To'] = ','.join(to)
    s = smtplib.SMTP(mail['stmp']['server'])
    s.login(user, pwd)
    s.sendmail(user, to, msg.as_string())
    tools.sys_log(2,('%s send email!')%(to))
    s.close()
    
