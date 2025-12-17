"""Word list for seed word generation.

Provides two word sources:
1. COMMON_NOUNS: ~250 common nouns (original, may be too easy)
2. DICTIONARY_WORDS: ~30k filtered words from system dictionary (harder)

Factorial design support: generate triplets of words that create
controlled pair combinations for rigorous benchmarking.
"""

import random
from functools import lru_cache
from pathlib import Path


# Common nouns suitable for word association games (ORIGINAL - may be too easy)
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


# Expanded word list: ~1000 common English words across diverse categories
# Designed to create challenging but fair word associations
DIVERSE_WORDS: tuple[str, ...] = (
    # Abstract concepts
    "truth", "freedom", "justice", "peace", "chaos", "order", "balance",
    "power", "wisdom", "courage", "faith", "doubt", "hope", "fear", "love",
    "hate", "anger", "joy", "sorrow", "pride", "shame", "guilt", "trust",
    "honor", "glory", "destiny", "fate", "luck", "chance", "risk", "choice",
    "change", "growth", "decay", "birth", "death", "life", "soul", "spirit",
    "mind", "heart", "thought", "dream", "memory", "idea", "theory", "fact",
    "myth", "legend", "story", "history", "future", "past", "present", "time",
    # Science & technology
    "atom", "cell", "gene", "virus", "bacteria", "protein", "enzyme", "acid",
    "carbon", "oxygen", "nitrogen", "hydrogen", "electron", "photon", "wave",
    "particle", "energy", "force", "gravity", "magnet", "electric", "nuclear",
    "laser", "radar", "sonar", "robot", "computer", "software", "hardware",
    "network", "internet", "data", "code", "algorithm", "binary", "digital",
    "analog", "signal", "frequency", "spectrum", "radiation", "quantum",
    # Geography & places
    "mountain", "valley", "canyon", "plateau", "island", "peninsula", "coast",
    "shore", "beach", "cliff", "cave", "glacier", "volcano", "desert", "jungle",
    "forest", "prairie", "swamp", "marsh", "river", "stream", "lake", "pond",
    "ocean", "sea", "bay", "gulf", "strait", "channel", "harbor", "port",
    "city", "town", "village", "suburb", "district", "region", "country",
    "continent", "border", "frontier", "capital", "province", "state",
    # Architecture & structures
    "tower", "castle", "palace", "temple", "church", "mosque", "pyramid",
    "monument", "statue", "fountain", "bridge", "tunnel", "dam", "canal",
    "wall", "fence", "gate", "door", "window", "roof", "floor", "ceiling",
    "column", "arch", "dome", "staircase", "elevator", "corridor", "lobby",
    "basement", "attic", "balcony", "terrace", "garden", "courtyard",
    # Transportation
    "wheel", "axle", "engine", "motor", "fuel", "gasoline", "diesel", "battery",
    "car", "truck", "bus", "taxi", "train", "subway", "tram", "bicycle",
    "motorcycle", "boat", "ship", "ferry", "yacht", "submarine", "airplane",
    "helicopter", "rocket", "satellite", "parachute", "balloon", "glider",
    # Food & cuisine
    "bread", "rice", "pasta", "noodle", "flour", "wheat", "corn", "barley",
    "oat", "bean", "lentil", "pea", "potato", "tomato", "onion", "garlic",
    "pepper", "carrot", "cabbage", "lettuce", "spinach", "broccoli", "mushroom",
    "apple", "orange", "banana", "grape", "lemon", "lime", "mango", "peach",
    "cherry", "berry", "melon", "coconut", "pineapple", "olive", "avocado",
    "beef", "pork", "chicken", "lamb", "fish", "shrimp", "lobster", "crab",
    "cheese", "butter", "cream", "yogurt", "honey", "sugar", "salt", "vinegar",
    "chocolate", "vanilla", "cinnamon", "ginger", "curry", "sauce", "soup",
    # Animals
    "elephant", "giraffe", "zebra", "lion", "tiger", "leopard", "cheetah",
    "wolf", "fox", "bear", "deer", "moose", "elk", "buffalo", "rhino",
    "hippo", "gorilla", "monkey", "ape", "kangaroo", "koala", "panda",
    "eagle", "hawk", "falcon", "owl", "crow", "raven", "parrot", "penguin",
    "swan", "duck", "goose", "turkey", "chicken", "peacock", "flamingo",
    "shark", "whale", "dolphin", "seal", "walrus", "octopus", "squid",
    "crab", "lobster", "shrimp", "jellyfish", "starfish", "coral", "turtle",
    "snake", "lizard", "crocodile", "frog", "toad", "salamander", "spider",
    "scorpion", "beetle", "butterfly", "moth", "bee", "wasp", "ant", "termite",
    # Plants
    "tree", "shrub", "bush", "vine", "grass", "moss", "fern", "palm",
    "oak", "maple", "pine", "cedar", "birch", "willow", "bamboo", "cactus",
    "flower", "rose", "lily", "tulip", "orchid", "daisy", "sunflower",
    "violet", "iris", "lotus", "poppy", "jasmine", "lavender", "herb",
    "mint", "basil", "thyme", "sage", "rosemary", "parsley", "cilantro",
    # Materials & substances
    "wood", "metal", "stone", "rock", "sand", "clay", "glass", "plastic",
    "rubber", "leather", "fabric", "cotton", "wool", "silk", "linen", "velvet",
    "gold", "silver", "bronze", "copper", "iron", "steel", "aluminum", "tin",
    "diamond", "ruby", "emerald", "sapphire", "pearl", "crystal", "marble",
    "granite", "concrete", "cement", "brick", "tile", "porcelain", "ceramic",
    # Weather & climate
    "sun", "moon", "star", "cloud", "rain", "snow", "hail", "sleet",
    "fog", "mist", "dew", "frost", "ice", "wind", "breeze", "gust",
    "storm", "thunder", "lightning", "tornado", "hurricane", "typhoon",
    "flood", "drought", "heat", "cold", "freeze", "thaw", "rainbow",
    # Music & arts
    "music", "song", "melody", "rhythm", "beat", "tempo", "harmony", "chord",
    "note", "scale", "octave", "pitch", "tone", "bass", "treble", "soprano",
    "guitar", "piano", "violin", "cello", "flute", "trumpet", "drum", "harp",
    "orchestra", "band", "choir", "opera", "symphony", "concert", "album",
    "paint", "brush", "canvas", "sketch", "portrait", "landscape", "sculpture",
    "pottery", "mosaic", "mural", "gallery", "museum", "theater", "cinema",
    # Sports & games
    "ball", "bat", "racket", "stick", "club", "net", "goal", "hoop",
    "court", "field", "track", "pool", "ring", "arena", "stadium",
    "soccer", "football", "basketball", "baseball", "tennis", "golf", "hockey",
    "cricket", "rugby", "volleyball", "boxing", "wrestling", "swimming",
    "diving", "skiing", "skating", "surfing", "sailing", "archery", "fencing",
    "chess", "poker", "dice", "cards", "puzzle", "maze", "riddle",
    # Occupations
    "doctor", "nurse", "surgeon", "dentist", "pharmacist", "therapist",
    "lawyer", "judge", "police", "soldier", "pilot", "sailor", "captain",
    "teacher", "professor", "scientist", "engineer", "architect", "designer",
    "artist", "musician", "actor", "writer", "journalist", "photographer",
    "chef", "baker", "farmer", "gardener", "carpenter", "plumber", "electrician",
    "mechanic", "driver", "pilot", "merchant", "banker", "accountant",
    # Clothing & accessories
    "shirt", "pants", "dress", "skirt", "jacket", "coat", "sweater", "vest",
    "suit", "tie", "scarf", "glove", "hat", "cap", "helmet", "crown",
    "shoe", "boot", "sandal", "slipper", "sock", "belt", "buckle", "button",
    "zipper", "pocket", "collar", "sleeve", "cuff", "hem", "seam", "patch",
    "ring", "bracelet", "necklace", "earring", "watch", "glasses", "umbrella",
    # Tools & equipment
    "hammer", "nail", "screw", "bolt", "nut", "wrench", "pliers", "drill",
    "saw", "blade", "chisel", "file", "sandpaper", "glue", "tape", "rope",
    "chain", "hook", "pulley", "lever", "gear", "spring", "hinge", "lock",
    "key", "switch", "button", "dial", "gauge", "meter", "scale", "ruler",
    "compass", "level", "clamp", "vice", "anvil", "forge", "furnace",
    # Furniture & household
    "table", "chair", "bench", "stool", "sofa", "couch", "bed", "mattress",
    "pillow", "blanket", "sheet", "curtain", "carpet", "rug", "lamp", "candle",
    "mirror", "clock", "vase", "frame", "shelf", "drawer", "cabinet", "closet",
    "desk", "bookcase", "wardrobe", "dresser", "nightstand", "headboard",
    # Kitchen items
    "pot", "pan", "skillet", "wok", "kettle", "teapot", "coffeepot", "pitcher",
    "bowl", "plate", "dish", "cup", "mug", "glass", "bottle", "jar",
    "fork", "knife", "spoon", "chopstick", "ladle", "spatula", "whisk", "grater",
    "blender", "mixer", "toaster", "oven", "stove", "microwave", "fridge",
    # Body parts (expanded)
    "head", "face", "forehead", "temple", "cheek", "chin", "jaw", "neck",
    "shoulder", "arm", "elbow", "wrist", "hand", "palm", "finger", "thumb",
    "chest", "back", "spine", "hip", "waist", "belly", "navel", "rib",
    "leg", "thigh", "knee", "calf", "ankle", "foot", "heel", "toe",
    "eye", "eyebrow", "eyelash", "pupil", "iris", "retina", "cornea",
    "ear", "earlobe", "eardrum", "nose", "nostril", "mouth", "lip", "tongue",
    "tooth", "gum", "throat", "larynx", "lung", "heart", "liver", "kidney",
    "stomach", "intestine", "bladder", "muscle", "tendon", "ligament", "bone",
    "skull", "rib", "pelvis", "femur", "tibia", "spine", "vertebra",
    "skin", "pore", "hair", "nail", "vein", "artery", "nerve", "brain",
    # Military & conflict
    "sword", "shield", "spear", "arrow", "bow", "axe", "dagger", "lance",
    "cannon", "rifle", "pistol", "bullet", "bomb", "grenade", "missile",
    "tank", "warship", "fighter", "bomber", "submarine", "aircraft",
    "army", "navy", "marine", "soldier", "general", "admiral", "sergeant",
    "battle", "war", "peace", "treaty", "alliance", "enemy", "ally", "truce",
    # Religion & mythology
    "god", "goddess", "angel", "demon", "devil", "saint", "prophet", "priest",
    "temple", "church", "mosque", "synagogue", "shrine", "altar", "prayer",
    "heaven", "hell", "paradise", "purgatory", "karma", "soul", "spirit",
    "miracle", "blessing", "curse", "prophecy", "revelation", "scripture",
    "dragon", "phoenix", "unicorn", "griffin", "mermaid", "giant", "dwarf",
    "wizard", "witch", "fairy", "elf", "troll", "goblin", "vampire", "werewolf",
    # Academic subjects
    "math", "algebra", "geometry", "calculus", "statistics", "physics",
    "chemistry", "biology", "geology", "astronomy", "ecology", "botany",
    "zoology", "anatomy", "psychology", "sociology", "anthropology",
    "history", "geography", "economics", "politics", "philosophy", "ethics",
    "logic", "rhetoric", "grammar", "literature", "poetry", "drama", "fiction",
    # Emotions & states
    "happy", "sad", "angry", "afraid", "surprised", "disgusted", "calm",
    "excited", "bored", "tired", "awake", "asleep", "hungry", "thirsty",
    "hot", "cold", "warm", "cool", "wet", "dry", "clean", "dirty",
    "healthy", "sick", "strong", "weak", "fast", "slow", "loud", "quiet",
    # Actions (verbs as nouns)
    "jump", "run", "walk", "climb", "swim", "fly", "dive", "fall",
    "push", "pull", "lift", "drop", "throw", "catch", "kick", "punch",
    "cut", "slice", "chop", "tear", "break", "bend", "fold", "wrap",
    "open", "close", "lock", "unlock", "tie", "untie", "connect", "disconnect",
    # Miscellaneous
    "shadow", "echo", "silence", "noise", "signal", "symbol", "sign", "mark",
    "pattern", "texture", "shape", "form", "color", "shade", "tint", "hue",
    "edge", "corner", "center", "middle", "top", "bottom", "side", "front",
    "back", "inside", "outside", "surface", "depth", "height", "width", "length",
    "weight", "mass", "volume", "density", "pressure", "temperature", "speed",
    "distance", "angle", "curve", "line", "point", "circle", "square", "triangle",
)


def load_dictionary_words() -> tuple[str, ...]:
    """Load diverse word list for challenging benchmarks.

    Returns a curated list of ~1000 common English words spanning
    many categories, designed to create challenging but fair
    word association pairs.

    Returns:
        Tuple of diverse common English words.
    """
    return DIVERSE_WORDS


# Word frequency weights (Zipf-like distribution)
# Higher tier = more common. Used for weighted sampling.
# Tiers: 5=very common, 4=common, 3=moderate, 2=less common, 1=uncommon
WORD_FREQUENCY_TIERS: dict[str, int] = {
    # Tier 5 - Very common (everyday words)
    **{w: 5 for w in [
        "time", "life", "day", "man", "world", "way", "year", "work", "water",
        "money", "home", "hand", "school", "place", "room", "mother", "father",
        "child", "book", "word", "name", "food", "city", "car", "door", "house",
        "tree", "sun", "night", "head", "face", "eye", "heart", "mind", "love",
        "family", "friend", "game", "story", "music", "phone", "table", "chair",
        "bed", "window", "street", "road", "sky", "fire", "dog", "cat", "bird",
        "fish", "flower", "rain", "snow", "wind", "color", "light", "sound",
        "ball", "box", "cup", "key", "ring", "shoe", "hat", "coat", "shirt",
    ]},
    # Tier 4 - Common
    **{w: 4 for w in [
        "truth", "power", "change", "death", "peace", "war", "dream", "hope",
        "fear", "anger", "joy", "memory", "idea", "history", "future", "past",
        "mountain", "river", "ocean", "forest", "island", "beach", "lake",
        "bridge", "tower", "wall", "gate", "garden", "train", "boat", "ship",
        "wheel", "engine", "bread", "rice", "meat", "cheese", "apple", "orange",
        "chicken", "wolf", "bear", "horse", "lion", "snake", "grass", "stone",
        "gold", "silver", "iron", "glass", "wood", "paper", "cloud", "star",
        "moon", "storm", "song", "dance", "paint", "doctor", "teacher", "king",
        "queen", "soldier", "judge", "farm", "shop", "bank", "church", "castle",
        "knife", "gun", "sword", "battle", "army", "god", "angel", "devil",
        "magic", "ghost", "king", "queen", "prince", "math", "science", "art",
    ]},
    # Tier 3 - Moderate
    **{w: 3 for w in [
        "freedom", "justice", "wisdom", "courage", "faith", "doubt", "pride",
        "shame", "guilt", "honor", "glory", "destiny", "fate", "soul", "spirit",
        "theory", "myth", "legend", "atom", "cell", "virus", "energy", "force",
        "gravity", "computer", "network", "data", "code", "valley", "canyon",
        "glacier", "volcano", "desert", "jungle", "swamp", "harbor", "port",
        "palace", "temple", "mosque", "pyramid", "monument", "statue", "fountain",
        "tunnel", "dam", "canal", "column", "arch", "dome", "elevator", "basement",
        "fuel", "battery", "truck", "taxi", "subway", "bicycle", "motorcycle",
        "yacht", "helicopter", "rocket", "satellite", "flour", "wheat", "garlic",
        "pepper", "mushroom", "grape", "lemon", "mango", "beef", "pork", "lamb",
        "butter", "honey", "chocolate", "elephant", "giraffe", "zebra", "tiger",
        "leopard", "gorilla", "kangaroo", "eagle", "hawk", "owl", "penguin",
        "whale", "dolphin", "shark", "octopus", "turtle", "frog", "spider",
        "butterfly", "bee", "oak", "maple", "pine", "bamboo", "cactus", "rose",
        "copper", "steel", "diamond", "ruby", "marble", "thunder", "lightning",
        "tornado", "hurricane", "flood", "drought", "guitar", "piano", "violin",
        "drum", "orchestra", "symphony", "opera", "canvas", "portrait", "gallery",
        "museum", "soccer", "football", "basketball", "tennis", "golf", "boxing",
        "chess", "nurse", "lawyer", "pilot", "chef", "engineer", "architect",
        "journalist", "photographer", "jacket", "sweater", "helmet", "belt",
        "bracelet", "necklace", "hammer", "drill", "rope", "chain", "hook",
        "compass", "sofa", "lamp", "mirror", "curtain", "carpet", "pot", "pan",
        "bowl", "fork", "spoon", "oven", "shoulder", "elbow", "wrist", "knee",
        "ankle", "throat", "lung", "liver", "muscle", "bone", "brain", "shield",
        "spear", "arrow", "cannon", "rifle", "bomb", "missile", "tank", "navy",
        "general", "treaty", "alliance", "goddess", "demon", "saint", "prophet",
        "priest", "heaven", "hell", "miracle", "curse", "dragon", "wizard",
        "witch", "fairy", "vampire", "algebra", "geometry", "physics", "chemistry",
        "biology", "astronomy", "psychology", "philosophy", "economics", "poetry",
    ]},
    # Tier 2 - Less common
    **{w: 2 for w in [
        "chaos", "order", "balance", "sorrow", "trust", "growth", "decay",
        "birth", "thought", "fact", "present", "gene", "bacteria", "protein",
        "enzyme", "acid", "carbon", "oxygen", "nitrogen", "hydrogen", "electron",
        "photon", "wave", "particle", "magnet", "nuclear", "laser", "radar",
        "sonar", "robot", "software", "hardware", "internet", "algorithm",
        "binary", "digital", "analog", "signal", "frequency", "spectrum",
        "radiation", "quantum", "plateau", "peninsula", "coast", "shore",
        "cliff", "cave", "prairie", "marsh", "stream", "pond", "bay", "gulf",
        "strait", "channel", "suburb", "district", "region", "continent",
        "border", "frontier", "capital", "province", "arch", "staircase",
        "corridor", "lobby", "attic", "balcony", "terrace", "courtyard",
        "axle", "motor", "gasoline", "diesel", "tram", "ferry", "submarine",
        "airplane", "parachute", "balloon", "glider", "pasta", "noodle",
        "barley", "oat", "bean", "lentil", "pea", "cabbage", "lettuce",
        "spinach", "broccoli", "lime", "peach", "cherry", "berry", "melon",
        "coconut", "pineapple", "olive", "avocado", "shrimp", "lobster",
        "crab", "cream", "yogurt", "vinegar", "vanilla", "cinnamon", "ginger",
        "curry", "sauce", "soup", "cheetah", "fox", "deer", "moose", "elk",
        "buffalo", "rhino", "hippo", "ape", "koala", "panda", "falcon",
        "crow", "raven", "parrot", "swan", "goose", "turkey", "peacock",
        "flamingo", "seal", "walrus", "squid", "jellyfish", "starfish",
        "coral", "lizard", "crocodile", "toad", "salamander", "scorpion",
        "beetle", "moth", "wasp", "ant", "termite", "shrub", "bush", "vine",
        "moss", "fern", "palm", "cedar", "birch", "willow", "lily", "tulip",
        "orchid", "daisy", "sunflower", "violet", "iris", "lotus", "poppy",
        "jasmine", "lavender", "herb", "mint", "basil", "thyme", "sage",
        "rosemary", "parsley", "cilantro", "sand", "clay", "plastic",
        "rubber", "leather", "fabric", "cotton", "wool", "silk", "linen",
        "velvet", "bronze", "aluminum", "tin", "emerald", "sapphire", "pearl",
        "crystal", "granite", "concrete", "cement", "brick", "tile", "porcelain",
        "ceramic", "hail", "sleet", "fog", "mist", "dew", "frost", "breeze",
        "gust", "typhoon", "thaw", "rainbow", "melody", "rhythm", "beat",
        "tempo", "harmony", "chord", "note", "scale", "octave", "pitch",
        "tone", "bass", "treble", "soprano", "cello", "flute", "trumpet",
        "harp", "band", "choir", "concert", "album", "brush", "sketch",
        "landscape", "sculpture", "pottery", "mosaic", "mural", "theater",
        "cinema", "bat", "racket", "stick", "club", "net", "hoop", "court",
        "track", "arena", "stadium", "baseball", "hockey", "cricket", "rugby",
        "volleyball", "wrestling", "swimming", "diving", "skiing", "skating",
        "surfing", "sailing", "archery", "fencing", "poker", "dice", "puzzle",
        "maze", "riddle", "surgeon", "dentist", "pharmacist", "therapist",
        "sailor", "captain", "professor", "scientist", "designer", "musician",
        "actor", "writer", "baker", "gardener", "carpenter", "plumber",
        "electrician", "mechanic", "driver", "merchant", "banker", "accountant",
        "pants", "skirt", "vest", "suit", "scarf", "glove", "cap", "crown",
        "boot", "sandal", "slipper", "sock", "buckle", "zipper", "pocket",
        "collar", "sleeve", "cuff", "hem", "seam", "patch", "earring", "glasses",
        "umbrella", "nail", "screw", "bolt", "nut", "wrench", "pliers", "saw",
        "blade", "chisel", "file", "sandpaper", "glue", "tape", "pulley",
        "lever", "gear", "spring", "hinge", "switch", "dial", "gauge", "meter",
        "ruler", "level", "clamp", "vice", "anvil", "forge", "furnace",
        "bench", "stool", "couch", "mattress", "pillow", "blanket", "sheet",
        "candle", "vase", "frame", "shelf", "drawer", "cabinet", "closet",
        "desk", "bookcase", "wardrobe", "dresser", "nightstand", "headboard",
        "skillet", "wok", "kettle", "teapot", "coffeepot", "pitcher", "plate",
        "dish", "mug", "bottle", "jar", "chopstick", "ladle", "spatula",
        "whisk", "grater", "blender", "mixer", "toaster", "stove", "microwave",
        "fridge", "forehead", "cheek", "chin", "jaw", "neck", "palm", "thumb",
        "chest", "spine", "hip", "waist", "belly", "navel", "rib", "thigh",
        "calf", "heel", "toe", "eyebrow", "eyelash", "pupil", "iris", "retina",
        "cornea", "earlobe", "eardrum", "nostril", "lip", "tongue", "gum",
        "larynx", "kidney", "stomach", "intestine", "bladder", "tendon",
        "ligament", "skull", "pelvis", "femur", "tibia", "vertebra", "pore",
        "vein", "artery", "nerve", "dagger", "lance", "pistol", "bullet",
        "grenade", "warship", "fighter", "bomber", "aircraft", "marine",
        "admiral", "sergeant", "enemy", "ally", "truce", "shrine", "altar",
        "prayer", "paradise", "purgatory", "karma", "blessing", "prophecy",
        "revelation", "scripture", "phoenix", "unicorn", "griffin", "mermaid",
        "giant", "dwarf", "elf", "troll", "goblin", "werewolf", "calculus",
        "statistics", "geology", "ecology", "botany", "zoology", "anatomy",
        "sociology", "anthropology", "geography", "politics", "ethics",
        "logic", "rhetoric", "grammar", "literature", "drama", "fiction",
    ]},
}


def get_word_frequency_weight(word: str) -> float:
    """Get frequency weight for a word (higher = more common).

    Uses a curated tier system where:
    - Tier 5: very common (weight 32)
    - Tier 4: common (weight 16)
    - Tier 3: moderate (weight 8)
    - Tier 2: less common (weight 4)
    - Tier 1/default: uncommon (weight 1)

    Returns:
        Float weight for use in weighted sampling.
    """
    tier = WORD_FREQUENCY_TIERS.get(word, 1)
    # Exponential weighting: tier 5 is 32x more likely than tier 1
    return 2 ** tier


def get_seed_words(use_dictionary: bool = False) -> tuple[str, str]:
    """Get two random different seed words for a game.

    Args:
        use_dictionary: If True, use full dictionary (~30k words).
                       If False, use common nouns (~250 words).

    Returns:
        Tuple of two different words.
    """
    word_list = load_dictionary_words() if use_dictionary else COMMON_NOUNS
    words = random.sample(word_list, 2)
    return (words[0], words[1])


def _weighted_sample(
    word_list: tuple[str, ...],
    n: int,
    rng: random.Random,
) -> list[str]:
    """Sample n unique words with frequency weighting.

    Higher-frequency words are more likely to be selected.

    Args:
        word_list: Tuple of words to sample from.
        n: Number of words to sample.
        rng: Random number generator instance.

    Returns:
        List of n unique sampled words.
    """
    weights = [get_word_frequency_weight(w) for w in word_list]
    total_weight = sum(weights)
    probs = [w / total_weight for w in weights]

    # Sample without replacement using weighted probabilities
    available = list(range(len(word_list)))
    available_probs = probs.copy()
    selected = []

    for _ in range(n):
        # Normalize remaining probabilities
        prob_sum = sum(available_probs)
        if prob_sum == 0:
            break
        normalized = [p / prob_sum for p in available_probs]

        # Select one index
        r = rng.random()
        cumulative = 0
        for i, (idx, prob) in enumerate(zip(available, normalized)):
            cumulative += prob
            if r <= cumulative:
                selected.append(word_list[idx])
                # Remove selected item
                available.pop(i)
                available_probs.pop(i)
                break

    return selected


def generate_factorial_pairs(
    num_triplets: int,
    seed: int | None = None,
    use_dictionary: bool = True,
    weighted: bool = True,
) -> list[tuple[str, str]]:
    """Generate word pairs using factorial design.

    For each triplet of words (A, B, C), generates 3 unique pairs:
    - (A, B)
    - (A, C)
    - (B, C)

    This creates controlled variation where the same words appear
    in multiple pairs, enabling analysis of word-specific effects.

    Args:
        num_triplets: Number of word triplets to generate.
                     Total pairs = num_triplets * 3.
        seed: Random seed for reproducibility.
        use_dictionary: If True, use diverse word list (harder).
        weighted: If True, sample words weighted by frequency.

    Returns:
        List of (word1, word2) pairs.

    Example:
        >>> generate_factorial_pairs(2, seed=42)
        [('apple', 'guitar'), ('apple', 'theory'), ('guitar', 'theory'),
         ('bench', 'music'), ('bench', 'planet'), ('music', 'planet')]
    """
    rng = random.Random(seed)

    word_list = load_dictionary_words() if use_dictionary else COMMON_NOUNS

    # Sample enough unique words for all triplets
    num_words_needed = num_triplets * 3
    if num_words_needed > len(word_list):
        raise ValueError(
            f"Need {num_words_needed} unique words but only have {len(word_list)}"
        )

    if weighted:
        sampled_words = _weighted_sample(word_list, num_words_needed, rng)
    else:
        sampled_words = rng.sample(list(word_list), num_words_needed)

    pairs = []
    for i in range(num_triplets):
        # Get triplet
        a = sampled_words[i * 3]
        b = sampled_words[i * 3 + 1]
        c = sampled_words[i * 3 + 2]

        # Generate 3 pairs from triplet
        pairs.append((a, b))
        pairs.append((a, c))
        pairs.append((b, c))

    return pairs


def generate_random_pairs(
    num_pairs: int,
    seed: int | None = None,
    use_dictionary: bool = True,
    weighted: bool = True,
) -> list[tuple[str, str]]:
    """Generate random word pairs (no factorial structure).

    Args:
        num_pairs: Number of pairs to generate.
        seed: Random seed for reproducibility.
        use_dictionary: If True, use diverse word list (harder).
        weighted: If True, sample words weighted by frequency.

    Returns:
        List of (word1, word2) pairs, all words unique.
    """
    rng = random.Random(seed)

    word_list = load_dictionary_words() if use_dictionary else COMMON_NOUNS

    num_words_needed = num_pairs * 2
    if num_words_needed > len(word_list):
        raise ValueError(
            f"Need {num_words_needed} unique words but only have {len(word_list)}"
        )

    if weighted:
        sampled_words = _weighted_sample(word_list, num_words_needed, rng)
    else:
        sampled_words = rng.sample(list(word_list), num_words_needed)

    pairs = []
    for i in range(num_pairs):
        pairs.append((sampled_words[i * 2], sampled_words[i * 2 + 1]))

    return pairs
