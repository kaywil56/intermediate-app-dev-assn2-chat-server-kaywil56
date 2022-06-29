class User:
    """A user class for storing imortant client data"""
    def __init__(self):
        """Default user values on creation."""
        self.username = None
        self.last_read = None
        self.is_logged_in = False