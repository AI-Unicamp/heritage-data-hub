from pymongo import MongoClient

# MongoDB Connection Setup
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "europeana_db"
COLLECTION_NAME = "cultural_objects"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


def insert_bulk_metadata(metadata_list, item_ids):
    """Insert multiple JSON metadata records into MongoDB in bulk using item_id as _id."""
    if not metadata_list or not item_ids:
        print("⚠️ No valid metadata to insert into MongoDB. Skipping batch.")
        return 0

    try:
        # Ensure each document has `_id` set as `item_id`
        for metadata, item_id in zip(metadata_list, item_ids):
            metadata["_id"] = item_id

        result = collection.insert_many(metadata_list, ordered=False)
        inserted_count = len(result.inserted_ids)
        print(f"✅ Inserted {inserted_count} items into MongoDB.")
        return inserted_count

    except Exception as e:
        print(f"❌ ERROR: Failed to insert batch into MongoDB: {e}")
        return 0
