from database import insert_user

def create_user_service(name: str):
    # some business logic
    processed_name = name.strip().upper()
    return insert_user(processed_name)
