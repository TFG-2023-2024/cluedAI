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
    return archetypes

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

def randomize_items(items_collection, locations_ids):
    """
    Randomizes the list of items and assigns random location IDs from the provided list.

    Args:
    - items_collection (pymongo.collection.Collection): The MongoDB collection containing item documents.
    - locations_ids (list): List of location IDs to choose from.

    Returns:
    - randomized_items (list): Randomized list of item documents with random location IDs assigned.
    """
    try:
        # Fetch all items from the items collection
        all_items = list(items_collection.find())

        # Randomly shuffle the list of items
        random.shuffle(all_items)

        # Assign a random location ID to each item
        randomized_items = []
        for item in all_items:
            # Randomly select a location ID
            random_location_id = random.choice(locations_ids)
            # Assign the random location ID to the item
            item["Location"] = random_location_id
            randomized_items.append(item)

        return randomized_items
    except Exception as e:
        print(f"Error randomizing items: {e}")
        return []
    