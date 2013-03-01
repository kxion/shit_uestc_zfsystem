#!/usr/bin/env python
#coding=utf-8

import re
import os
import urllib
import urllib2
import cookielib
import webbrowser

class cxcore:
    
    __root_host= 'ea.uestc.edu.cn'
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
        
        self.__save('shit_zf_cjcx_local.html',tmpcontent)

    def __ifcx_query(self,filename):

        tmpopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie))
        tmpreqhandle = urllib2.Request(self.__info_url,None,self.__query_header)
        tmpcontent = tmpopener.open(tmpreqhandle,None).read()
        
        self.__save(filename,tmpcontent)
    
    def user_query(self,info):
        
        self.__query_header = self.__login_header
        self.__query_header['HOST'] = self.__root_host
        self.__query_header['Referer'] = 'http://'+self.__root_host+'/xs_main_zzjk1.aspx?xh='+self.__username+'&type=1'

        if(info[0] in [0,1,2]):
            
            tmpregurl = re.search('"xscjcx.aspx\?([^"]+)"',self.__tmpcontent)
            self.__info_url = 'http://'+self.__root_host+'/xscjcx.aspx?'+tmpregurl.group(1)
            self.__info_url = self.__info_url.decode('utf-8').encode('gb2312')
            self.__cjcx_query(info)

        elif(info[0] == 3):
            
            tmpregurl = re.search('"xskbcx.aspx\?([^"]+)"',self.__tmpcontent)
            self.__info_url = 'http://'+self.__root_host+'/xskbcx.aspx?'+tmpregurl.group(1)
            self.__info_url = self.__info_url.decode('utf-8').encode('gb2312')
            self.__ifcx_query('shit_zf_kbcx_local.html')

        elif(info[0] == 4):
            
            tmpregurl = re.search('"xskscx.aspx\?([^"]+)"',self.__tmpcontent)
            self.__info_url = 'http://'+self.__root_host+'/xskscx.aspx?'+tmpregurl.group(1)
            self.__info_url = self.__info_url.decode('utf-8').encode('gb2312')
            self.__ifcx_query('shit_zf_kscx_local.html')

        elif(info[0] == 5):
            
            tmpregurl = re.search('"xsdjkscx.aspx\?([^"]+)"',self.__tmpcontent)
            self.__info_url = 'http://'+self.__root_host+'/xsdjkscx.aspx?'+tmpregurl.group(1)
            self.__info_url = self.__info_url.decode('utf-8').encode('gb2312')
            self.__ifcx_query('shit_zf_djks_local.html')

    
    def __save(self,filename,content):
        
        content=self.__get_style(content)
        tmpfp = open(filename,'w')
        tmpfp.write(content)
        tmpfp.close()
        
        browser=raw_input("是否用浏览器打开?(y/n)\n")
        if browser=='Y' or browser=='y':
            path=os.path.abspath(filename)
            webbrowser.open_new_tab('file://'+path)
        else:
            print filename+'已经保存到当前目录下'
    
    def __get_style(self,content):
        
        suffix={'css':[],'gif':[],'jpg':[],'js':[],'ico':[],'png':[],'jpeg':[]}
        
        for suffixkey in suffix.keys():
            tmpfilelist = re.findall('href="([^"]+\.'+suffixkey+')',content)
            suffix[suffixkey] = tmpfilelist
            tmpfilelist = re.findall('src="([^"]+\.'+suffixkey+')',content)
            suffix[suffixkey] += tmpfilelist

            self.__download(suffix[suffixkey])
            for filename in suffix[suffixkey]:
                content = re.sub('href="'+filename+'"','href="tmp/'+filename+'"',content)
                content = re.sub('src="'+filename+'"','src="tmp/'+filename+'"',content)
        
        tmpsrc = self.__get_inside_files(suffix['css'])
        self.__download(tmpsrc)

        return content
    
    def __get_inside_files(self,css):
        
        tmpret = []
        
        for filename in css:
            tmppath = 'tmp/'+filename
            try:
                tmpfp = open(tmppath)
            except:
                continue
            
            tmpcontent = tmpfp.read()
            tmpsrc = re.findall('url\(([^\)]+)\)',tmpcontent)
            tmpdir = '/'.join(filename.split('/')[:-1])+'/'
            
            for tmpiter in range(len(tmpsrc)):
                tmpsrc[tmpiter] = tmpdir + tmpsrc[tmpiter].lstrip('/')
                
            tmpret += tmpsrc
            
        return tmpret
            

    def __download(self,filelist):
        
        for tmpfilename in filelist:
            
            try:
                tmpopen = urllib2.urlopen('http://'+self.__root_host+'/'+tmpfilename)
            except:
                continue

            tmpdata = tmpopen.read()
            tmppath = 'tmp/'+tmpfilename
            directory = '/'.join(tmppath.split('/')[:-1])

            if os.path.exists(directory) != True:
                os.makedirs(directory)
            if os.path.exists(tmppath) != True:
                tmpfp = open(tmppath,"wb")
                tmpfp.write(tmpdata)
                tmpfp.close()

