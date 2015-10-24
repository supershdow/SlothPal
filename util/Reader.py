def read_file(fname):
    f=open(fname)
    s=f.read()
    f.close()
    return s

def getCsvList(fname):
    words=read_file(fname)
    lines=words.split('\n')
    line_list=[]
    for line in lines:
        z=line.split(',')
        line_list.append(z)
    return line_list

def getCsvDict(fname):
    lists=getCsvList(fname)
    foo={}
    for item in lists:
        key=item.pop(0)
        value=item
        foo[key]=value
    return foo

def write_file(fname,text,mode='w'):
    f=open(fname, mode)
    f.write(text)
    f.close()

if __name__=='__main__': #If running on its own
    text=read_file('wordlist.csv')
    lines=getCsvList('wordlist.csv')
    print text
    print lines
    print getCsvDict('wordlist.csv')
