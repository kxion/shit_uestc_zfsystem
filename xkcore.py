#!/usr/bin/env python
#coding=utf-8

import re
import urllib
import urllib2
import cookielib
import time
import threading

class xkcore:

    __cookie = cookielib.CookieJar()
    __loginheader = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'en-US,en;q=0.8','Cache-Control':'max-age=0','Connection':'keep-alive','Host':'','Referer':'','User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.12 Safari/537.31'}
    

    def __init__(self,username,password,useropt,serveraddr):
        self.__username = username
        self.__password = password
        self.__useropt = useropt
        self.__serveraddr = serveraddr
        self.__loginheader['HOST'] = self.__serveraddr
        self.__loginheader['Referer'] = self.__serveraddr+'/default_ldap.aspx'
        self.__loginurl = 'http://'+self.__serveraddr+'/default_ldap.aspx'
        self.__infourl = 'http://'+self.__serveraddr+'/xs_main_zzjk.aspx?xh='+self.__username
        self.__login()

    def __login(self):
        
        tmpcontent = urllib2.urlopen(self.__loginurl).read().decode('gb2312').encode('utf-8')
        tmpviewstate = re.search('name="__VIEWSTATE" value="([^"]+)"',tmpcontent).group(1)
        
        tmpdata = {'__VIEWSTATE':tmpviewstate,'tbYHM':self.__username,'tbPSW':self.__password,'Button1':' 登 录 '.decode('utf-8').encode('gb2312')}
        tmpdata = urllib.urlencode(tmpdata)
        tmpopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie))
        tmpreq = urllib2.Request(self.__loginurl,tmpdata,self.__loginheader)
        tmpopener.open(tmpreq,tmpdata)

        tmpcontent = tmpopener.open(self.__infourl).read().decode('gb2312').encode('utf-8')
        tmpaddr = re.search('href="(xsxk.aspx\?xh=[^"]+)',tmpcontent).group(1)
        self.__xkurl = 'http://'+self.__serveraddr+'/'+tmpaddr
        self.__xkurl = self.__xkurl.decode('utf-8').encode('gb2312')

        
    def show_course(self):
        
        self.__infoheader = self.__loginheader
        self.__infoheader['Referer'] = self.__infourl
        
        tmpopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie))
        tmpreqhandle = urllib2.Request(self.__xkurl,None,self.__infoheader)
        tmpcontent = tmpopener.open(tmpreqhandle,None).read().decode('gb2312').encode('utf-8')
        tmpviewstate = re.search('name="__VIEWSTATE" value="([^"]+)"',tmpcontent).group(1)
        

        tmpdata = {'__EVENTTARGET':'','__EVENTARGUMENT':'','__VIEWSTATE':tmpviewstate,'DrDl_Nj':'2010','zymc':'0201电子信息工程主修专业'.decode('utf-8').encode('gb2312'),'Button5':'本专业选课'.decode('utf-8').encode('gb2312')}
        tmpdata = urllib.urlencode(tmpdata)
        self.__infoheader['Referer'] = self.__xkurl
        tmpreqhandle = urllib2.Request(self.__xkurl,tmpdata,self.__infoheader)
        tmpcontent = tmpopener.open(tmpreqhandle,tmpdata).read().decode('gbk').encode('utf-8')

        
        self.__course = re.findall('onclick="window.open\(\'xsxjs.aspx\?xkkh=([^&]+)&xh='+self.__username+'\',\'xsxjs\',\'toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=1\'\)">([^<]+)</a>',tmpcontent)
        tmppage = re.findall('<a href="javascript:__doPostBack\(\'([^\']+)\',\'([^\']?)\'\)">',tmpcontent)
        tmpviewstate = re.search('name="__VIEWSTATE" value="([^"]+)"',tmpcontent).group(1)
        
        
        for iterator in range(len(tmppage)):
            tmptarget = ':'.join(tmppage[iterator][0].split('$'))
            tmpargument = tmppage[iterator][1]
            tmpdata = {'__EVENTTARGET':tmptarget,'__EVENTARGUMENT':tmpargument,'__VIEWSTATE':tmpviewstate,'zymc':   '0201电子信息工程主修专业||2010'.decode('utf-8').encode('gb2312'),'xx':''}
            tmpdata = urllib.urlencode(tmpdata)
            tmpreqhandle = urllib2.Request(self.__xkurl,tmpdata,self.__infoheader)
            tmpcontent = tmpopener.open(tmpreqhandle,tmpdata).read().decode('gbk').encode('utf-8')
            tmpcourse = re.findall('onclick="window.open\(\'xsxjs.aspx\?xkkh=([^&]+)&xh='+self.__username+'\',\'xsxjs\',\'toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=1\'\)">([^<]+)</a>',tmpcontent)
            self.__course = self.__course + tmpcourse
        
        
        for iterator in range(len(self.__course)):
            if iterator%2 == 0:
                print "%d" % (iterator//2),
                print '、课程编号:'+self.__course[iterator][1]+'   ',
            else:
                print '课程名称:'+self.__course[iterator][1]

        return len(self.__course)/2
    
    
    def __get_courseurl(self):

        self.__courseurl = []

        for iterator in range(len(self.__course)):
            if iterator % 2 == 0:
                self.__courseurl.append('http://'+self.__serveraddr+'/xsxjs.aspx?xkkh='+self.__course[iterator][0]+'&xh='+self.__username)


    def show_teacher(self,parmcourse):
        
        self.__viewflag = 0
        self.__get_courseurl()
        
        tmpopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie))
        tmpreqhandle = urllib2.Request(self.__courseurl[parmcourse],None,self.__infoheader)
        tmpcontent = tmpopener.open(tmpreqhandle,None).read().decode('gb2312').encode('utf-8')

        tmpcourseinfo = re.findall('onclick="window.open\(\'jsxx.aspx\?xh='+self.__username+'&xkkh=([^&]+)&amp;jszgh=([^\']+)\',\'jsxx\',\'toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=0\'\)" href="#" >([^<]+)</A>',tmpcontent)
        

        if self.__viewflag == 0 :
            tmptime = 1
            while self.__viewflag == 0:
                try:
                    self.__xkviewstate = re.search('name="__VIEWSTATE" value="([^"]+)"',tmpcontent).group(1)
                except:
                    time.sleep(tmptime)
                    tmptime <<= 1
                    continue
                
                self.__viewflag = 1

        for iterator in range(len(tmpcourseinfo)):
            print iterator,
            print '、 课程编号:'+tmpcourseinfo[iterator][0]+'   ',
            print '上课教师:'+tmpcourseinfo[iterator][2]

        return tmpcourseinfo
    
    def __threading_go(self,parmurl,parmdata,parmid,parmcount):
        
        tmptarget = ':'.join('Button1'.split('$'))
        tmpdata = {'__EVENTTARGET':tmptarget,'__EVENTARGUMENT':'','__VIEWSTATE':self.__xkviewstate,'xkkh':parmdata}
        tmpdata = urllib.urlencode(tmpdata)

        tmpcourseurl = 'http://'+self.__serveraddr+'/xsxjs.aspx?xkkh='+parmurl+'&xh='+self.__username
        self.__infoheader['Referer'] = tmpcourseurl
        
        tmpopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie))
        tmpreqhandle = urllib2.Request(tmpcourseurl,tmpdata,self.__infoheader)
        
        stopflag = True
        while parmcount and stopflag :
            
            parmcount = parmcount - 1

            tmpcontent = tmpopener.open(tmpreqhandle,tmpdata).read().decode('gb2312').encode('utf-8')
            
            tmpre = re.search('五秒防刷',tmpcontent)
            if tmpre != None:
                sleep(6)
                continue
            
            tmpre = re.search('人数超过限制',tmpcontent)
            if tmpre != None:
                print "%d号课程人数超过限制，正在等待" % parmid
                time.sleep(1)
                continue
           
            tmpre = re.search('现在不是选课时间',tmpcontent)
            if tmpre != None:
                print "现在不是选课时间，正在等待"
                time.sleep(1)
                continue

            tmpre = re.search('上课时间冲突',tmpcontent)
            if tmpre != None:
                print "%d号课程上课时间冲突" % parmid
                stopflag = False
                continue
            
            tmpre = re.search('保存成功',tmpcontent)
            if tmpre != None:
                print "恭喜你，%d号课程保存成功" % parmid
                stopflag = False
                continue

            stopflag = False
        self.__threadcnt -= 1


    def go(self,parmcourse):
        
        self.__threadcnt = 0
        tmpitemlist = []

        for item in parmcourse:
            
            tmpthreadlist = []

            tmpthreadlist.append(threading.Thread(group=None,target=self.__threading_go,name=self.__course[item[0]*2+1][0],args=(self.__course[item[0]*2+1][0],item[1],item[0],65535)))
            
            self.__threadcnt += 1

            for tmpthreaditem in tmpthreadlist:
                tmpthreaditem.start()
            
        while self.__threadcnt:
            for tmpthreaditem in tmpthreadlist:
                tmpthreaditem.join(0)
            time.sleep(1)
            

