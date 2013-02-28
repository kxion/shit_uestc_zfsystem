#-*- coding=utf-8 -*-

import core
import getpass

flag = 'r'
info = []
year = ['2001-2002','2002-2003','2003-2004','2004-2005','2005-2006','2006-2007','2007-2008','2008-2009','2009-2010','2010-2011','2011-2012','2012-2013','2013-2014']

print '请输入你的学号'
username = raw_input('> ')
print '请输入你的密码'
password = getpass.getpass('> ')

userinfo = core.cxcore(username,password)

while(flag == 'r'):
    
    print '选择你所需要的功能：'
    print '0、学期成绩  1、学年成绩  2、历年成绩  3、学生课表查询'
    print '4、学生考试查询  5、等级考试查询  6、退出'
    choose = raw_input('> ')
    choose = int(choose)
    if(choose not in range(6)):
        if(choose != 6):
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
    
    userinfo.user_query(info)
    info = []
