import pymongo

try:
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client['spiceblue']
    user = db.user
    user_session = db.user_session
    products = db.products
    print("database connection success")
except Exception as e:
    print(e)


# client = pymongo.MongoClient("mongodb+srv://dheera97:dheeraj@dheeaj.rwgs6.mongodb.net/myFirstDatabase?retryWrites
# =true&w=majority")