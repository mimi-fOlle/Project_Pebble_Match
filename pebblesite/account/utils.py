import secrets
import string
import os

def generate_random_user_id(user_id):
    """
    Generate a random user ID that is not equal to the given user ID.
    """
    while True:
        # Generate 4 random bytes
        random_bytes = os.urandom(4)

        # Convert the bytes to an integer
        random_int = int.from_bytes(random_bytes, byteorder='big')

        # Make sure the generated user ID is not equal to the given user ID
        if random_int != user_id:
            return random_int