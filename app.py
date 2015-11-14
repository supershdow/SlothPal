from flask import Flask,render_template,request,session,redirect,url_for
from flask_bootstrap import Bootstrap
from util import login as lo
from util import Reader as reader
from util import messages as mess
from random import choice

app=Flask(__name__)
Bootstrap(app)

globe = {}

globe["session"] = session


@app.route('/')
def root():
    return render_template('index.html')

@app.route('/log')
def log():
    #return app.send_static_file('account/login.html')
    #return url_for('static', filename='login.html')
    return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def log_in():
    if request.method=="GET":
        return 'GET'
    elif request.method=="POST":
        data=request.form
        if lo.validate(data['username'],data['password'])==True:
            session['username']=data['username']
            return redirect('/home')
        else:
            return redirect('/')
    else:
        return 'yo'

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    elif request.method=='POST':
        data=request.form
        if data['change']=="Change info":
            lo.changeSettings(session['username'],data['nuser'],data['npswd'],data['gender'],data['Countryin'],data['Countrylook'])
            return redirect('/account/'+session['username'])
        lo.sign_up(data['nuser'],data['npswd'],data['gender'],data['Countryin'],data['Countrylook'])
        return redirect('/')
    else:
        return 'yo'

@app.route('/home')
def home():
    if not 'username' in session:
        return redirect('/')
    user_list=reader.getCsvDict('./util/credentials.txt')
    current=user_list[session['username']][3]
    del user_list[session['username']]
    g=0
    rect=False
    rec=[]
    for i in user_list.keys():
        if user_list[i]==current:
            rec.append(user_list.items()[g][0])
            rect=True
        g+=1
    if rec!=[]:
        rec=choice(rec)
    usr=session['username']
    url='/account/'+usr+'/sendmessage'
    if not rect:
        return render_template('home.html',user=session['username'],prof='/account/'+session['username'],recomended=rect,dir=url)
    return render_template('home.html',user=session['username'],prof='/account/'+session['username'],rec='/account/'+rec,recomended=rect,dir=url)

@app.route('/account/<usr>')
def account(usr):
    if not 'username' in session:
        return redirect('/')
    user_list = reader.getCsvDict("./util/credentials.txt")
    if not usr in user_list.keys():
        return render_template("error.html",error = "The username you have provided does not exist.",globe=globe)
    img=reader.getCsvDict('util/pfpimg.txt')
    userinfo=user_list[usr]
    gender=userinfo[1]
    Countryin=userinfo[2]
    Target=userinfo[3]
    url='/account/'+session['username']+'/settings'
    if session['username']==usr:
        own=True
    else:
        own=False
    if usr in img:
        img=img[usr][0]
    else:
        img='http://s3-static-ak.buzzfed.com/static/2014-07/14/12/campaign_images/webdr09/meet-lunita-the-cutest-baby-sloth-on-planet-earth-2-9684-1405357019-4_big.jpg'
    return render_template("account.html",user = usr,user_list = user_list,globe=globe, img=img,gender=gender,Country=Countryin,target=Target,own=own,dir=url)
    
@app.route('/account/pfppic', methods=['POST'])
def pfppic():
    if not 'username' in session:
        return redirect('/')
    url=request.form['image']
    reader.write_file('util/pfpimg.txt',session['username']+','+url+'\n','a')
    return redirect('/account/'+session['username'])

@app.route('/account/<usr>/sendmessage',methods=['GET','POST'])
def sendmessage(usr):
    reader.write_file('./util/'+usr+'message.txt','','a')
    url='/account/'+usr+'/sendmessage'
    if not 'username' in session:
        return redirect('/')
    user_list=reader.getCsvDict('./util/credentials.txt').keys()
    messages=reader.read_file('./util/'+usr+'message.txt')
    messages=messages.split('\n')
    messages.pop(-1)
    if messages==['']:
        out=False
    else:
        out=True
    if request.method=='GET':
        return render_template('messages.html',dir=url,messages=messages,out=out)
    elif request.method=='POST':
        if not request.form['recipient'] in user_list:
            return render_template('messages.html',dir=url,messages=messages,out=out)
        mess.sendMessage(session['username'],request.form['recipient'],request.form['message'])
        return redirect(url)

@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method=='GET':
        reader.write_file('./util/'+session['username']+'message.txt','')
    else: 
        if request.method=='POST':
            old=reader.getCsvList('./util/'+session['username']+'message.txt')
            old.pop([int(request.form.keys()[0])][0])
            reader.write_file('./util/'+session['username']+'message.txt','')
            old.pop()
            for mess in old:
                reader.write_file('./util/'+session['username']+'message.txt',mess[0]+'\n','a')
    return redirect('/account/'+session['username']+'/sendmessage')
            

@app.route('/account/<usr>/settings')
def settings(usr):
    return render_template("settings.html")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect('/')

if __name__=='__main__':
    app.secret_key='\xf2\xd4\x9c\xc8\xf6~\xabk|\x8bL\xfbfK\x7f\xc5\xc3\xc4\x0bX\xa7\xf3\x91\x1f'
    app.debug=True
    app.run()
