import Reader as read

def validate(username, password):
    if username=='' or password=='':
        return False
    creds=read.getCsvDict('./util/credentials.txt')
    if username in creds.keys() and creds[username][0]==password:
        return True
    else:
        return False

def sign_up(new_username,new_password,gender,Countryin,Targetcountry):
    previousCredentials=read.read_file('./util/credentials.txt')
    new_credentials='%s,%s,%s,%s,%s'%(new_username,new_password,gender,Countryin,Targetcountry)
    if new_username=='' or new_password=='' or new_username in previousCredentials or new_username.find(',')!=-1 or new_password.find(',')!=-1:
        return 'Invalid signup credentials'
    else:
        read.write_file('./util/credentials.txt','\n'+new_credentials,'a')
        return 'Successfully signed up'

def changeSettings(old_user,new_username,new_password,gender,Countryin,Targetcountry):
    previousCredentials=read.getCsvDict('./util/credentials.txt')
    newCredentials=''
    if new_username=='':
        newCredentials+=old_user+','
    else:
        newCredentials+=new_username+','
    if new_password=='':
        newCredentials+=previousCredentials[old_user][0]+','
    else:
        newCredentials+=new_password+','
    if gender=='blank':
        newCredentials+=previousCredentials[old_user][1]+','
    else:
        newCredentials+=gender+','
    if Countryin=='':
        newCredentials+=previousCredentials[old_user][2]+','
    else:
        newCredentials+=Countryin+','
    if Targetcountry=='':
        newCredentials+=previousCredentials[old_user][3]
    else:
        newCredentials+=Targetcountry
    
    del previousCredentials[old_user]
    newCredentials=newCredentials.split(',')
    previousCredentials[newCredentials[0]]=newCredentials[1:]
    Credentials=''
    for i in previousCredentials.keys():
        Credentials+=i+','
        for u in previousCredentials[i]:
            Credentials+=u+','
        
        Credentials=Credentials[:-1]+'\n'
        
    read.write_file('./util/credentials.txt',Credentials,'w')

if __name__=='__main__':
    print validate('magic','unicorns')
    print signup('sloth','themed')
