from global_variables import *

tagging = {
    "PoS": {
        "postfix": "",
        "values": {
            "NOUN": "сущ",
            "ADJF": "прил полн",
            "ADJS": "прил сокр",
            "VERB": "глаг",
            "INFN": "глаг",
            "PRTF": "прич полн",
            "PRTS": "прич крат",
            "GRND": "дееприч",
            "NUMR": "числ",
            "ADVB": "нареч",
            "NPRO": "мест-сущ",
            "PREP": "предл",
            "CONJ": "союз",
            "PRCL": "част",
            "INTJ": "межд",
            None: None}
    },
    "case": {
        "postfix": "п.",
        "values": {
            "nomn": "имен",
            "gent": "род",
            "datv": "дат",
            "accs": "вин",
            "ablt": "тв",
            "loct": "пр",
            None: None}
    },
    "quan": {
        "postfix": "ч.",
        "values": {
            "sing": "ед",
            "plur": "мн",
            None: None}
    },
    "gender": {
        "postfix": "р.",
        "values": {
            "masc": "м",
            "femn": "ж",
            "neut": "ср",
            None: None
        }
    },
    "person": {"postfix": "л.",
               "values": {
                   "1per": "1",
                   "2per": "2",
                   "3per": "3",
                   None: None
               }}
}

def reduce_tag(tag):
    return "-".join([str(tag[fea_name]) for fea_name in ALL_FEATURES])


def get_tags(word, min_rating=0.05):
    is_caps = True;
    for c in word:
        if not ('A' <= c and c <= 'Я'):
            is_caps = False
            break
    if is_caps:
        res = [{"ч.р.": "сущ",
                "род": "Any",
                "падеж": "Any",
                "числ": "Any",
                "лицо": "None",
                "rating": 1}]
    elif word.isnumeric():
        res = [{"ч.р.": "числ",
                "род": "None",
                "падеж": "None",
                "числ": "None",
                "лицо": "None",
                "rating": 1}]
        # print(res)
    elif not word.isalpha() or word == 'и':
        return f"{word}"
    else:
        res = [{"ч.р.": tagging["PoS"]["values"][parse_res.tag.POS],
                "род": tagging["gender"]["values"][parse_res.tag.gender],
                "падеж": tagging["case"]["values"][parse_res.tag.case],
                "числ": tagging["quan"]["values"][parse_res.tag.number],
                "лицо": tagging["person"]["values"][parse_res.tag.person],
                "rating": parse_res.score}
               for parse_res in morph.parse(word) if parse_res.score >= min_rating]

    res = [reduce_tag(tag) for tag in res]
    return res

def split_sentence(sentence):
    pts = sentence.split()
    tokens = []
    for i in range(len(pts)):
        if pts[i] in SUB_UNIONS:
            pts[i] = 'союз соч'
        if pts[i] in SUB_UNIONS:
            pts[i] = 'союз подч'
        if pts[i] == ',':
            dict_tokens[','] = i
        if pts[i] == 'и':
            tokens += pts[i]
            continue
        if (not pts[i].isalpha()) and pts[i][:-1].isalpha():
            if pts[i][-1] in SKIP_TOKENS:
                tokens += [pts[i][:-1]]
            else:
                tokens += [pts[i][:-1], pts[i][-1]]
            continue
        tokens += [pts[i]]

    dict_tokens = {}
    dels = []
    for i in range(len(tokens)):
        t = tokens[i]
        if (t in [',', 'и']) or (not t in dict_tokens):
            dict_tokens[t] = i
        else:
            if (',' in dict_tokens and dict_tokens[','] > dict_tokens[t]) or (
                    'и' in dict_tokens and dict_tokens['и'] > dict_tokens[t]):
                dels.append(i)

    tokens = [tokens[i] for i in range(len(tokens)) if not i in dels]
    return tokens

def choose_options(token_options):
    new_options = []
    for option in token_options:
        correct_option = True
        for i in range(len(option) - 1):
            token = option[i]
            next_token = option[i + 1]
            fea_vals = token.split("-")
            next_fea_vals = next_token.split("-")
            if fea_vals[ALL_FEATURES.index("ч.р.")] == "прил полн" and \
                    next_fea_vals[ALL_FEATURES.index("ч.р.")] in ["прил полн", "сущ"]:
                if fea_vals[ALL_FEATURES.index("падеж")] != next_fea_vals[ALL_FEATURES.index("падеж")]:
                    correct_option = False
                    break
        if correct_option:
            new_options.append(option)

    return new_options
