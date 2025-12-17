"""Word list for seed word generation.

Contains common English nouns suitable for word association games.
Words are selected for:
- High frequency in everyday usage
- Concrete meanings (easier to associate)
- Single words (no phrases)
"""

import random

# Common nouns suitable for word association games
# Roughly ordered by frequency/commonality
COMMON_NOUNS: tuple[str, ...] = (
    # People & relationships
    "person", "people", "man", "woman", "child", "baby", "friend", "family",
    "mother", "father", "parent", "brother", "sister", "doctor", "teacher",
    "student", "worker", "artist", "leader", "king", "queen", "hero",
    # Animals
    "dog", "cat", "bird", "fish", "horse", "cow", "pig", "chicken", "duck",
    "lion", "tiger", "bear", "elephant", "monkey", "snake", "spider", "bee",
    "butterfly", "whale", "shark", "dolphin", "wolf", "fox", "rabbit", "mouse",
    # Nature
    "tree", "flower", "grass", "plant", "leaf", "forest", "garden", "park",
    "mountain", "river", "lake", "ocean", "sea", "beach", "island", "desert",
    "sky", "cloud", "rain", "snow", "sun", "moon", "star", "earth", "wind",
    # Food & drink
    "food", "water", "milk", "bread", "meat", "fruit", "apple", "orange",
    "banana", "grape", "lemon", "tomato", "potato", "carrot", "onion", "rice",
    "pasta", "pizza", "burger", "sandwich", "cake", "cookie", "candy", "cheese",
    "egg", "butter", "salt", "sugar", "coffee", "tea", "juice", "wine", "beer",
    # Body parts
    "head", "face", "eye", "nose", "mouth", "ear", "hair", "hand", "finger",
    "arm", "leg", "foot", "heart", "brain", "blood", "bone", "skin", "tooth",
    # Objects & things
    "thing", "object", "stuff", "box", "bag", "bottle", "cup", "glass", "plate",
    "bowl", "spoon", "fork", "knife", "table", "chair", "bed", "door", "window",
    "wall", "floor", "roof", "room", "house", "home", "building", "tower",
    "bridge", "road", "street", "car", "bus", "train", "plane", "boat", "ship",
    "wheel", "engine", "machine", "tool", "hammer", "key", "lock", "bell",
    "clock", "watch", "phone", "camera", "computer", "screen", "button",
    # Clothing
    "clothes", "shirt", "pants", "dress", "coat", "jacket", "hat", "shoe",
    "sock", "glove", "belt", "pocket", "button", "zipper",
    # Materials
    "wood", "metal", "stone", "rock", "glass", "plastic", "paper", "cloth",
    "leather", "gold", "silver", "iron", "steel", "diamond", "cotton", "wool",
    # Abstract but common
    "time", "day", "night", "morning", "evening", "week", "month", "year",
    "moment", "second", "minute", "hour", "place", "space", "area", "point",
    "line", "circle", "square", "shape", "color", "light", "dark", "shadow",
    "sound", "noise", "music", "song", "voice", "word", "name", "number",
    "letter", "book", "page", "story", "news", "picture", "photo", "movie",
    "game", "sport", "ball", "goal", "team", "player", "winner", "prize",
    # Concepts
    "idea", "thought", "dream", "memory", "feeling", "love", "hope", "fear",
    "anger", "joy", "peace", "war", "fight", "power", "energy", "force",
    "magic", "secret", "truth", "lie", "joke", "question", "answer", "problem",
    # Work & money
    "work", "job", "money", "price", "cost", "bank", "store", "shop", "market",
    "office", "company", "business", "product", "service", "deal", "trade",
    # Education & knowledge
    "school", "class", "lesson", "test", "science", "math", "history", "art",
    "language", "english", "knowledge", "skill", "practice", "example",
    # Health & medicine
    "health", "medicine", "hospital", "pain", "disease", "virus", "cure",
    # Events & activities
    "party", "meeting", "trip", "travel", "vacation", "adventure", "event",
    "show", "concert", "dance", "wedding", "birthday", "holiday", "christmas",
    # Weather & elements
    "weather", "storm", "thunder", "lightning", "fire", "flame", "smoke", "ice",
    # Miscellaneous common nouns
    "air", "dirt", "dust", "mud", "oil", "gas", "fuel", "gift", "present",
    "surprise", "chance", "luck", "risk", "danger", "safety", "rule", "law",
    "crime", "police", "army", "weapon", "gun", "sword", "battle", "victory",
    "flag", "sign", "symbol", "mark", "note", "message", "letter", "card",
    "map", "path", "way", "direction", "distance", "speed", "weight", "size",
    "edge", "corner", "center", "middle", "top", "bottom", "side", "front",
    "back", "end", "start", "beginning", "finish", "goal", "target", "result",
)


def get_seed_words() -> tuple[str, str]:
    """Get two random different seed words for a game.

    Returns:
        Tuple of two different words from the common nouns list.
    """
    words = random.sample(COMMON_NOUNS, 2)
    return (words[0], words[1])
