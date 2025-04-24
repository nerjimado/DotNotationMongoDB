def top_5_paises(collection):
    pipeline = [
        {"$group": {"_id": "$country", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}},
        {"$limit": 5}
    ]
    print("\nTop 5 países con más usuarios:")
    for doc in collection.aggregate(pipeline):
        print(f"{doc['_id']}: {doc['total']} usuarios")
