def create_indexes(collection):
    collection.create_index("contact.email")
    collection.create_index("shoppings.provider.country")
    print("\nÍndices creados en contact.email y shoppings.provider.country.")
