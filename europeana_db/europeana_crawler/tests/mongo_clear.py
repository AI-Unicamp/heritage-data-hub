from pymongo import MongoClient

# Connect to MongoDB
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "europeana_db"
COLLECTION_NAME = "cultural_objects"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Delete all documents in the collection
delete_result = collection.delete_many({})
print(f"Deleted {delete_result.deleted_count} documents from MongoDB.")
