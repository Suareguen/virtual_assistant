from motor.motor_asyncio import AsyncIOMotorClient

# Connect to the MongoDB instance
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.testing  # Define the database
