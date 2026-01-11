async def create_indexes(db):
    await db.users.create_index(
        'email', unique=True, name='users_email_unique'
    )
    await db.users.create_index(
        'username', unique=True, name='users_username_unique'
    )
    await db.authors.create_index(
        'name', unique=True, name='authors_name_unique'
    )
    await db.books.create_index('title', unique=True, name='title_name_unique')
