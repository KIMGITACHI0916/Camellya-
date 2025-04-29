from pymongo import MongoClient

# MongoDB connection
MONGO_URL = "mongodb+srv://pop300k:tE4m7yVI6DNtXWsk@cluster0.y3knwm0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URL)

# Database and collection
db = client["camellia_bot"]
warns = db["warns"]

def warn_user(chat_id: int, user_id: int, reason: str = "No reason provided"):
    """Inserts or updates a warning for a user in a specific chat."""
    warns.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {
            "$push": {"reasons": reason},
            "$inc": {"count": 1}
        },
        upsert=True
    )
  
