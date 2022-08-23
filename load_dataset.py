from pymongo import MongoClient

conn = MongoClient('mongodb+srv://rebeccah:6tes5DKS5as63fpeI9Cr@cluster0.z4vhaxi.mongodb.net/Cluster0?retryWrites=true&w=majority')

db = conn["ResourceManager"]

account_collection = db.account_collection

accounts = [
    {
        "uid": "axj",
        "gecos": "Alice Jones",
        "uidNumber": 1111,
        "eppns": ["alice@gmail.com", "a.jones@stanford.edu"],
        "status": {
            "training_uptodate": True,
            "last_account_activity": "2022-03-01T15:48:12Z"
        }
    },
    {
        "uid": "wns",
        "gecos": "Ben Smith",
        "uidNumber": 1261,
        "eppns": ["ben.smith@hotmail.com", "ben@yale.edu"],
        "status": {
            "training_uptodate": True,
            "last_account_activity": "2022-01-01T07:12:03Z"
        }
    },
    {
        "uid": "cjt",
        "gecos": "Clare Taylor",
        "uidNumber": 2983,
        "eppns": ["clare.taylor@yahoo.com", "cjt@mit.edu"],
        "status": {
            "training_uptodate": False,
            "last_account_activity": "2021-10-27T21:28:09Z"
        }
    }
]

account_collection.insert_many(accounts)

account_collection.create_index("uid", unique=True)
account_collection.create_index("uidNumber", unique=True)

cursor = account_collection.find()
for record in cursor:
    print(record)