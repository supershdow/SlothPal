from flask import Flask,render_template,request,session,redirect
from flask_bootstrap import Bootstrap
from util import login as log
from util import Reader as reader


app=Flask(__name__)
Bootstrap(app)

globe = {}

globe["session"] = session



@app.route('/')
def root():
    return render_template('login-form.html')

@app.route('/login',methods=['GET','POST'])
def log_in():
    if request.method=="GET":
        return 'GET'
    elif request.method=="POST":
        data=request.form
        if log.validate(data['username'],data['password'])==True:
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
        log.signup(data['nuser'],data['npswd'],data['gender'],data['Countryin'],data['Targetcountry'])
        return render_template('login-form.html')
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
    for i in user_list.keys():
        if user_list[i][2]==current:
            rec=user_list.items()[g][0]
            rect=True
        g+=1
    if not rect:
        return render_template('home.html',user=session['username'],prof='/account/'+session['username'],recomended=rect)
    return render_template('home.html',user=session['username'],prof='/account/'+session['username'],rec='/account/'+rec,recomended=rect)

@app.route('/account/<usr>')
def account(usr):
    if not 'username' in session:
        return redirect('/')
    user_list = reader.getCsvDict("./util/credentials.txt")
    if not usr in user_list.keys():
        return render_template("error.html",error = "The username you have provided does not exist.",globe=globe)
    img=reader.getCsvDict('util/pfpimg.txt')
    userinfo=user_list[usr]
    print userinfo
    gender=userinfo[1]
    Countryin=userinfo[2]
    Target=userinfo[3]
    if usr in img:
        img=img[usr][0]
    else:
        img='http://s3-static-ak.buzzfed.com/static/2014-07/14/12/campaign_images/webdr09/meet-lunita-the-cutest-baby-sloth-on-planet-earth-2-9684-1405357019-4_big.jpg'
    return render_template("account.html",user = usr,user_list = user_list,globe=globe, img=img,gender=gender,Country=Countryin,target=Target)
    
@app.route('/account/pfppic', methods=['POST'])
def pfppic():
    if not 'username' in session:
        return redirect('/')
    url=request.form['image']
    reader.write_file('util/pfpimg.txt',session['username']+','+url+'\n','a')
    return redirect('/account/'+session['username'])

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect('/')

if __name__=='__main__':
    app.secret_key='\xf2\xd4\x9c\xc8\xf6~\xabk|\x8bL\xfbfK\x7f\xc5\xc3\xc4\x0bX\xa7\xf3\x91\x1f'
    app.debug=True
    app.run()
