#!/usr/bin/env python
#coding=utf-8

import time
import conf
import cxcore
import xkcore
import getpass

flag = 'r'
info = []
cxfail = 32
flagcxlogin = 0
flagxklogin = 0
year = ['2001-2002','2002-2003','2003-2004','2004-2005','2005-2006','2006-2007','2007-2008','2008-2009','2009-2010','2010-2011','2011-2012','2012-2013','2013-2014']

while flag == 'r':
    
    print '选择你所需要的功能：'
    print '0、学期成绩  1、学年成绩  2、历年成绩  3、学生课表查询'
    print '4、学生考试查询  5、等级考试查询 6、我要选课  7、退出'
    choose = raw_input('> ')
    choose = int(choose)
    if(choose not in range(7)):
        if(choose != 7):
            print '选择错误，正在退出'
        flag = 'q'
        info = []
        continue
    
    info.append(choose)

    if(choose == 0 or choose == 1):
        print '选择你要查询的学年'
        print '0、2001-2002  1、2002-2003  2、2003-2004'
        print '3、2004-2005  4、2005-2006  5、2006-2007'
        print '6、2007-2008  7、2008-2009  8、2009-2010'
        print '9、2010-2011  10、2011-2012 11、2012-2013'
        print '12、2013-2014'

        yearchoose = raw_input('> ')
        yearchoose = int(yearchoose)

        if(yearchoose not in range(13)):
            print '选择错误，请重新选择'
            info = []
            continue

        info.append(year[yearchoose])

    if(choose == 0):
        print '请选择你要查询的学期'
        print '0、第一学期  1、第二学期  2、第三学期'

        termchoose = raw_input('> ')
        termchoose = int(termchoose)

        if(termchoose not in range(3)):
            print '选择错误，请重新选择'
            info = []
            continue

        info.append(termchoose + 1)
    
    if choose in range(6):
        
        while flagcxlogin == 0:
            wait = 1
            try:
                userinfo = cxcore.cxcore(conf.username,conf.password)
                flagcxlogin = 1
            except:
                if wait <= cxfail :
                    print '由于网络的原因，连接失败，%d秒后重试' % wait
                    time.sleep(wait)
                    wait <<= 1
                else:
                    print '连接超时，正在退出'
                    exit(-1)
            
        userinfo.user_query(info)
    
    else:
        course = []
        xkfail = 128
        serviter = 0
        while flagxklogin == 0:
            wait = 1
            try:
                serverlist = conf.xkserver.split('|')
                serviter = serviter % len(serverlist)
                xkinfo = xkcore.xkcore(conf.username,conf.password,None,serverlist[serviter])
                print '%s ： 登录成功' % serverlist[serviter]
                flagxklogin = 1
            except:
                if xkfail :
                    print '由于网络的原因，连接失败，%d秒后重试' % wait
                    time.sleep(wait)
                    xkfail -= 1
                    serviter += 1
                else:
                    print '连接超时，正在退出'
                    exit(-1)
        coursechoose = 0
        while coursechoose != -1:
            
            try:
                coursenum = xkinfo.show_course()
            except:
                continue

            print '请输入你要选择的课程，-1为开始选课'
            coursechoose = raw_input('>')
            
            try:
                coursechoose = int(coursechoose)
            except:
                print '你的输入错误，即将退出'
                coursechoose = -1
                continue
            
            if coursechoose == -1:
                break

            if coursechoose not in range(coursenum):
                print '你的输入错误，即将退出'
                coursechoose = -1;
                continue
            
            
            teacherinfo = xkinfo.show_teacher(coursechoose);

            print '请输入你要选择的老师'
            teacherchoose = raw_input('>')

            try:
                teacherchoose = int(teacherchoose)
            except:
                print '输入无效，请重新选择课程'
                continue

            coursetuple = (coursechoose,teacherinfo[teacherchoose][0])
            course.append(coursetuple)
        
        print '选课开始，请耐心等待'
        xkinfo.go(course)
        print '选课完成'

    info = []
