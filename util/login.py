import Reader as read

def validate(username, password):
    if username=='' or password=='':
        return False
    creds=read.getCsvDict('credentials.txt')
    if creds[username]==password:
        return True
    else:
        return False

def signup(new_username,new_password):
    previousCredentials=read.read_file('credentials.txt')
    new_credentials='%s,%s'%(new_username,new_password)
    if new_username=='' or new_password=='' or new_username in previousCredentials or new_username.find(',')!=-1 or new_password.find(',')!=-1:
        return 'Invalid signup credentials'
    else:
        read.write_file('credentials.txt',new_credentials,'a')
        return 'Successfully signed up'

if __name__=='__main__':
    validate('magic','unicorns')
    signup('Sloth','themed')
