"""User model and database operations."""
# User data model and database interactions

class User:
    """User model."""
    def __init__(self, user_id, username, first_name):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.created_at = None
        self.updated_at = None
