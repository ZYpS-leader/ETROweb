from flask import Flask
app=Flask("app")
app.secret_key="!@#$%^&*()1234567890"


#* os文件处理
import os
app.config["UPLOAD_PATH"]=os.path.join(app.root_path,"uploads")


#* 外部SQL头类处理
import pymysql as sql
connect=sql.connect(host="127.0.0.1",port=3306,user="root",password="Eto20230403",charset="utf8")
cursor=connect.cursor()
cursor.execute("use etroweb");connect.commit()


from jinja2.utils import escape


#* wtforms头类处理
from wtforms import StringField, PasswordField, FileField, SubmitField, IntegerField, TextAreaField, BooleanField
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired 
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
app.config["WTF_I18N_ENABLED"]=False
app.config["MAX_CONTENT_LENGTH"]=5*1024*1024
class baseform(FlaskForm):
    class Meta:
        locales=["zh"]


class Login(baseform):
    username=StringField("Input your name:",validators=[DataRequired(message="Your name cannot be none!"),Length(6,32) ])
    password=PasswordField("Input your password:",validators=[DataRequired(message="Invalid password!"),Length(6,64) ])
    checword=PasswordField("Confirm your password:",validators=[DataRequired(),EqualTo("password")])
    #photo=FileField("Upload your photo:",validators=[FileAllowed(["jpg","png","jpeg","gif"])])
    moreinfo=StringField("Say something or your description:(Can be none)",validators=[Length(-1,320)])
    email=StringField("Input your email:",validators=[DataRequired()])
    vip_code=StringField("如果您拥有vip兑换token,请输入:(若无忽视即可)",validators=[Length(-1,32)])
    submit=SubmitField("Confirm")

class Signin(baseform):
    username=StringField("Input your name:",validators=[DataRequired(message="Your name cannot be none!"),Length(6,32)])
    password=PasswordField("Input your password:",validators=[DataRequired(message="Invalid password!"),Length(6,64)])
    submit=SubmitField("Confirm")

class Check_code(baseform):
    checkcode=StringField("We've just send an email to your email-account with a confirm code, now copy it here:",validators=[DataRequired('It must be filled!')])
    submit=SubmitField('Confirm')

class article_input(baseform):
    texthead=StringField("Name your article with a good name:",validators=[DataRequired("Name must not bu none!")])
    body=CKEditorField("write your article here:",validators=[Length(20,32767)])
    typea=BooleanField("勾选以公开使所有人可见(通过主页面)")
    typeb=BooleanField("勾选以在社区文章列表中展示")
    submit=SubmitField("Confirm")

class all_social(baseform):
    admincode=StringField("由于该操作为特殊操作,请输入管理员验证码以进行操作:")
    social_na=StringField("本次审批的社区操作码为:")
    submit=SubmitField("确认通过该社区的成立申请")


class uploadfile(baseform):
    file=FileField(u"上传文件:",validators=[FileRequired(u"不能上传空文件!")])
    submit=SubmitField(u"确定并上传")

class del_user(baseform):
    username=StringField(u"需要删除的用户:")
    submit=SubmitField(u"确认删除")

class del_arti(baseform):
    artiname=StringField(u"需要删除的文章名:")
    submit=SubmitField(u"确认删除")

class _patch_1(baseform):
    name=StringField(u"百度知道搜索关键字:",validators=[DataRequired("关键字不能为空")])
    submit=SubmitField(u"提交")

class _patch_3(baseform):
    name=StringField(u"本站token:",validators=[DataRequired("token不能为空")])
    submit=SubmitField(u"提交")

class yincai(baseform):
    name=StringField(u"你的猜测:",validators=[DataRequired("不能留空哦")])
    submit=SubmitField(u"确认")

class _patch_2(baseform):
    name=StringField(u"百度图片搜索关键字:",validators=[DataRequired("关键字不能为空")])
    times=IntegerField(u"爬取图片数量:",validators=[DataRequired("数量不能为空"),NumberRange(-1,60)])
    submit=SubmitField(u"提交")

class getvip(baseform):
    name=StringField("你也可以输入vip兑换券码来免费兑换vip:")
    submit=SubmitField("兑换")


class new_socail(baseform):
    name=StringField(u"请输入社区名称:",validators=[DataRequired("名称不能为空"),Length(6,32)])
    text=TextAreaField(u"请输入社区描述:")
    submit=SubmitField("提交申请")



import hashlib
SECRET_STRING="admin_123456"
class user_base():
    def __init__(self,name:str,password:str,email:str,code:str,admin:bool=0,if_vip:bool=0,p2times:int=3,description:str=None) -> None:
        self.name=name
        self.word=password
        self.emai=email
        self.code=code
        self.admi=admin
        self.time=get_time()
        self.vipa=if_vip
        self.shen=p2times
        if description is None or description.replace(" ","")!="" :
            self.desc="This bro doesn't leave his description..."
        else:
            self.desc=description.replace(" ","_")

    def __print__(self,admin=None) -> str:
        if admin==SECRET_STRING:
            return [self.name,self.word,self.desc,self.emai]
        else:
            return [self.name,self.desc]

    def update(self,**kwargs):
        try:
            new_name=kwargs["name"]
            self.name=new_name
            cursor.execute("update users set userid=%s where uuid=%s",(self.name,self.getid()))
        except:pass
        try:
            new_password=kwargs["password"]
            self.word=new_password
            cursor.execute("update users set password=%s where uuid=%s",(self.word,self.getid()))
        except:pass
        try:
            new_desc=kwargs["description"]
            self.desc=new_desc
            cursor.execute("update users set description=%s where uuid=%s",(self.desc,self.getid()))
        except:pass
        try:
            new_vipa=kwargs["if_vip"]
            self.admi=new_vipa
            cursor.execute("update users set if_vip=%s where uuid=%s",(self.vipa,self.getid()))
        except:pass
        try:
            t=kwargs["p2times"]
            self.admi=t
            cursor.execute("update users set p2times=%s where uuid=%s",(self.shen,self.getid()))
        except:pass
        connect.commit()
        return self

    def write_to_sql(self):
        #! 确认新账号合法且不存在时调用(内部无检测!!!)
        #* 将用户信息写入数据库
        salt,new_word=behash(self.word)
        cursor.execute("insert into users (userid,password,description,email,confirm_code,if_admin,zhuce_time,if_vip,p2times,hash_salt) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.name,new_word,self.desc,self.emai,int(self.code),self.admi,self.time,self.vipa,self.shen,salt))
        cursor.execute("insert into user_level (username,level) values (%s,%s)",(self.name,1))
        connect.commit()


    def is_valid_in(self):
        #* 合法返回真 不合法返回假
        n,p,j=self.name,self.word,self.desc
        for i in n:
            if i=="<" or i==">" or i==" " or i==";" or i=="\\" or i=="=" or i=="?" or i=="&":
                return False
        for i in p:
            if i=="<" or i==">" or i==" " or i==";" or i=="\\" or i=="=" or i=="?" or i=="&":
                return False
        if not j is None:
            for i in j:
                if i=="<" or i==">" or i==";" or i=="\\" or i=="=" or i=="?" or i=="&":
                    return False
        return True

    def login_check(self):
        #* 返回-2:账户不存在 返回-1:密码不正确 返回0:账户信息正确
        try:
            cursor.execute("select password from users where userid=%s"%self.name)
            password=cursor.fetchall()
        except:
            return -2
        if password!=self.password:
            return -1
        return 0

    def out(self):
        return  self.name,self.word,self.desc,self.emai,self.code,self.admi,self.time,

    def getid(self):
        cursor.execute("select uuid from users where userid=%s",(self.name))
        get=cursor.fetchall()
        a=get[0]
        uuid=a[0]
        return uuid

def new_times(name,nt):
    try:
        cursor.execute("update users set p2times=%s where userid=%s",(nt,name))
        connect.commit()
    except:pass

def setvip(name):
    try:
        cursor.execute("update users set if_vip=1 where userid=%s",(name))
        connect.commit()
    except:pass


def into(dic:dict):
    user=user_base(dic["name"],dic["word"],dic["emai"],dic["code"],dic["admi"],dic["desc"])
    return user


"""
    积分规则(score为总分)
    一级:level1 score0
    二级:score达到128
    三级:达到512
    四级:达到1024
    五级:达到4096
    六级:达到16384
    七级:达到65536
    八级:达到135000
    九级:达到300000
    十级:达到888888
"""

def get_level_and_score(name):
    cursor.execute("select level,score from user_level where username=%s",(name))
    try:
        answer_from_sql=cursor.fetchall()[0]
        return answer_from_sql[0],answer_from_sql[1]
    except:
        return False


def add_score(name,delta_score):
    try:
        level,score=get_level_and_score(name=name)
        score+=delta_score
        new_level=if_level(score=score)
        cursor.execute("updae user_level set level=%s,score=%s where username=%s",(new_level,score,name))
        connect.commit()
        if new_level>=7:
            setvip(name)
        return True
    except:
        return False    



def if_level(score):
    if score<128:return 1
    else:
        if score<512:return 2
        else:
            if score<1024:return 3
            else:
                if score<4096:return 4
                else:
                    if score<16384:return 5
                    else:
                        if score<65536:return 6
                        else:
                            if score<135000:return 7
                            else:
                                if score<300000:return 8
                                else:
                                    if score<888888:return 9
                                    else:return 10



class an_article():
    """
    :head:文章标题

    :body:文章主题(md格式或纯文本,传入时必须为单引号包括起来的字符串,不能是超文本格式)

    :author:作者,即users表的userid

    :_time:发布时间
    """
    def __init__(self,head,body,author,_time) -> None:
        self.head=head
        self.body=body
        self.auth=author
        self._time=_time

    def in_to_sql(self):
        filename=sjn()
        with open("files/txt/%s.txt"%filename,"w",encoding="utf8") as i:
            i.write(self.body)
        head=self.head
        self.head=head.replace(" ","_")
        try:
            cursor.execute("insert into article (head,body_place,author,_time) values (\"%s\",\"%s\",\"%s\",\"%s\")"%(self.head,filename,self.auth,self._time))
            connect.commit()
        except sql.err.IntegrityError:
            return """已存在同名文章.<a href="/">点我返回首页</a>.如果您希望仍然使用该文章,我们建议您返回上一页从而修改文章名."""

def write_to_sql(n,w,d,e,c,a,v,t):
    #! 确认新账号合法且不存在时调用(内部无检测!!!)
    #* 将用户信息写入数据库
    this_user=user_base(n,w,e,c,a,v,t,d)
    this_user.write_to_sql()


#* mail邮件处理
import smtplib as smtl
from email.mime.multipart import MIMEMultipart as mmmlt
from email.mime.text import MIMEText as mmtt
from email.header import Header
import json
with open(".json") as secret:
    secrets=json.load(secret) 
def send_email(addr,yanzm):
    connect1=smtl.SMTP_SSL("smtp.163.com",465)
    connect1.login("ETRO_gfyx@163.com",secrets["email key"])
    youjian=mmmlt()
    youjian["Subject"]=Header("ETRO网站的验证码",charset="utf-8").encode()
    youjian["To"]=addr
    youjian["From"]="ETRO_gfyx@163.com"
    text="""
            <h2>验证码</h2>
            您刚刚在我们的网站(etrowebsite.com)上用您的邮箱请求了验证码.如果这并非您的本人操作,请忽略本封邮件.它可能由于某人误输入了您的邮箱.如果这确实是您所请求的内容,现献上您的验证码:<br>
            <h3>%s</h3>
            该验证码永久有效,但无法再次获取.这意味着任何人(包括您自己)再也无法用您目前所在的邮箱来注册我们的账号.这是出于对您和我们的安全考虑.由此带来的不便敬请谅解.<br>
            如果您希望再次获取验证码,请联系ETRO_omega@outlook.com.他是我们网站的管理员.请向他发送邮件,其中请包括以下内容:
            <ul>
                 <li>上述的验证码(用于核查邮箱)</li>
                 <li>验证您的身份的信息(如ETRO组内名称等)</li>
                 <li>您申请二次验证的原因</li>
                 <li>您大致的首次登录时间</li>
                 <li>其他可能需要的信息</li>
            </ul>
            如果申请通过,不出意外的话,您目前所在邮箱将很快收到回信.
            <br><br><br><br><br>
            ETRO网络部 omega
            """%(str(yanzm))
    youjian.attach(mmtt(text,"html",_charset="utf-8"))
    connect1.sendmail('ETRO_gfyx@163.com',addr, youjian.as_string())
    connect1.quit()


import random
def sjs():
    s=""
    for _ in range(6):
        s=s+str(random.randint(0,9))
    return s

def sjn():
    codes=["a","b","c","d","e","f","1","2","3","4","5","6","7","8","9","0"]
    result=""
    for _ in range(0,32):
        i=random.randint(0,15)
        result+=codes[i]
    return result

import time
def get_time():
    timestamp = time.time()
    localTime = time.localtime(timestamp)
    return time.strftime("%Y/%m/%d/ %H:%M:%S", localTime)

debug=True
def logst(from_,body,level=1):
    lj=""
    for _ in range(5,25-len(from_)):
        lj+="-"
    type_=""
    if from_!="101.224.7.145":
        if level==1:
            type_="INFO-"
        elif level==2:
            type_="QUES-"
        elif level==3:
            type_="WARN-"
        elif level==4:
            type_="ERROR"
            mk_err(from_,body)
        else:
            type_="ELSE-"
    elif not debug:return
    else:
        if level==4:
            mk_err(from_,body)
            type_="ERROR"
        elif level==3:
            type_="WARN-"
        else:
            type_="DEBUG"
    time_=get_time()
    try:
        with open("P:\\ETRO.web\\project\\logging\\loggings-%s.log"%(time_[0:10].replace("/","-")),"a",encoding="utf8") as loga:
            loga.write("[%s]-%s-------FROM:%s%sBODY:%s\n"%(time_,type_,from_,lj,body))
    except:
        with open("P:\\ETRO.web\\project\\logging\\loggings-%s.txt"%(time_[0:10].replace("/","-")),"w",encoding="utf8") as loga:
            loga.write("[%s]-%s-------FROM:%s%sBODY:%s\n"%(time_,type_,from_,lj,body))
        os.rename("P:\\ETRO.web\\project\\logging\\loggings-%s.txt"%(time_[0:10].replace("/","-")),r"logging/loggings-%s.log"%(time_[0:10]))

def mk_err(from_,aerrno):
    lj=""
    for _ in range(5,25-len(from_)):
        lj+="-"
    with open("errors.err","a",encoding="utf8") as mk_error:
        mk_error.write("[%s]---FROM:%s%sERROR:%s\n"%(get_time(),from_,lj,aerrno))


import requests
def search(i:str)->str :
    url = "https://baike.baidu.com/item/"+i
    r = requests.get(url)
    html_code = r.content.decode(r.encoding)
    hc=html_code
    with open("new.txt","w",encoding="utf-8") as h:
      h.write(str(hc))
    with open("new.txt","r",encoding="utf-8") as n:
      real=n.readlines()
    get=real[10]
    text=get[34:-3]
    os.remove("new.txt")
    return escape(text)


import re
from urllib import parse
from shutil import make_archive as mka
class ImageSpider(object):
    def __init__(self):
        self.url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={}{}'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        self.word_parse = ''
        self.i = 1  #添加计数

    # 获取图片递归函数
    def getimage(self,url,word,times):
        res= requests.get(url,headers=self.headers)
        res.encoding="utf-8"
        html=res.text
        pattern = re.compile('"hoverURL":"(.*?)"',re.S)
        img_link_list = pattern.findall(html)
        directory ='files/temps/%s'%word
        if not os.path.exists(directory):
            os.makedirs(directory)

        for img_link in img_link_list:
            filename = '{}/{}_{}.jpg'.format(directory, word, self.i)
            self.save_image(img_link,filename)
            self.i += 1
            if self.i == times:
                return 0

    # 保存图片
    def save_image(self,img_link,filename):
        html = requests.get(url=img_link,headers=self.headers).content
        with open(filename,'wb') as f:
            f.write(html)

    # 执行函数
    def run(self,word,times):
        self.word_parse = parse.quote(word)
        url = self.url.format(self.word_parse,'&pn=0')
        self.getimage(url,word,times+1)
        name=sjn()
        mka('files/temps/zips/%s'%name,'zip','files/temps/%s'%word)
        return name



def behash(_old:str):
    salt=sjn()
    new=_old+salt
    password=hashlib.sha256(new.encode()).hexdigest()
    return salt,password


def newhah(salt:str,old:str):
    l=old+salt
    return hashlib.sha256(l.encode()).hexdigest()



import statsmodels.api as sm
import pandas as pd
import numpy as np
def stats_predict(path,x:float,mode=0):      
    la=pd.read_csv(path,usecols=['特征组'] )
    lb=pd.read_csv(path,usecols=["目标组"]) 
    la1=list(la["特征组"])
    lb1=list(lb["目标组"])
    X=la1
    Y=lb1
    if mode==0:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.sin(X),np.tan(X),np.cos(X)  ))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.sin(x),np.tan(x),np.cos(x)])
    elif mode==1:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.sin(X)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.sin(x) ])
    elif mode==2:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4)])   
    elif mode==3:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,5)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,5)])   
    elif mode==4:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,5),np.power(X,6)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,5),np.power(X,6)])   
    elif mode==5:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,5),np.power(X,6),np.power(X,7)])   
    elif mode==6:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8)])   
    elif mode==7:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9)]) 
    elif mode==8:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9),np.power(X,10)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9),np.power(X,10)])   
    elif mode==9:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9),np.power(X,10),np.power(X,11)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9),np.power(X,10),np.power(X,11)])   
    elif mode==10:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9),np.power(X,10),np.power(X,11),np.power(X,12)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9),np.power(X,10),np.power(X,11),np.power(X,12)]) 
    a1=p1;a2=p2                                             
    try:
        p=p2[0]
        p=list(p)
        p0=p[0]
        sum0=0
        for i in p0:
            sum0=sum0+i
        p2=sum0/len(p0)
    except:
        p1=a1
        p2=a2
    return p1,p2
