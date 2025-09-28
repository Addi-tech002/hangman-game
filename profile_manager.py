import json
import os

FILE = "users.json"

def load_users():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    with open(FILE, 'w') as file:
        json.dump(users, file, indent=4)

def create_profile(username):
    users = load_users()
    if username not in users:
        users[username] = {
            "matches_played": 0,
            "wins": 0,
            "losses": 0,
            "challenges_attempted": 0,
            "challenge_score": 0,
            "high_score": 0
        }
        save_users(users)
    return users[username]

def update_stats(username, win=False, challenge=False, score=0):
    users = load_users()
    user = users[username]
    user["matches_played"] += 1
    if win:
        user["wins"] += 1
    else:
        user["losses"] += 1
    if challenge:
        user["challenges_attempted"] += 1
        user["challenge_score"] += score
    if score > user["high_score"]:
        user["high_score"] = score
    users[username] = user
    save_users(users)

def get_user_stats(username):
    users = load_users()
    if username not in users:
        create_profile(username)  # Ensure user is created
        users = load_users()      # Reload to reflect the new user
    return users[username]
