"""Constanten voor Houtbeheer."""
DOMAIN = "houtbeheer"
PLATFORMS = ["sensor", "select", "number", "button", "binary_sensor", "switch", "date"]
DEFAULT_SHEDS = 12
NO_WOOD_TYPE = "Geen houtsoort"
WOOD_TYPES = [NO_WOOD_TYPE, "Den", "Eik", "Beuk", "Laurier", "Kastanje", "Es", "Haagbeuk", "Berk", "Appel", "Acacia", "Esdoorn", "Spar", "Populier", "Wilg", "Anders"]
CONF_SHEDS = "sheds"
STORAGE_VERSION = 1
