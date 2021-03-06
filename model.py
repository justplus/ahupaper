#!/usr/bin/python
# -*- coding: UTF-8 -*-
import web
import sae.const
import sae.storage
from datetime import date,time,timedelta,datetime
import sys

#数据库配置
db = web.database(dbn='mysql', user=sae.const.MYSQL_USER, pw=sae.const.MYSQL_PASS,\
host=sae.const.MYSQL_HOST, port=int(sae.const.MYSQL_PORT), db=sae.const.MYSQL_DB)

#用户登陆
def userLogin(username,userpsw):
	temp="select * from users where username='%s' and userpassword='%s'"%(username,userpsw.encode("hex"))
	result=db.query(temp)
	return result

#用户注册
def userRegister(userno,username,userpsw,useremail,userschool,userdepartment):
    temp="insert into users(username,userpassword,userno,userschool,userdepartment,useremail) values ('%s','%s','%s','%s','%s','%s')"%(username,userpsw.encode("hex"),userno,userschool,userdepartment,useremail)
    retstr=True
    try:
        db.query(temp)
    except:
        retstr=False
    return retstr

#判断cookie中用户是否合法
def isuservalid(username,useremail):
    temp="select * from users where username='%s' and useremail='%s'"%(username,useremail)
    result=db.query(temp)
    return result

#今天的日期
def get_date_today():
	td=date.today()
	if td.month<10:
		month_str="0"+str(td.month)
	else:
		month_str=str(td.month)
	if td.day<10:
		day_str="0"+str(td.day)
	else:
		day_str=str(td.day)
	return str(td.year)+"-"+month_str+"-"+day_str
	
#当前时刻
def get_now_time():
	nowtime=datetime.now()
	h=nowtime.hour
	m=nowtime.minute
	return "%s:%s"%(h,m)

#添加试卷
def insertpaper(school,department,course,pyear,term,ptype,answer,dirurl,uploader):
    ans=0
    if answer!="0":
        ans=1
    if not department:
        department='NULL'
    uploadtime="%s %s"%(get_date_today(),get_now_time())
    temp="insert into papers(school,department,course,year,term,type,answer,dirurl,uploader,uploadtime) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(school,department,course,int(pyear),int(term),int(ptype),ans,dirurl,uploader,uploadtime)
    retstr=True
    try:
        db.query(temp)
    except:
        retstr=False
    return retstr

#下载试卷
def downloadpaper(pyear,term,school,department,course,ptype,searchtype,currentpage):
    temp=''
    if searchtype=='1':
        temp="select * from papers where 1"
        if pyear!='-1':
            temp="%s and year='%s'"%(temp,pyear)
        if term!='-1':
            temp="%s and term='%s'"%(temp,term)
        if school!='NULL':
            temp="%s and school='%s' and department='%s'"%(temp,school,department)
        if course!='NULL':
            temp="%s and course='%s'"%(temp,course)
        if ptype!='5':
            temp="%s and type='%s'"%(temp,ptype)
    else:
        temp="select * from papers where 1"
        if pyear!='-1':
            temp="%s and year='%s'"%(temp,pyear)
        if term!='-1':
            temp="%s and term='%s'"%(temp,term)
        if school!='NULL':
            temp="%s and school='%s' and department='%s'"%(temp,school,department)
        if course!='NULL':
            temp="%s and upper(course) like binary concat('%%',upper('%s'),'%%')"%(temp,course)
        if ptype!='5':
            temp="%s and type='%s'"%(temp,ptype)
    tempcount=db.query('select count(*) as rc from (%s)sub'%temp)
    resultscount=tempcount[0].rc
    resultperpage=10
    if resultscount%resultperpage==0:
        pages=resultscount/resultperpage
    else:
        pages=resultscount/resultperpage+1
    offsetvalue=(currentpage-1)*resultperpage
    temp='%s limit 10 offset %s'%(temp,offsetvalue)
    queryresult=db.query(temp)
    pageargs=[]
    if pages==2:
        pageargs=[currentpage,1,2,1,2]
    elif pages>=3:
        if currentpage==1:
            pageargs=[currentpage,1,pages,1,2,3]
        elif currentpage==pages:
            pageargs=[currentpage,1,pages,pages-2,pages-1,pages]
        else:
            pageargs=[currentpage,1,pages,currentpage-1,currentpage,currentpage+1]
    retstring=''
    if not queryresult:
        retstring='<p>没有找到资源！你可以选择更改搜索条件或者<a href="/upload">上传</a>！即将推出试卷应求功能~</p>'
    else:
        if pageargs:
            #acurl='/download?downyear=%s&downterm=%s&downschool=%s&downdepartment=%s&downcourse=%s&downtype=%s&searchtype=%s&page='%(pyear,term,school,department,course,ptype,searchtype)
            retstring=u'%s<div><table class="pager"><tr><td><a href="#nogo" onclick="showResults(1)">首页</a></td>'%(retstring)
            for p in pageargs[3:]:
                #pagepurl="%s%s"%(acurl,p)
                if p==currentpage:
                    retstring='%s<td bgcolor=#99CCFF><a href="#nogo" onclick="showResults(%d)">%s</a></td>'%(retstring,p,p)
                else:
                    retstring='%s<td><a href="#nogo" onclick="showResults(%d)">%s</a></td>'%(retstring,p,p)
            #pagenurl="%s%s"%(acurl,pageargs[2])
            retstring=u'%s<td><a href="#nogo" onclick="showResults(%d)">末页</a></td>'%(retstring,pageargs[2])
            retstring='%s</tr></table></div>'%retstring
        retstring='%s<div class="helpbox">'%retstring
        for result in queryresult:
            papername=u'%s-%s 第%s学期 %s试卷'%(result.year,result.year+1,result.term,result.course)
            coursetype=getCourseType(result.type)
            if result.school=="NULL":
                retstring=u'%s<span class="helphead"><a href="%s" onclick="checkLogin();">%s</a>(%s)</span>上传者:%s&nbsp&nbsp&nbsp&nbsp上传时间:%s<br/><br/>'%(retstring,result.dirurl,papername,coursetype,result.uploader,result.uploadtime)
            else:
                retstring=u'%s<span class="helphead"><a href="%s" onclick="checkLogin();">%s</a>(%s)</span>%s&nbsp&nbsp&nbsp&nbsp%s&nbsp&nbsp&nbsp&nbsp上传者:%s&nbsp&nbsp&nbsp&nbsp上传时间:%s<br/><br/>'%(retstring,result.dirurl,papername,coursetype,result.school,result.department,result.uploader,result.uploadtime)
        retstring='%s%s'%(retstring,'</div>')
    return retstring

#搜索试卷/按照关键字
def querypaper(q):
    temp="select * from papers where upper(course) like binary concat('%%',upper('%s'),'%%') limit 10 offset 0"%q
    queryresult=db.query(temp)
    retstring=''
    if not queryresult:
        retstring='<p>没有找到资源！你可以选择更改搜索条件或者<a href="/upload">上传</a>！即将推出试卷应求功能~</p>'
    else:
        retstring='%s<div class="helpbox">'%retstring
        for result in queryresult:
            papername=u'%s-%s 第%s学期 %s试卷'%(result.year,result.year+1,result.term,result.course)
            coursetype=getCourseType(result.type)
            if result.school=="NULL":
                retstring=u'%s<span class="helphead"><a href="#nogo" onclick="checkLogin();">%s</a>(%s)</span>上传者:%s&nbsp&nbsp&nbsp&nbsp上传时间:%s<br/><br/>'%(retstring,papername,coursetype,result.uploader,result.uploadtime)
            else:
                retstring=u'%s<span class="helphead"><a href="#nogo" onclick="checkLogin();">%s</a>(%s)</span>%s&nbsp&nbsp&nbsp&nbsp%s&nbsp&nbsp&nbsp&nbsp上传者:%s&nbsp&nbsp&nbsp&nbsp上传时间:%s<br/><br/>'%(retstring,papername,coursetype,result.school,result.department,result.uploader,result.uploadtime)
        retstring='%s%s'%(retstring,'</div>')
    return retstring

#搜索试卷/按照关键字
def queryloginpaper(q):
    temp="select * from papers where upper(course) like binary concat('%%',upper('%s'),'%%') limit 10 offset 0"%q
    queryresult=db.query(temp)
    retstring=''
    if not queryresult:
        retstring='<p>没有找到资源！你可以选择更改搜索条件或者<a href="/upload">上传</a>！即将推出试卷应求功能~</p>'
    else:
        retstring='%s<div class="helpbox">'%retstring
        for result in queryresult:
            papername=u'%s-%s 第%s学期 %s试卷'%(result.year,result.year+1,result.term,result.course)
            coursetype=getCourseType(result.type)
            if result.school=="NULL":
                retstring=u'%s<span class="helphead"><a href="%s" onclick="checkLogin();">%s</a>(%s)</span>上传者:%s&nbsp&nbsp&nbsp&nbsp上传时间:%s<br/><br/>'%(retstring,result.dirurl,papername,coursetype,result.uploader,result.uploadtime)
            else:
                retstring=u'%s<span class="helphead"><a href="%s">%s</a></span>%s&nbsp&nbsp&nbsp&nbsp%s&nbsp&nbsp&nbsp&nbsp上传者:%s&nbsp&nbsp&nbsp&nbsp上传时间:%s<br/><br/>'%(retstring,result.dirurl,papername,result.school,result.department,result.uploader,result.uploadtime)
        retstring='%s%s'%(retstring,'</div>')
    return retstring

#转换课程类型
def getCourseType(i):
    if i==1:
        return u"公共基础课"
    elif i==2:
        return u"专业核心课"
    elif i==3:
        return u"专业选修课"
    else:
        return u"校公选课"

#提交评论内容
def insertcomment(commentnickname,commentemail,commentcontent):
    commenttime="%s %s"%(get_date_today(),get_now_time())
    if commentemail=="":
		commentemail="NULL"
    temp="insert into comment(nickname,Email,content,time) values ('%s','%s','%s','%s')"%(commentnickname,commentemail,commentcontent,commenttime)
    retstr=True
    try:
        db.query(temp)
    except:
        retstr=False
    return retstr

#获取最新上传试卷
def getuploadinfo():
    temp="select * from papers order by id desc limit 15 offset 0"
    result=db.query(temp)
    retarray=[]
    for r in result:
        retarray.append([r.uploader,r.uploadtime,r.dirurl,r.year,r.year+1,r.term,r.course,getCourseType(r.type)])
        #retarray.append(u'%s于%s上传了 <a href=%s>%s-%s第%s学期%s试卷(%s)</a>'%())
    return retarray

def getuserpapercount():
    temp=db.query("select count(*) as pc from papers")
    papercount=temp[0].pc
    temp=db.query("select count(*) as uc from users")
    usercount=temp[0].uc
    return [papercount,usercount]