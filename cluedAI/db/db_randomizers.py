import random

def randomize_archetypes(characters_collection):
    """
    Randomizes the list of character archetypes.

    Args:
    - characters_collection (pymongo.collection.Collection): The MongoDB collection containing character documents.

    Returns:
    - randomized_archetypes (list): Randomized list of character archetypes.
    """
    characters = list(characters_collection.find({}, {"Archetype": 1}))  # Fetching archetype data from MongoDB
    archetypes = [character["Archetype"] for character in characters]
    random.shuffle(archetypes)
    try:
        # Update each document in characters_collection with a random archetype
        for index, character in enumerate(characters_collection.find()):
            random_archetype = archetypes[index]  # Get random archetype
            characters_collection.update_one(
                {"_id": character["_id"]},
                {"$set": {"Archetype": random_archetype}}
            )
    except Exception as e:
        print(f"Error updating character archetypes: {e}")

def randomize_locations(locations_collection):
    """
    Randomly selects 10 location IDs from the provided collection.

    Args:
    - locations_collection (pymongo.collection.Collection): The MongoDB collection containing location documents.

    Returns:
    - random_location_ids (list): List of 10 random location IDs.
    """
    try:
        # Fetch all location IDs from the locations collection
        all_location_ids = [location["_id"] for location in locations_collection.find({}, {"_id": 1})]

        # Randomly shuffle the list of location IDs
        random.shuffle(all_location_ids)

        # Select the first 10 location IDs
        random_location_ids = all_location_ids[:10]

        return random_location_ids
    except Exception as e:
        print(f"Error randomizing locations: {e}")
        return []

def randomize_items(items_collection, locations_collection, locations_ids):
    """
    Randomizes the list of items and assigns random location IDs from the provided list.
    Updates the corresponding location documents with the item IDs.

    Args:
    - items_collection (pymongo.collection.Collection): The MongoDB collection containing item documents.
    - locations_collection (pymongo.collection.Collection): The MongoDB collection containing location documents.
    - locations_ids (list): List of location IDs to choose from.
    """
    try:
        # Clear existing item references in all locations
        locations_collection.update_many({}, {"$set": {"Items": []}})

        for item in items_collection.find():
            # Randomly select a location ID
            random_location_id = random.choice(locations_ids)
            # Assign the random location ID to the item
            items_collection.update_one({"_id": item["_id"]}, {"$set": {"Location": random_location_id}})
            # Update the corresponding location with the item ID
            locations_collection.update_one(
                {"_id": random_location_id},
                {"$push": {"Items": item["_id"]}}
            )
    
        return None
    except Exception as e:
        print(f"Error randomizing items: {e}")
        return []
    
