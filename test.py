# -*- coding: gb2312 -*-
import os
import platform
import tools
import mail

def pingtest(ip):
    #ip = "192.168.1.3"
    if platform.system()=='Windows':
        pstr = "ping -n 1 -w 1"
    else:
        pstr = "ping -w 1"
    print pstr
    reval=os.system('%s %s'%(pstr,ip))
    print reval
    return reval

monito = tools.load('data/monito.json')
count_True,count_False = 0,0
for i in monito['list']:
    if pingtest(i['ip']):
        count_False +=1
    else:
        count_True += 1

#print count_True,count_False

if count_False>0:
    print "发送邮件"
    mail.send_email('mcyrj@qq.com')
elif(count_False>count_True/2):
    print "警告"
elif(count_True==0):
    print "通知，关机"




