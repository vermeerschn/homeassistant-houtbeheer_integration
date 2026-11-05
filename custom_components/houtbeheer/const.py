"""Constanten voor Houtbeheer."""
DOMAIN = "houtbeheer"
PLATFORMS = ["sensor", "number", "button", "binary_sensor", "switch", "date"]
DEFAULT_SHEDS = 12
NO_WOOD_TYPE = "Geen houtsoort"  # weergave voor een hok zonder gekozen houtsoorten
DEFAULT_WOOD_TYPES = ["Den", "Eik", "Beuk", "Laurier", "Kastanje", "Es", "Haagbeuk", "Berk", "Appel", "Acacia", "Esdoorn", "Spar", "Populier", "Wilg", "Anders"]
ATTR_WOOD_TYPES = "houtsoorten"
ATTR_WOOD_OPTIONS = "opties"
ATTR_MEASUREMENTS = "metingen"
HISTORY_SIZE = 5
SERVICE_SET_WOOD_TYPES = "set_wood_types"
CONF_SHEDS = "sheds"
CONF_WOOD_TYPES = "wood_types"
MAX_WOOD_TYPES = 50
MAX_WOOD_NAME_LENGTH = 30
STORAGE_VERSION = 1
