def insert_user(name: str):
    # Mock database insert
    print(f"Executing INSERT query for {name}")
    db_commit()
    return {"id": 1, "name": name}

def db_commit():
    print("MOCK COMMIT")
