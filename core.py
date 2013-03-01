#!/usr/bin/env python
#coding=utf-8

import re
import cookielib
import urllib
import urllib2
import webbrowser
import os

class cxcore:
    __root_url = 'http://ea.uestc.edu.cn'
    __login_url = 'http://portal.uestc.edu.cn/userPasswordValidate.portal'
    __query_url = 'http://ea.uestc.edu.cn/default_zzjk.aspx'
    __login_header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3','User-Agent':'Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.12 Safari/537.31','Content-Type':'application/x-www-form-urlencoded','Connection':'keep-alive','HOST':'portal.uestc.edu.cn','Referer':'http://portal.uestc.edu.cn'}
    __cookie = cookielib.CookieJar()

    def __init__(self,username,password):
        
        self.__username = username
        self.__password = password
        self.__login_data = {'userName':self.__username,'password':self.__password,'btn':'登录'}
        self.__login_data = urllib.urlencode(self.__login_data)
        self.__login()
        print '登录成功'

    def __login(self):

        tmpopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie))
        tmpreqhandle = urllib2.Request(self.__login_url,self.__login_data,self.__login_header)
        tmpopener.open(tmpreqhandle,self.__login_data)
        self.__tmpcontent = tmpopener.open(self.__query_url).read().decode('gb2312').encode('utf-8')
        tmpornot = re.search('"xscjcx.aspx\?([^"]+)"',self.__tmpcontent)
        if(tmpornot == None):
            print '学号或密码错误'
            exit(0)

    def __cjcx_query(self,info):
        
        
        self.__cjcx_data = {'__EVENTTARGET':'','__EVENTARGUMENT':'','hidLanguage':'','ddlXN':'','ddlXQ':'','ddl_kcxz':''}

        tmpopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie))
        tmpreqhandle = urllib2.Request(self.__info_url,None,self.__query_header)
        tmpcontent = tmpopener.open(tmpreqhandle,None).read().decode('gb2312').encode('utf-8')
        tmpViewstate = re.search('"__VIEWSTATE" value="([^"]+)"',tmpcontent)
        
        self.__cjcx_data['__VIEWSTATE'] = tmpViewstate.group(1)

        if(info[0] == 2):
            self.__cjcx_data['btn_zcj'] = '历年成绩'
        elif(info[0] == 1):
            self.__cjcx_data['ddlXN'] = info[1]
            self.__cjcx_data['btn_xn'] = '学年成绩'
        elif(info[0] == 0):
            self.__cjcx_data['ddlXN'] = info[1]
            self.__cjcx_data['ddlXQ'] = info[2]
            self.__cjcx_data['btn_xq'] = '学期成绩'
        
        self.__cjcx_data = urllib.urlencode(self.__cjcx_data)

        tmpopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie))
        tmpreqhandle = urllib2.Request(self.__info_url,self.__cjcx_data,self.__query_header)
        tmpcontent = tmpopener.open(tmpreqhandle,self.__cjcx_data).read()

        tmpfp = open('shit_zf_cjcx_local.html','w')
        tmpfp.write(tmpcontent)
        tmpfp.close()

        print 'shit_zf_cjcx_local.html已经保存到当前目录下'
    
    
    def __ifcx_query(self,filename):

        tmpopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie))
        tmpreqhandle = urllib2.Request(self.__info_url,None,self.__query_header)
        tmpcontent = tmpopener.open(tmpreqhandle,None).read()

        
        self.save(filename,tmpcontent)

    
    def user_query(self,info):
        
        self.__query_header = self.__login_header
        self.__query_header['HOST'] = self.__root_url
        self.__query_header['Referer'] = 'http://'+self.__root_url+'/xs_main_zzjk1.aspx?xh='+self.__username+'&type=1'

        if(info[0] in [0,1,2]):
            
            tmpregurl = re.search('"xscjcx.aspx\?([^"]+)"',self.__tmpcontent)
            self.__info_url = 'http://'+self.__root_url+'/xscjcx.aspx?'+tmpregurl.group(1)
            self.__info_url = self.__info_url.decode('utf-8').encode('gb2312')
            self.__cjcx_query(info)

        elif(info[0] == 3):
            
            tmpregurl = re.search('"xskbcx.aspx\?([^"]+)"',self.__tmpcontent)
            self.__info_url = 'http://'+self.__root_url+'/xskbcx.aspx?'+tmpregurl.group(1)
            self.__info_url = self.__info_url.decode('utf-8').encode('gb2312')
            self.__ifcx_query('shit_zf_kbcx_local.html')

        elif(info[0] == 4):
            
            tmpregurl = re.search('"xskscx.aspx\?([^"]+)"',self.__tmpcontent)
            self.__info_url = 'http://'+self.__root_url+'/xskscx.aspx?'+tmpregurl.group(1)
            self.__info_url = self.__info_url.decode('utf-8').encode('gb2312')
            self.__ifcx_query('shit_zf_kscx_local.html')

        elif(info[0] == 5):
            
            tmpregurl = re.search('"xsdjkscx.aspx\?([^"]+)"',self.__tmpcontent)
            self.__info_url = 'http://'+self.__root_url+'/xsdjkscx.aspx?'+tmpregurl.group(1)
            self.__info_url = self.__info_url.decode('utf-8').encode('gb2312')
            self.__ifcx_query('shit_zf_djks_local.html')

    def save(self,filename,content):
        content=self.get_style(content)
        tmpfp = open(filename,'w')
        tmpfp.write(content)
        tmpfp.close()
        
        browser=raw_input("是否用浏览器打开?(y/n)\n")
        if browser=='Y' or browser=='y':
            path=os.path.abspath(filename)
            webbrowser.open_new_tab('file://'+path)
        else:
            print filename+'已经保存到当前目录下'
    
    #save stylesheet
    def get_style(self,content):
        suffix={'css':[],'gif':[],'jpg':[],'js':[],'ico':[]}
        src=[]

        for i,a in suffix.items():
            suffix[i]=re.findall('href="([^"]+\.'+i+')',content)
            
            src+=suffix.get(i)
        
        
        self.download(src)

        for i in src:
            content=re.sub(i,'tmp/'+i,content)

        s2=self.get_inside_css(suffix.get("css"))
        self.download(s2)


        
        
        return content
    
    def get_inside_css(self,css):
        src=[]
        for i in css:
            p='tmp/'+i
            try:content=open(p)
            except:
                print "exception"
                continue
            content=content.read()
            tmpsrc=re.findall('url\(([^\)]+)',content)
            prefix='/'.join(i.split('/')[:-1])
            for j in tmpsrc:
                #TODO  my have problem when j is like "/base.css"
                
                src.append(prefix+'/'+j)
        return src
            

    def download(self,li):
        for i in li:
            try:s=urllib2.urlopen('http://'+self.__root_url+'/'+i)
            except:
                continue
            data=s.read()
            path='tmp/'+i
            directory='/'.join(path.split('/')[:-1])
            if os.path.exists(directory) != True:
                os.makedirs(directory)
            if os.path.exists(path) !=True:
                with open(path,"wb") as f:
                    f.write(data)
            s.close()
        
