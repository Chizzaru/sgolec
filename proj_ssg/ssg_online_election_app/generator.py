from hashids import Hashids

def runGeneration(saltStr, minLength, end):
    hash_id = Hashids(salt=str(saltStr), min_length=int(minLength))
    list_vcode = []
    end = int(end)+1
    for x in range(1,end):
        list_vcode.append(hash_id.encrypt(x))
    return list_vcode

#mylist = runGeneration('HelloWorld',8,1,10)

#print(mylist)