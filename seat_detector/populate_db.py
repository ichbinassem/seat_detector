import random
import string
from queuing_app.models import Restaurant  # Replace 'your_app_name' with the name of your app

def generate_random_code(length=6):
    """Generate a random code consisting of letters and numbers."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def populate_database():
    for i in range(10):
        name = f"Restaurant {i+1}"
        code = generate_random_code()
        
        # Ensure the code is unique
        while Restaurant.objects.filter(code=code).exists():
            code = generate_random_code()
        
        Restaurant.objects.create(name=name, code=code)
        print(f"Added {name} with code {code}")

if __name__ == "__main__":
    populate_database()
