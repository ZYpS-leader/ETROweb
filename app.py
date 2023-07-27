#-*- utf8 -*-
#TODO: 待办事项集合列表
#TODO: 6.博客分页系统
#TODO: 7.勋章系统
#TODO：*：离线聊天室
""" 
    离线聊天室
    1.32个不同频道
    2.可用StringField随时输入
    3.输入的内容将 time_,author,key(sjn产生对应键值)存入SQL,
        将key和text以纯文本形式放在对应的频道聊天室txt里.
    4.进入聊天室时取出最后128条消息并展示,底部是输入框
    5.按15s一次轮询刷新内容
"""
#TODO: 8.在线聊天室
#TODO: 9.用户社区
#TODO: 10.
from pymysql.converters import escape_string as est
from threading import Thread
from flask_ckeditor import CKEditor
from flask import (
    Flask,
    render_template,
    flash, redirect,
    url_for,
    Markup,
    request,
    abort,
    session,
    send_file,
    )
from forms import (
    sjn,
    sjs,
    get_time,
    send_email,
    user_base,
    del_arti,
    del_user,
    uploadfile,
    article_input,
    Check_code,
    Signin,
    Login,
    cursor,
    connect,
    logst,
    write_to_sql,
    new_times,
    search,
    _patch_1,
    _patch_2,
    _patch_3,
    new_socail,
    all_social,
    getvip,
    setvip,
    ImageSpider,
    yincai,
    newhah,
    get_level_and_score,
    add_score
    )
from shutil import rmtree 
spider=ImageSpider()
app=Flask("app")

ckeditor=CKEditor(app)
import json
with open(".json") as secret:
    secrets=json.load(secret) 
vipcodes=secrets["vipcodes"]
admincodes=secrets["admincodes"]
app.secret_key=secrets["secret key"]
#* os文件处理
import os
app.config["UPLOAD_PATH"]=os.path.join(app.root_path,"uploads")
app.config["WTF_I18N_ENABLED"]=False
app.config["MAX_CONTENT_LENGTH"]=5*1024*1024

 

#* 根路由 /
@app.route("/")
def index():
    from_=request.headers["X-Real-Ip"]
    body_="进入了主界面"
    logst(from_=from_,body=body_)
    if "logged-in" in session and not session["admin"]:
        return render_template("main_in.html",i=session['to_up2'])
    elif "logged-in" in session and session["admin"]:
        return render_template("main_in_admin.html",i=session['to_up2'])
    else:
        return render_template("main.html")

#* 招募界面 /join_us
@app.route("/join_us")
def join_us():
    from_=request.headers["X-Real-Ip"]
    body_="进入了join_us界面"
    logst(from_=from_,body=body_)
    return """<a href="/">Return</a><br>Our Email: ETRO_gfyx@163.com<br>Or you can contact with me(ETRO.omega) by ETRO_omega@outlook.com"""


#* 创建新账户(输入信息界面)
@app.route("/signup1",methods=["GET","POST"])
def signup():
    form=Login()
    from_=request.headers["X-Real-Ip"]
    body_="尝试创建账户"
    logst(from_=from_,body=body_)
    if form.validate_on_submit():
        from_=request.headers["X-Real-Ip"]
        body_="在创建账户界面提交了请求"
        logst(from_=from_,body=body_)
        username=form.username.data
        password=form.password.data
        moreinfo=form.moreinfo.data
        emaiaddr=form.email.data
        ifhisvip=form.vip_code.data
        checkcode0=sjs()
        cursor.execute("select uuid from users where userid=%s",username)
        answer=cursor.fetchall()
        cursor.execute("select uuid from users where email=%s",str(emaiaddr))
        result=cursor.fetchall()
        if len(answer)==0 and len(result)==0:
            new_user=user_base(str(username),str(password),str(emaiaddr),checkcode0,description=str(moreinfo))
            if new_user.is_valid_in():
                t=Thread(target=send_email,args=(emaiaddr,checkcode0))
                t.start()
                session["to_up2"]=username
                session["stdinfo"]=True
                session["n"],session["w"],session["d"],session["e"],session["c"],session["a"],session["t"] = new_user.out()
                print(session["c"])
                if ifhisvip in vipcodes:
                    session["ifvip"]=True
                return redirect(url_for("check"))
            else:
                from_=request.headers["X-Real-Ip"]
                body_="提交了创建账户申请后由于非法字符而失败了"
                logst(from_=from_,body=body_,level=2)
                return render_template("dlbc1.html",ly="创建账户界面:输入的内容含有非法字符,如<等",fangfas=["重新输入所有信息,确保密码、用户名、邮箱等信息中不包含空格等非法字符"])
        else:
            from_=request.headers["X-Real-Ip"]
            body_="提交了创建账户申请后由于用户名或邮箱已存在而失败了"
            logst(from_=from_,body=body_,level=2)
            return render_template("dlbc1.html",ly="创建账户界面:用户已存在 或 该邮箱已被注册 ",fangfas=["更换用户名或修改邮箱地址"])
    return render_template("signup.html",form=form)

#* 创建新账户(确认验证码界面)
@app.route("/signup2",methods=["GET","POST"])
def check():
    if "stdinfo" in session:
        form=Check_code()
        from_=request.headers["X-Real-Ip"]
        body_="进入了创建账户的确认验证码界面"
        try:
            cursor.execute("insert into user_ip (userid,ip,sm) values (%s,%s,\"未知\")",(session["to_up2"],from_))
            cursor.commit()
        except:
            pass
        logst(from_=from_,body=body_)
        if form.validate_on_submit():
            print("Coding:%s"%(session["to_up2"]))
            real_code=session["c"]
            print(real_code)
            getd_code=form.checkcode.data
            if str(getd_code)==str(real_code):
                session["logged-in"]=True
                session["admin"]=False
                from_=request.headers["X-Real-Ip"]
                n,w,d,e,c,a=session["n"],session["w"],session["d"],session["e"],session["c"],session["a"]
                body_=n+"创建账户成功"
                logst(from_=from_,body=body_,level=1)
                session["t"]=p2times=3
                v=0
                if "ifvip" in session:
                    v=1
                    session["t"]=p2times=64
                    logst(from_=from_,body="开通了vip服务(来源:signup验证码兑换)",level=3)
                t2=Thread(target=write_to_sql,args=(n,w,d,e,c,a,v,p2times))
                t2.start()
                cr=send_file("files\\others\\用户须知.txt",as_attachment=True)
                fr=redirect(url_for("index"))
                payload = (cr,fr)
                #TODO: cr未实现返回
                return fr
            else:
                from_=request.headers["X-Real-Ip"]
                body_="提交了创建账户申请后由于邮箱验证码错误而失败了"
                logst(from_=from_,body=body_,level=2)
                return render_template('dlbc2.html',ly='验证码错误 ',fangfas=['重新查看并输入验证码'])
        return render_template("check.html",form=form)
    else:
        from_=request.headers["X-Real-Ip"]
        body_="可能的黑客攻击:直接进入了验证码确认界面而未绑定邮箱"
        logst(from_=from_,body=body_,level=5)
        return render_template("dlbc1.html",ly="创建账户界面:未绑定邮箱但意外地进入了确认验证码界面",fangfas=["退回到创建账户界面"])



#* 登录账户界面
@app.route("/signin",methods=["GET","POST"])
def signin():
    from_=request.headers["X-Real-Ip"]
    body_="尝试登录"
    logst(from_=from_,body=body_,level=1)
    form=Signin()
    if form.validate_on_submit():
        from_=request.headers["X-Real-Ip"]
        body_="提交了登录申请"
        logst(from_=from_,body=body_,level=1)
        username=form.username.data
        get_password=form.password.data
        cursor.execute("select password,if_admin,p2times,hash_salt from users where `userid`='%s'"%username)
        password=cursor.fetchall()

        print(username,"\n",password,"\n",get_password)

        if len(password) ==0:
            from_=request.headers["X-Real-Ip"]
            body_="提交了登录申请后由于错误的用户名而失败了"
            logst(from_=from_,body=body_,level=2)
            return render_template("dlbc3.html",ly="用户不存在",fangfas=["检查用户名"])
        else:
            password0=password[0]
            password1=password0[0]#密码,可能未经哈希
            if_admin=password0[1]
            try:#如果存在哈希盐 就加密对比
                hash_salt=password0[3]
                if len(hash_salt)==32:
                    get_password=newhah(hash_salt,get_password)
            except:pass
            print(password1)
            if password1==get_password:
                if if_admin==0 or not if_admin:
                    from_=request.headers["X-Real-Ip"]
                    session["to_up2"]=username
                    session["logged-in"]=True
                    session["admin"]=False
                    body_="登录成功"+username
                    logst(from_=from_,body=body_,level=1)
                    flash("Welcome back, %s"%username)
                else:
                    from_=request.headers["X-Real-Ip"]
                    body_="admin账号登录(请确认ip地址正确与否)"
                    logst(from_=from_,body=body_,level=3)
                    session["to_up2"]=username
                    session["logged-in"]=True
                    session["admin"]=True
                    flash("Welcome back, %s"%username)
                session["n"],session["w"],session["a"],session["t"]=username,password1,if_admin,password0[2]
                return redirect(url_for("index"))
            else:
                from_=request.headers["X-Real-Ip"]
                body_="提交了登录申请后由于密码错误而失败了"
                logst(from_=from_,body=body_,level=2)
                return render_template("dlbc3.html",ly="密码不正确",fangfas=["重新输入密码"])
    return render_template("signin.html",form=form)


#* 不展示: 转跳后登出
@app.route("/signout")
def signout():
    try:del session["logged-in"]
    except:del session["logged_in"]
    try:del session["admin"]
    except:pass
    try:del session["ifvip"]
    except:pass
    try:del session["n"]
    except:pass
    try:del session["w"]
    except:pass
    try:del session["d"]
    except:pass
    try:del session["e"]
    except:pass
    try:del session["c"]
    except:pass
    try:del session["v"]
    except:pass

    return redirect(url_for("index"))

#* 查看全部用户
@app.route("/usersall",methods=["GET","POST"])
def userall():
    if "logged-in" in session:
        cursor.execute("select userid,if_vip from users")
        users=cursor.fetchall()
        USER=[]
        for a_user in users:
            a=a_user[0]
            b=a
            if a_user[1] or a_user[1]==1:
                b=a+"(★★★vip★★★)"
            USER.append({"a":a,"b":b})
        return render_template("showallusers.html",all_user=USER)
    return redirect("/signin")

#* 查看全部文章
@app.route("/articles",methods=["GET","POST"])
def articles():
    if "logged-in" in session:
        cursor.execute("select head from article where level<>2")
        articles=cursor.fetchall()
        ARTIS1=[]
        for a_article in articles:
            ARTIS1.append(a_article[0])
        ARTIS2=[]
        for a_article in articles:
            ARTIS2.append(a_article[0].replace("_"," "))
        reponse=[]
        for i in range(0,len(ARTIS1)):
            a=ARTIS1[i]
            b=ARTIS2[i]
            reponse.append({"xhx":a,"ykg":b})
        return render_template("articles.html",ARTICLES=reponse)
    return redirect("/signin")

@app.route("/allfiles")
def allfiles():
    if "logged-in" in session:
        cursor.execute("select head,_time from files")
        answers=cursor.fetchall()
        HEAD=[]
        TIME=[]
        for answer in answers:
            HEAD.append(answer[0])
            TIME.append(answer[1])
        RESULT=[]
        for i in range(0,len(HEAD)):
            a=HEAD[i]
            b=TIME[i]
            RESULT.append({"a":a,"b":b})
        return render_template('files.html',all_file=RESULT)
    return redirect("/signin")


# 2仅社区可见 1仅公开可见
#* 创建一条内容
@app.route("/create",methods=["GET","POST"])
def create():
    form=article_input()
    if form.validate_on_submit():
        if "logged-in" in session:
            username=session["to_up2"]
            text_head=form.texthead.data
            text_inputd=form.body.data
            typea=form.typea.data#是否公开可见
            typeb=form.typeb.data#是否社区可见
            if typea:
                if typeb:level=3
                else:level=1
            else:
                level=2
            
            
            getname=sjn()
            with open("templates/articles/%s.txt"%getname,"w",encoding="utf8") as wr:
                wr.write("<h1>%s</h1>\n"%text_head)
                wr.write("<h5>作者: %s&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;创建时间:%s</h5>\n"%(username,get_time()))
                wr.write("<body>\n")
                wr.write(text_inputd)
                wr.write("</body>\n")
                wr.write("<a href=\"\"")
            cursor.execute("insert into article (head,body_place,author,level) values (%s,%s,%s,%s)",(text_head,getname,username,level))
            connect.commit()
            os.rename("templates/articles/%s.txt"%getname,"templates/articles/%s.html"%getname)
            delta=10+int(len(text_inputd)/300)
            add_score(username,delta)
            
            from_=request.headers["X-Real-Ip"]
            body_="上传了文章:%s"%text_head
            logst(from_=from_,body=body_,level=1)
            
            if level!=1:
                cursor.execute("select cmt_code from user_social where username=%s",(username))
                try:
                    get=cursor.fetchall()[0][0]
                    cursor.execute("insert into %s_article (head,author,body_place) values (%s,%s,%s)",(get,text_head,username,getname))
                    connect.commit()
                    flash("Article created successfully!")
                except:
                    flash("您尚未在某个社区中,但您选择了在社区中发布.已自动更改模式为仅公开发布!")
            
            return redirect(url_for("index"))
        else:
            from_=request.headers["X-Real-Ip"]
            body_="可能的黑客攻击:在未登录状态下请求了上传文章"
            logst(from_=from_,body=body_,level=3)
            return redirect(url_for("signin"))
    return render_template("write.html",form=form)

#* 查看某条内容
@app.route("/article")
def article():
    head=request.args.get('head')
    headers=request.args.get("from")
    if headers!="social":
        cursor.execute("select body_place from article where head=%s and level<>2",(head))
        answer=cursor.fetchall()
        if len(answer)==0:
            return redirect(url_for("articles"))
        result=answer[0]
        filepath=result[0]
        return render_template("articles/%s.html"%filepath)
    else:
        cursor.execute("select body_place from article where head=%s",(head))
        answer=cursor.fetchall()
        if len(answer)==0:
            return redirect(url_for("articles"))
        result=answer[0]
        filepath=result[0]
        return render_template("articles/%s.html"%filepath)

app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True
#* 上传文件页面
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = uploadfile()#file submit
    if form.validate_on_submit():
        if "logged-in" in session:
            f = form.file.data
            head = f.filename#! head:实际名称
            head = Markup.escape(head)
            type1= head.split(".")
            type_="."+type1[-1]#! filetype:类型
            f0=sjn()
            filename=f0+type_#! body_place:保存名
            author=session["to_up2"]#! author: 作者
            _time=get_time()#! _time: 时间
            f.save(os.path.abspath(os.path.dirname(__file__))+"\\files\others\\"+filename)
            cursor.execute("select body_place from files where head=\"%s\""%head)
            ans=cursor.fetchall()
            if len(ans)==0:
                cursor.execute("insert into files (head,filetype,body_place,author,_time) values    (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"%(head,type_,f0,author,_time))
                connect.commit()
                flash('Upload success.')
                from_=request.headers["X-Real-Ip"]
                body_="上传了文件%s"%head
                logst(from_=from_,body=body_,level=1)
                return redirect(url_for('index'))
            else:
                from_=request.headers["X-Real-Ip"]
                body_="因重名而上传文件失败(名称%s)"%head
                logst(from_=from_,body=body_,level=2)
                return render_template("dupload.html",form=form)
        else:
            return redirect(url_for("signin"))
    return render_template('upload.html', form=form)


#* 下载文件页面(转跳下载 不显示)
@app.route("/download")
def download_file(ih=False):
    if not (ih):
        if "logged-in" in session:
            head=request.args.get("head")
            cursor.execute("select body_place,filetype from files where head=\"%s\""%head)
            body_place=cursor.fetchall()
            if len(body_place)==0:
                abort(1024)
            a=body_place[0]
            body_place=a[0]
            filetype__=a[1]
        else:
            return redirect("/signin")
    else:
        body_place="用户须知"
        filetype__=".txt"
    path="files\\others\\"+body_place+filetype__
    from_=request.headers["X-Real-Ip"]
    body_="下载了文件%s"%head
    logst(from_=from_,body=body_,level=1)
    return send_file(path,as_attachment=True)

#* 管理员登录后的界面(由signin转入)
@app.route("/admin")
def admin():
    if session["admin"]:
        return render_template("main_in_admin.html")
    else:
        from_=request.headers["X-Real-Ip"]
        body_="可能的黑客攻击:用户尝试进入admin界面"
        logst(from_=from_,body=body_,level=3)
        return redirect(url_for("index"))


@app.route("/admin/deluser",methods=["GET","POST"])
def deluser():
    form=del_user()
    if form.validate_on_submit() and session["admin"]:
        username=form.username.data
        name=session["n"]
        if username!=name:
            cursor.execute("delete from users where userid=\"%s\""%username)
            connect.commit()
            flash("Delete!")
            return redirect(url_for("admin"))
        else:
            return "您不能删除自己的账号！"
    return render_template("admin_del_user.html",form=form)

@app.route("/admin/delarti",methods=["GET","POST"])
def delarti():
    form=del_arti() 
    if form.validate_on_submit() and session["admin"]:
        artiname=form.artiname.data
        cursor.execute("delete from article where head=\"%s\""%artiname.replace(" ","_"))
        connect.commit()
        flash("Delete!")
        return redirect(url_for("admin"))
    elif form.validate_on_submit():
        username=session["to_up2"]
        cursor.execute("select if_vip from users where userid=%s",(session["to_up2"]))
        vips=cursor.fetchall()[0][0]
        if vips:
            artiname=form.artiname.data
            cursor.execute("select author from article where head=%s",(artiname))
            if cursor.fetchall()[0][0]==username:
                cursor.execute("delete from article where head=\"%s\""%artiname.replace(" ","_"))
                connect.commit()
                flash("Delete!")
                return redirect(url_for("index"))
            else:
                return render_template("admin_del_arti.html",form=form,notice="权限组为vip,无法直接删除非本人文章.")
        else:
            return render_template("admin_del_arti.html",form=form,notice="权限组为普通用户,无法删除个人文章.")
    return render_template("admin_del_arti.html",form=form,notice="")

#* 用户的个人信息
@app.route("/user_space")
def user_space():
    if "logged-in" in session:
        username=request.args.get("username")
        cursor.execute("select head from article where `author`='%s'"%est(username))
        articles=cursor.fetchall()
        ARTIS1=[]
        for a_article in articles:
            ARTIS1.append(a_article[0])
        ARTIS2=[]
        for a_article in articles:
            ARTIS2.append(a_article[0].replace("_"," "))
        reponse=[]
        for i in range(0,len(ARTIS1)):
            a=ARTIS1[i]
            b=ARTIS2[i]
            reponse.append({"xhx":a,"ykg":b})
        cursor.execute("select zhuce_time,description,if_vip from users where `userid`='%s'"%username)
        answer_from_sql=cursor.fetchall()
        answer=answer_from_sql[0]
        if answer[2] or answer[2]==1:
            a_user={"name":username,"desc":answer[1],"time":answer[0],"ivip":1}
        else:
            a_user={"name":username,"desc":answer[1],"time":answer[0],"ivip":0}
        level,_=get_level_and_score(username)    
        return render_template("auser.html",ARTICLES=reponse,a_user=a_user,level=level)
    return redirect("/signin")


@app.route("/admin/allow",methods=["GET","POST"])
def allow_social():
    form=all_social()
    if form.validate_on_submit():
        admincode=form.admincode.data
        socialname=form.social_na.data
        if admincode in admincodes:
            cursor.execute("update social set state=3 where member_place=%s",(socialname))
            cursor.execute("create table "+socialname+"_article(\
                head varchar(32) not null primary key,\
                author varchar(40) not null,\
                body_place varchar(33))default charset utf8")
            connect.commit()
            with open("files/socials/%s.txt"%socialname,"w",encoding="utf8") as new:
                new.write("")
            flash("审批成功,该社团/社区已成为非正式社团,社团状态码0-10.")
        return redirect(url_for("index"))
    return render_template("admin_allow_social.html",form=form)


@app.route("/patch")
def patch():
    if "logged-in" in session:
        return render_template("patch_main.html")
    return redirect("/signin")

@app.route("/patch/text",methods=['GET','POST'])
def patch_1():
    if "logged-in" in session:
        form=_patch_1()
        if form.validate_on_submit():
            text=form.name.data
            data=search(str(text))
            from_=request.headers["X-Real-Ip"]
            body_="用户查询了"+text
            logst(from_=from_,body=body_,level=1)
            return render_template("patch_answer_text.html",text=text,body_text=data)
        return render_template("patch_1.html",form=form)
    return redirect("/signin")


@app.route("/patch/image",methods=["GET","POST"])
def patch_2():
    if "logged-in" in session:
        form=_patch_2()
        if form.validate_on_submit():
            username=session["n"]
            cursor.execute("select if_vip from users where userid=%s",(username))
            vips=cursor.fetchall()
            vip=vips[0]
            if_vip=vip[0]
            level,score=get_level_and_score(name=username)
            
            if "ifvip" in session or if_vip or level>=5:
                name=form.name.data
                times=form.times.data
                token=spider.run(name,times)
                rmtree("files/temps/%s"%name)
                return """
                您的图片已经准备完成.出于安全考虑,我们不能直接为您提供下载.这是出于防止大量利用本站下载图片而恶意DDoS等攻击.请前往<a href="/patch">爬取工具</a>页面的"本站token文件提取"页面输入token来下载图片压缩包.
                您的token:<b>%s</b>
                """%token
            else:
                stimes=session["t"]
                if stimes==0:
                    return """
                    很抱歉,但您的图片爬虫免费试用次数已用完.<br>
                    <a href="/patch">点我返回工具界面</a>"""
                else:
                    a=stimes-1
                    stimes=session["t"]=a
                    new_times(session["n"],a)
                    name=form.name.data
                    times=form.times.data
                    token=spider.run(name,times)
                    rmtree("files/temps/%s"%name)
                    return """
                    您的图片已经准备完成.出于安全考虑,我们不能直接为您提供下载.这是出于防止大量利用本站下载图片而恶意DDoS等攻击.请前往<a href="/patch">爬取工具</a>页面的"本站token文件提取"页面输入token来下载图片压缩包.
                    您的token:<b>%s</b>
                    另外,由于您不是vip用户,您的图片爬虫免费使用次数还有: %s 次.
                    """%(token,a)
        return render_template("patch_2.html",form=form)
    return redirect("/signin")


@app.route("/patch/get_token",methods=["GET","POST"])
def patch_3():
    if "logged-in" in session:
        form=_patch_3()
        if form.validate_on_submit():
            token=form.name.data
            return send_file("files/temps/zips/%s.zip"%token,as_attachment=True)
        return render_template("patch_3.html",form=form)
    return redirect("/signin")


@app.route("/game",methods=["GET","POST"])
def game():
    form=yincai()
    if form.validate_on_submit():
        name=form.name.data
        logst(request.headers["X-Real-Ip"],"有人竞猜了内容:%s"%name)
        flash("竞猜已发出!")
        return redirect("/")
    return render_template("game.html",form=form)

@app.route("/havevip",methods=["GET","POST"])
def havevip():
    form=getvip()
    try:
        cursor.execute("select if_vip from users where userid=%s",(session["to_up2"]))
    except KeyError:
        return redirect(url_for("signin"))
    get=cursor.fetchall()
    ifvip=get[0]
    ifvip=ifvip[0]
    if not ifvip:
        if form.validate_on_submit():
            token=form.name.data
            print(token)
            if token in vipcodes:
                setvip(session["to_up2"])
                flash("vip兑换成功!")
                add_score(session["to_up2"],1000)
                from_=request.headers["X-Real-Ip"]
                logst(from_=from_,body="用户兑换了vip(来源:vip兑换界面)",level=3)
                return redirect(url_for("index"))
            return render_template("havevip.html",form=form,nowd="您的token不正确!")
        if "logged-in" in session:
            return render_template("havevip.html",form=form,nowd="")
        else:
            return redirect(url_for("signin"))
    else:
        return """您已经是一名vip了!<a href="/">点我返回首页</a>"""


# 状态码
# 1：正在申请
# 2：申请通过，非正式社区
# 3：正式社区（1级）
# 4：正式社区（2级）
# 5：正式社区（3级）
#* 创建社区
@app.route("/social/new",methods=["GET","POST"])
def create_social():
    form=new_socail()
    if form.validate_on_submit():
        if "to_up2" in session:
            level,_=get_level_and_score(session["to_up2"])
            if level>=6:
                pre_name=sjn()
                name=form.name.data
                desc=form.text.data
                if desc is None:desc="该社区区长没有留下发言……"
                cursor.execute("insert into social (name,owner,member_place,state,descrtipion) values (%s,%s,%s,%s,%s)",(name,session["to_up2"],pre_name,1,desc))
                connect.commit()
                flash("建立社区申请已提交,待管理员审批.(状态码:0x0000ad03)")
            else:
                flash("用户等级不足(需6级方可建立社区)") 
            return redirect(url_for("index"))       
        else:
            return redirect(url_for("signin"))
            
    return render_template("new_social.html",form=form)



@app.route("/social/view")
def view_a_social():
    if "to_up2" in session or "logged_in" in session:
        social_code=request.args.get("code")
        cursor.execute("select owner,name,state,descrtipion from social where member_place=%s",(social_code))
        owner,name,state,desc=cursor.fetchall()[0]
        if state==1: 
            state_="该社团正在审批中,尚未开放"  
            seeable=False
        elif state==2:
            state_="该社团审批已通过,但未拥有除拥有者外的成员."
            seeable=True
        else:
            state_="该社团的等级为:   %s"%(state-2)
            seeable=True
        cursor.execute("select head from "+social_code+"_article")
        heads=cursor.fetchall()    
        return render_template("social_community.html",social={"name":name,"owner":owner,"desc":desc,"info":state_,"cansee":seeable},heads=heads)    
                


@app.route("/aip")
def aip_main():
    return render_template("aip_main.html")


@app.route("/echarts")
def test():
    return render_template("echarts_all.html")


@app.route("/echarts/<mode>")
def echarts(mode):
    if mode=="twoaxis":
        return render_template("echarts/a.html")
    elif mode=="datasets":
        return render_template("echarts/b.html")
    elif mode=="piedata":
        return render_template("echarts/c.html")
    else:
        return render_template("echarts/d.html")




#* 404
@app.errorhandler(404)
def error_404(e):
    from_=request.headers["X-Real-Ip"]
    if request.endpoint!=None:
        try:
            BOdy=str(e)+request.endpoint
        except TypeError:
            BOdy="404 ERROR"+request.endpoint
    else:
        BOdy=str(e)
    logst(from_=from_,body=BOdy,level=4)
    return render_template("errors/404.html"),404

@app.errorhandler(400)
def error_400(e):
    from_=request.headers["X-Real-Ip"]
    if request.endpoint!=None:
        try:
            BOdy=str(e)+request.endpoint
        except TypeError:
            BOdy="400 ERROR"+request.endpoint
    else:
        BOdy=str(e)
    logst(from_=from_,body=BOdy,level=4)
    return render_template("errors/400.html"),400

@app.errorhandler(401)
def error_401(e):
    from_=request.headers["X-Real-Ip"]
    if request.endpoint!=None:
        try:
            BOdy=str(e)+request.endpoint
        except TypeError:
            BOdy="401 ERROR"+request.endpoint
    else:
        BOdy=str(e)
    logst(from_=from_,body=BOdy,level=4)
    return render_template("errors/401.html"),401

@app.errorhandler(403)
def error_403(e):
    from_=request.headers["X-Real-Ip"]
    if request.endpoint!=None:
        try:
            BOdy=str(e)+request.endpoint
        except TypeError:
            BOdy="403 ERROR"+request.endpoint
    else:
        BOdy=str(e)
    logst(from_=from_,body=BOdy,level=4)
    return render_template("errors/403.html"),403

@app.errorhandler(500)
def error_500(e):
    from_=request.headers["X-Real-Ip"]
    if request.endpoint!=None:
        try:
            BOdy=str(e)+request.endpoint
        except TypeError:
            BOdy="500 ERROR"+request.endpoint
    else:
        BOdy=str(e)
    logst(from_=from_,body=BOdy,level=4)
    return render_template("errors/500.html",e=e),500



