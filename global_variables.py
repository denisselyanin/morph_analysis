import pymorphy2 as py

morph = py.MorphAnalyzer()
STOP_TOKENS = [" "]
CON_UNIONS = ['a', 'но', 'да', 'также', 'тоже']
SUB_UNIONS = ['который', 'кто', 'что', 'потому', 'если', 'то']
RULE_CHECK_STOP_TOKENS = [",", "союз", "предл", "—", ";", "и", "соч союз", "подч союз"]
ALL_FEATURES = ["ч.р.", "род", "числ", "падеж", "лицо"]