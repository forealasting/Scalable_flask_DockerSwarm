import pymongo
import pandas as pd
client = pymongo.MongoClient("mongodb+srv://ncku_gwhsu:123@cluster0.wtz5pwg.mongodb.net/?retryWrites=true&w=majority")
db_delay = client['containers']['delay1']
db_cpu = client['state']['cpu_u1']
db_type = client['status']['type']





def get_type(db_type):
    type1 = pd.DataFrame(list(db_type.find()))
    # print(type1['type'][0])
    type1 = type1['type'][0] # str

    return type1


def update_type(type1, type_c):
    myquery = {'type': type1}
    newvalues = {"$set": {'type': type_c}}
    db_type.update_many(myquery, newvalues)


type1 = get_type(db_type)
print(type1)
update_type(type1, '1')
type1 = get_type(db_type)
print(type1)
##
## cursor = db.find({})
## for document in cursor:
##       print(document)
##

## delete all
x = db_delay.delete_many({})
y = db_cpu.delete_many({})
###