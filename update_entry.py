
def update_participant_entry(participant_id, post,collection):
    try:
        existing_participant = collection.find_one({"_id": participant_id})
        if existing_participant:
            entries = existing_participant.get("entries", [])
            # Check if the post already exists in the entries
            if post not in entries:
                entries.append(post)
                collection.update_one({"_id": participant_id}, {"$set": {"entries": entries}})
                return True  # Post added successfully
            else:
                return False  # Post already exists
        else:
            new_participant = {"_id": participant_id, "entries": [post]}
            collection.insert_one(new_participant)
            return True  # Post added successfully
    except Exception as e:
        print(f'Error updating participant entry: {e}')
        return False  # Post not added due to error