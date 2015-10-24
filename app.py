from flask import Flask,render_template,request,session,redirect
from util import login

app=Flask(__name__)

@app.route('/')
def root():
    return render_template('base.html')

@app.route('/login',methods=['POST'])
def login():
    data=request.form
    if validate(data['username'],data['password']):
        session['username']=data['username']
        return redirect('/home')

@app.route('/home')
def home():
    return 'Homepage'

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect('/')

if __name__=='__main__':
    app.secret_key='\xf2\xd4\x9c\xc8\xf6~\xabk|\x8bL\xfbfK\x7f\xc5\xc3\xc4\x0bX\xa7\xf3\x91\x1f'
    app.debug=True
    app.run()
