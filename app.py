from flask import Flask,render_template,request,session,redirect
from util import login as log
from util import Reader as reader


app=Flask(__name__)


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
            return 'Invalid login'
    else:
        return 'yo'

@app.route('/signup',methods=['GET','POST'])
def signup():
    data=request.form
    if request.method=='GET':
        return render_template('signup.html')
    elif request.method=='POST':
        log.signup(data['username'],data['password'])
        return 'Successfully signed up'
    else:
        return 'yo'

@app.route('/home')
def home():
    return 'Homepage'

@app.route('/account/<usr>')
def account(usr):
    user_list = reader.getCsvDict("./util/credentials.txt")
    if not usr in user_list.keys():
        return render_template("error.html",error = "The username you have provided does not exist.",globe=globe)
    return render_template("account.html",user = usr,user_list = user_list,globe=globe)
    



@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return 'logout'

if __name__=='__main__':
    app.secret_key='\xf2\xd4\x9c\xc8\xf6~\xabk|\x8bL\xfbfK\x7f\xc5\xc3\xc4\x0bX\xa7\xf3\x91\x1f'
    app.debug=True
    app.run()
