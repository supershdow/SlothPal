import Reader as reader

def sendMessage(sender,recipient,message):
    reader.write_file('./util/'+recipient+'message.txt',sender+' writes: '+message+'\n','a')

def readMessage(user):
    messages=reader.getCsvDict(user+'message.txt')
    return messages
