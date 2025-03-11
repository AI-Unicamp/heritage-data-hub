from pymongo import MongoClient
from collections import Counter

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "europeana_db"
COLLECTION_NAME = "cultural_objects"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


def summarize_mongo():
    """Generate a summary of the MongoDB database."""
    total_items = collection.count_documents({})

    # Check sample document structure
    sample = collection.find_one()

    # Count unique providers (if available)
    providers = collection.distinct("object.aggregations.edmProvider.def")
    total_providers = len(providers)

    # Count year distribution
    years = []
    for doc in collection.find({}, {"object.agents.begin.def": 1}):
        year = (
            doc.get("object", {})
            .get("agents", [{}])[0]
            .get("begin", {})
            .get("def", ["Unknown"])[0]
        )
        years.append(year)

    year_counts = Counter(years)

    # Print summary
    print("\n📊 MongoDB Summary Report")
    print("----------------------------------")
    print(f"Total Items: {total_items}")
    print(f"Total Unique Providers: {total_providers}")
    print(f"Year Distribution (Top 5): {dict(year_counts.most_common(5))}")
    print(f"Sample Document Keys: {list(sample.keys()) if sample else 'No data found'}")


if __name__ == "__main__":
    summarize_mongo()
