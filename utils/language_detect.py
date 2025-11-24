def detect_language(text):
    """Detect Hindi or English text automatically"""
    if any("\u0900" <= c <= "\u097F" for c in text):
        return "hindi"
    else:
        return "english"
