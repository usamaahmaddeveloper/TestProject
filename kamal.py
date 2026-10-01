from pymongo import MongoClient, InsertOne
import time

# =========================
# MongoDB
# =========================

MONGO_URI = "mongodb://localhost:27017/"

client = MongoClient(MONGO_URI)

# Test connection
client.admin.command("ping")
print("MongoDB connected!")

db = client["tst"]
collection = db["tst"]

# =========================
# SETTINGS
# =========================

START = 1

# Example:
# 1,000,000 = generate until 1 million
# 1,000,000,000 = 1 billion
# END = 1_000_000
END = 43_608_742_899_428_874_059_776

# Number of records inserted per MongoDB operation
BATCH_SIZE = 1_000_000


# =========================
# a -> z -> aa -> ab...
# =========================

def number_to_letters(n):
    result = []

    while n > 0:
        n -= 1
        result.append(chr(97 + (n % 26)))
        n //= 26

    return "".join(reversed(result))


# =========================
# GENERATE + INSERT
# =========================

start_time = time.time()

for batch_start in range(START, END + 1, BATCH_SIZE):

    batch_end = min(
        batch_start + BATCH_SIZE - 1,
        END
    )

    documents = []

    for i in range(batch_start, batch_end + 1):

        documents.append({
            "_id": i,
            "code": number_to_letters(i)
        })

    collection.insert_many(
        documents,
        ordered=False
    )

    elapsed = time.time() - start_time

    print(
        f"Inserted: {batch_end:,} / {END:,} "
        f"| Batch: {len(documents):,} "
        f"| Time: {elapsed:.2f}s"
    )

print("\nDONE!")
