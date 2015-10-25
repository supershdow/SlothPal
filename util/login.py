import Reader as read

def validate(username, password):
    if username=='' or password=='':
        return False
    creds=read.getCsvDict('./util/credentials.txt')
    if username in creds.keys() and creds[username][0]==password:
        return True
    else:
        return False

def signup(new_username,new_password,gender,Countryin,Targetcountry):
    previousCredentials=read.read_file('./util/credentials.txt')
    new_credentials='%s,%s,%s,%s,%s'%(new_username,new_password,gender,Countryin,Targetcountry)
    if new_username=='' or new_password=='' or new_username in previousCredentials or new_username.find(',')!=-1 or new_password.find(',')!=-1:
        return 'Invalid signup credentials'
    else:
        read.write_file('./util/credentials.txt','\n'+new_credentials,'a')
        return 'Successfully signed up'

if __name__=='__main__':
    print validate('magic','unicorns')
    print signup('sloth','themed')
