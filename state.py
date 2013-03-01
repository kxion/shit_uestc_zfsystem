#-*-coding:utf-8-*-

default_year='2012-2013'
year = {'0':'2001-2002','1':'2002-2003','2':'2003-2004','3':'2004-2005','4':'2005-2006','5':'2006-2007','6':'2007-2008','7':'2008-2009','8':'2009-2010','9':'2010-2011','10':'2011-2012','11':'2012-2013','12':'2013-2014'}

#状态机
class StateMachine(object):

    def __init__(self,user):
        #原始状态
        self.states={
            '0':self.grade,
            '1':self.chart, 
            '2':self.exam,
            '3':self.level,
            '4':self.exit,
            '5':self.execute
        }
        self.userinfo=user
        

    def run(self,init):
        return self.states.get(init,self.exit)()


    #成绩查询
    def grade(self):
        #next states
        ns={
            '0':self.sem_grade,
            '1':self.year_grade, 
            '2':self.all_grade,
            '3':self.restart
        }
        print "选择学期成绩或学年成绩"
        print "0、学期成绩  1、学年成绩  2、历年成绩  3、返回顶级"
        choice= raw_input("> ")
        return ns.get(choice,self.dead)()

    #学期成绩
    def sem_grade(self,info=[]):
        
        if info!=[]:
            self.userinfo.user_query(info)
            return 'r'
        
        y=year.get(self.get_year(),default_year)
        print '请选择你要查询的学期'
        print '0、第一学期  1、第二学期  2、第三学期'
        termchoose=raw_input('> ')

        try: termchoose=int(termchoose)
        except:
            return self.dead("不是数字")

        if termchoose in range(3):
            info=[0,y,termchoose+1]
        else:
            print "输入错误重新选择"
        
        return self.sem_grade(info)
        
    #学年成绩
    def year_grade(self,info=[]):
        if info!=[]:
            self.userinfo.user_query(info)
            return 'r'
        
        y=year.get(self.get_year(),default_year)
        info=[1,y]
 
        return self.year_grade(info)
        
        
    #历年成绩
    def all_grade(self):
        self.userinfo.user_query([2])
        return 'r'
        


    #课表查询
    def chart(self):
        self.userinfo.user_query([3])
        return 'r'
    
    #考试查询
    def exam(self):
        self.userinfo.user_query([4])
        return 'r'

    #等级考试查询
    def level(self):
        self.userinfo.user_query([5])
        return 'r' 




    #Ok
    def restart(self):
        return 'r'

    #Error
    def dead(self,info=''):
        print "输入异常，退出"
        if info !='':
            print '原因:',info
        return 'q'

    #Exit
    def exit(self):
        return 'q'
    
    



    #Public 选择学年
    def get_year(self):
        print '选择你要查询的学年'
        print '0、2001-2002  1、2002-2003  2、2003-2004'
        print '3、2004-2005  4、2005-2006  5、2006-2007'
        print '6、2007-2008  7、2008-2009  8、2009-2010'
        print '9、2010-2011  10、2011-2012 11、2012-2013'
        print '12、2013-2014'

        yearchoose = raw_input('> ')
        return yearchoose



    def execute(self):
        self.userinfo.open()
        

