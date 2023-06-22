# Import the necessary libraries
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import credentials
#import urllib.parse

#password=urllib.parse.quote_plus(credentials.mongodb_password)
#uri=   "mongodb+srv://" + mongodb_username + ":" + password + mongodb_uri

uri = credentials.mongodb_uri

# Function to purge the collection
def purge_collection(collection):
    result = collection.delete_many({})
    
    return('Deleted {} documents from collection.'.format(result.deleted_count))

def addData(data,collection):
    ids=[]
    for item in data:
        # Insert a document
        doc = item
        result = collection.insert_one(doc)
        ids.append(result.inserted_id)
    return(ids)

def authenticatedb(dbname='maindb'):
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        import sys
        #print (sys._getframe(1).f_code.co_name)
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    # Get the database
    return client[dbname]

if __name__ == '__main__':
    authenticatedb()


