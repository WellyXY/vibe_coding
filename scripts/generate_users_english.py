#!/usr/bin/env python3
"""
Generate English-only user database
"""

import json
import random
from typing import List, Dict

# English-only data
FIRST_NAMES = [
    "Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason", "Isabella", "William",
    "Mia", "James", "Charlotte", "Benjamin", "Amelia", "Lucas", "Harper", "Henry", "Evelyn", "Alexander",
    "Abigail", "Michael", "Emily", "Daniel", "Elizabeth", "Matthew", "Sofia", "Jackson", "Avery", "Sebastian",
    "Ella", "David", "Madison", "Joseph", "Scarlett", "Carter", "Victoria", "Owen", "Aria", "Wyatt",
    "Grace", "John", "Chloe", "Jack", "Camila", "Luke", "Penelope", "Jayden", "Riley", "Dylan",
    "Lily", "Ryan", "Layla", "Nathan", "Zoey", "Isaac", "Nora", "Gabriel", "Hannah", "Anthony",
    "Audrey", "Samuel", "Brooklyn", "Christopher", "Bella", "Joshua", "Claire", "Andrew", "Skylar", "Mateo"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee",
    "Thompson", "White", "Harris", "Clark", "Lewis", "Robinson", "Walker", "Young", "Allen", "King"
]

OCCUPATIONS = [
    "Software Engineer", "Product Manager", "UX Designer", "Data Scientist", "Marketing Manager",
    "Teacher", "Doctor", "Nurse", "Lawyer", "Accountant", "Artist", "Writer", "Photographer",
    "Chef", "Entrepreneur", "Consultant", "Sales Manager", "HR Manager", "Financial Analyst",
    "UI Designer", "Full Stack Developer", "DevOps Engineer", "Project Manager", "Business Analyst",
    "Content Creator", "Social Media Manager", "Graphic Designer", "Student", "Researcher", "Architect"
]

LOCATIONS = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego",
    "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", "Indianapolis",
    "San Francisco", "Seattle", "Denver", "Boston", "Nashville", "Portland", "Las Vegas", "Detroit", "Miami"
]

HOBBIES = [
    "Photography", "Travel", "Reading", "Cooking", "Sports", "Music", "Painting", "Writing", "Movies", "Hiking",
    "Swimming", "Yoga", "Running", "Cycling", "Camping", "Coffee", "Wine Tasting", "Gardening", "Pets", "Crafts",
    "Programming", "Gaming", "Dancing", "Singing", "Fitness", "Basketball", "Tennis", "Golf", "Meditation", "Surfing"
]

GENDERS = ["Male", "Female", "Non-binary"]

def generate_user(user_id: int) -> Dict:
    """Generate single user data"""
    gender = random.choice(GENDERS)
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)

    # Random 2-4 hobbies
    num_hobbies = random.randint(2, 4)
    hobbies = random.sample(HOBBIES, num_hobbies)

    user = {
        "id": user_id,
        "name": f"{first_name} {last_name}",
        "age": random.randint(20, 65),
        "occupation": random.choice(OCCUPATIONS),
        "location": random.choice(LOCATIONS),
        "hobby": hobbies,
        "gender": gender,
        "image": f"avatars/avatar_{user_id:03d}.jpg"
    }

    return user

def generate_user_database(num_users: int = 100) -> List[Dict]:
    """Generate user database"""
    users = []
    for i in range(1, num_users + 1):
        users.append(generate_user(i))
    return users

def main():
    print("Generating 100 users with English-only data...")
    users = generate_user_database(100)

    output_file = "users_database.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    print(f"✅ Successfully generated {len(users)} users!")
    print(f"📁 Saved to: {output_file}")

    # Statistics
    locations = {}
    genders = {}
    occupations = {}

    for user in users:
        locations[user['location']] = locations.get(user['location'], 0) + 1
        genders[user['gender']] = genders.get(user['gender'], 0) + 1
        occupations[user['occupation']] = occupations.get(user['occupation'], 0) + 1

    print(f"\nLocation distribution: {dict(sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5])}")
    print(f"Gender distribution: {genders}")
    print(f"Occupation distribution: {dict(sorted(occupations.items(), key=lambda x: x[1], reverse=True)[:5])}")

    # Show first 3 users
    print("\nFirst 3 users:")
    for user in users[:3]:
        print(f"\n{user['id']}. {user['name']}")
        print(f"   Age: {user['age']}")
        print(f"   Occupation: {user['occupation']}")
        print(f"   Location: {user['location']}")
        print(f"   Hobbies: {', '.join(user['hobby'])}")
        print(f"   Gender: {user['gender']}")

if __name__ == "__main__":
    main()
