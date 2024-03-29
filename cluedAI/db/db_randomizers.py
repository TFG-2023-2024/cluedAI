import pymongo
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