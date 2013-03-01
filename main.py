#-*- coding=utf-8 -*-

import getpass
import state
import core

flag = 'r'

print '请输入你的学号'
username = raw_input('> ')
print '请输入你的密码'
password = getpass.getpass('> ')
userinfo = core.cxcore(username,password)

stat=state.StateMachine(userinfo)

while(flag == 'r'):
    
    print '选择你所需要的功能：'
    print '0、成绩查询  1、课表查询  2、考试查询  3、等级考试查询'
    print '4、退出' 
    choose = raw_input('> ')

    flag=stat.run(choose) 

    
