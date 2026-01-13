from pymongo import ASCENDING


INDEX_DEFINITIONS = {
    "users": [
        {
            "keys": [("email", ASCENDING)],
            "options": {"unique": True},
        },
        {
            "keys": [("username", ASCENDING)],
            "options": {"unique": True},
        },
    ],
    "authors": [
        {
            "keys": [("name", ASCENDING)],
            "options": {"unique": True},
        },
    ],
    "books": [
        {
            "keys": [("title", ASCENDING)],
            "options": {"unique": True},
        },
    ],
}

async def create_indexes(db):
    for collection_name, indexes in INDEX_DEFINITIONS.items():
        collection = db[collection_name]

        existing_indexes = await collection.index_information()

        for index in indexes:
            keys = index["keys"]
            options = index.get("options", {})

            # nome padrão do mongo (email_1, name_lower_1, etc)
            index_name = "_".join(f"{k}_{v}" for k, v in keys)

            if index_name not in existing_indexes:
                await collection.create_index(keys, **options)

