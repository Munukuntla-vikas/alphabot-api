import json

DATA_FILE = "group_data.json"

# Initialize data store if file does not exist
try:
    with open(DATA_FILE, "r") as f:
        group_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    group_data = {}  # Empty dict if file does not exist

def save_data():
    """Save group data to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(group_data, f, indent=4)

def set_influencers(group_id, influencers):
    """Set influencers for a specific group."""
    if group_id not in group_data:
        group_data[group_id] = {"influencers": [], "messages": []}
    group_data[group_id]["influencers"] = influencers
    save_data()

def get_influencers(group_id):
    """Get influencers for a specific group."""
    return group_data.get(group_id, {}).get("influencers", [])

def save_message(group_id, message):
    """Save message for a group to track trending topics."""
    if group_id not in group_data:
        group_data[group_id] = {"influencers": [], "messages": []}
    group_data[group_id]["messages"].append(message)
    save_data()

def get_messages(group_id):
    """Get messages for a group."""
    return group_data.get(group_id, {}).get("messages", [])
