import pymongo
import pandas as pd
import time
client = pymongo.MongoClient(
        "mongodb+srv://ncku_gwhsu:123@cluster0.wtz5pwg.mongodb.net/?retryWrites=true&w=majority")
db = client['containers']['delay1']

i = 0

while True:

    collection = list(db.find())
    data = pd.DataFrame(collection)
    r = data['123']
    print('i =', i)
    try:
        ans = r[i]
        if ans > 0.01:
            print('violation')
            print(ans)
        i = i + 1
    except:
        pass




