DOMAIN = "meteored"

# ==========================================================
# =============== MAPPATURA SIMBOLI METEO ==================
# ==========================================================
# La chiave "symbol" arriva dall'API Meteored
# Ogni simbolo viene tradotto in:
# - code: valore numerico ufficiale
# - description: descrizione testuale

SYMBOLS_MAP = {
    1: {"code": 1, "description": "Sereno"},
    2: {"code": 2, "description": "Poco nuvoloso"},
    3: {"code": 3, "description": "Parzialmente nuvoloso"},
    4: {"code": 4, "description": "Nuvoloso"},
    5: {"code": 5, "description": "Molto nuvoloso"},
    6: {"code": 6, "description": "Coperto"},
    7: {"code": 7, "description": "Nebbia"},
    8: {"code": 8, "description": "Pioggia debole"},
    9: {"code": 9, "description": "Pioggia moderata"},
    10: {"code": 10, "description": "Pioggia forte"},
    11: {"code": 11, "description": "Rovesci"},
    12: {"code": 12, "description": "Temporale"},
    13: {"code": 13, "description": "Grandine"},
    14: {"code": 14, "description": "Neve debole"},
    15: {"code": 15, "description": "Neve moderata"},
    16: {"code": 16, "description": "Neve forte"},
    17: {"code": 17, "description": "Pioggia e neve"},
    18: {"code": 18, "description": "Vento forte"},
    19: {"code": 19, "description": "Tempesta"},
    20: {"code": 20, "description": "Tornado"},
    21: {"code": 21, "description": "Uragano"},
}
