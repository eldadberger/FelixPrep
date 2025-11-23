from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")  # update if needed
db = client["doudu"]
collection = db["icons"]

cursor = collection.find()

for doc in cursor:
    mw = doc.get("mutationWeight")
    if not mw:
        continue

    colors = mw.get("colors")

    # Only convert if colors is a dict
    if isinstance(colors, dict):
        new_colors = [
            {"key": key, "weight": value}
            for key, value in colors.items()
        ]

        # Build new mutationWeight
        new_mw = dict(mw)  # copy other fields if exist
        new_mw["colors"] = new_colors

        # Update document
        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"mutationWeight": new_mw}}
        )

print("Migration complete.")
