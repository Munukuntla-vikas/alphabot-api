from data_store import get_influencers

def check_influencer_mentions(group_id, message):
    """Check if a message contains an influencer's name for a specific group."""
    influencers = get_influencers(group_id)
    detected = [name for name in influencers if name.lower() in message.lower()]
    return detected if detected else None
