from database import execute_query

def execute_signup(password_hash, email, username, role='user'):
    """
    Create a new user and store in the database.
    """
    new_user = {
        'email': email,
        'username': username,
        'password_hash': password_hash,
        'role': role
    }
    execute_query(
        "INSERT INTO users (email, username, password_hash, role) VALUES (%s, %s, %s, %s)",
        (email, username, password_hash, role)
    )
    return new_user

def get_user(key=None, value=None):
    """
    Retrieve user(s) from the database.
    If key is None, return all users.
    If key is provided, return the first user matching the key/value.
    """
    if key is None:
        queries = execute_query("SELECT * FROM users", fetch=True)
    else:
        queries = execute_query(
            f"SELECT * FROM users WHERE {key} = %s",
            (value,),
            fetch=True
        )
    users = [
        {
            'id': query[0],
            'email': query[1],
            'username': query[2],
            'password_hash': query[3],
            'role': query[4]
        }
        for query in queries
    ]
    return users if not key else users[0]
