from global_variables import STOP_TOKENS, CON_UNIONS, SUB_UNIONS, RULE_CHECK_STOP_TOKENS, ALL_FEATURES

class RuleCondition:
    def __init__(self):
        pass

    def check(self, tokens, *args, **kwargs):
        raise NotImplementedError


class EqualityCondition(RuleCondition):
    def __init__(self, feature, value=None):
        self._feature = feature
        self._value = value

    def check(self, tokens):

        if type(tokens) not in [list, tuple]:
            tokens = list(tokens)
        # # print("for tokens", tokens)
        # # print("checking equality of features", self._feature)
        fea_vals = [token.split("-")[ALL_FEATURES.index(self._feature)]
                    for token in tokens
                    if token.split("-")[ALL_FEATURES.index("ч.р.")] not in RULE_CHECK_STOP_TOKENS]
        # # print("fea_vals:", fea_vals)
        if len(set(fea_vals)) != 1:
            return False
        if self._value is not None and fea_vals[0] != self._value:
            return False
        return True


class ActionCoherence(RuleCondition):
    def __init__(self):
        pass

    def check(self, tokens):
        if type(tokens) not in [list, tuple]:
            tokens = list(tokens)

        return True


class ExactFeatureCondition(RuleCondition):
    def __init__(self, feature, value, pos=0):
        self._feature = feature
        self._value = value
        self._pos = pos

    def check(self, tokens):
        if type(tokens) not in [list, tuple]:
            tokens = list(tokens)

        fea_vals = [token.split("-")[ALL_FEATURES.index(self._feature)]
                    for token in tokens
                    if token.split("-")[ALL_FEATURES.index("ч.р.")] not in RULE_CHECK_STOP_TOKENS]

        # # print("for tokens", tokens)
        # # print("checking equality of features", self._feature, fea_vals[self._pos], self._value)
        return fea_vals[self._pos] == self._value

adjective_rules = {
    (("прил полн", "прил полн"),
     (EqualityCondition("падеж"),
      EqualityCondition("род"),
      EqualityCondition("числ"))): ("опр гр", ("род", "числ", "падеж"), 0),
    (("прил полн", ",", "прил полн"),
     (EqualityCondition("падеж"),
      EqualityCondition("род"),
      EqualityCondition("числ"))): ("опр перечисл", ("род", "числ", "падеж"), 0),
    (("прил полн", "и", "прил полн"),
     (EqualityCondition("падеж"),
      EqualityCondition("род"),
      EqualityCondition("числ"))): ("опр перечисл", ("род", "числ", "падеж"), 0),
    (("прил полн", "союз", "прил полн"),
     (EqualityCondition("падеж"),
      EqualityCondition("род"),
      EqualityCondition("числ"))): ("опр перечисл", ("род", "числ", "падеж"), 0),
    (("опр гр", "прил полн"),
     (EqualityCondition("падеж"),
      EqualityCondition("род"),
      EqualityCondition("числ"))): ("опр гр", ("род", "числ", "падеж"), 0),
    (("опр перечисл", ",", "прил полн"),
     (EqualityCondition("падеж"),
      EqualityCondition("род"),
      EqualityCondition("числ"))): ("опр перечисл", ("род", "числ", "падеж"), 0),
    (("прил полн",), ()): ("опр гр", ("род", "числ", "падеж"), 0),
}

name_rules = {
    (("опр гр", "сущ"),
     (EqualityCondition("падеж"),
      EqualityCondition("род"),
      EqualityCondition("числ"))): ("им гр", ("род", "числ", "падеж"), 0),
    (("опр гр", "сущ"),
     (EqualityCondition("падеж"),
      ExactFeatureCondition("числ", "мн", 0),
      EqualityCondition("числ"))): ("им гр", ("род", "числ", "падеж"), 0),

    (("опр гр", "им гр"),
     (EqualityCondition("падеж"),
      EqualityCondition("род"),
      EqualityCondition("числ"))): ("им гр", ("род", "числ", "падеж"), 0),
    (("опр гр", "им гр"),
     (EqualityCondition("падеж"),
      ExactFeatureCondition("числ", "мн", 0),
      EqualityCondition("числ"))): ("им гр", ("род", "числ", "падеж"), 0),

    (("опр перечисл", "сущ"),
     (EqualityCondition("падеж"),
      EqualityCondition("род"),
      EqualityCondition("числ"))): ("им гр", ("род", "числ", "падеж"), 0),
    (("опр перечисл", "сущ"),
     (EqualityCondition("падеж"),
      ExactFeatureCondition("числ", "мн", 0),
      EqualityCondition("числ"))): ("им гр", ("род", "числ", "падеж"), 0),

    (("опр перечисл", "им гр"),
     (EqualityCondition("падеж"),
      EqualityCondition("род"),
      EqualityCondition("числ"))): ("им гр", ("род", "числ", "падеж"), 0),
    (("опр перечисл", "им гр"),
     (EqualityCondition("падеж"),
      ExactFeatureCondition("числ", "мн", 0),
      EqualityCondition("числ"))): ("им гр", ("род", "числ", "падеж"), 0),

    (("сущ",), ()): ("им гр", ("род", "числ", "падеж"), 0),

    (("мест-сущ",), ()): ("им гр", ("род", "числ", "падеж"), 0),

    (("опр гр",), ()): ("им гр", ("род", "числ", "падеж"), 0),
}

noun_rules = {
    (("числ", "им гр",), ()): ("им гр", ("род", "числ", "падеж"), 0),

    (("им гр", "им гр"), ((ExactFeatureCondition("падеж", "род", 1)),)): ("им гр", ("род", "числ", "падеж"), 0),
    (("им гр", "предл", "им гр"), ()): ("им гр", ("род", "числ", "падеж"), 0),

    (("им гр", "и", "им гр"),
     (EqualityCondition("падеж"),)): ("им гр", ("род", "числ", "падеж"), 0),
    (("им гр", ",", "им гр"),
     (EqualityCondition("падеж"),)): ("им гр", ("род", "числ", "падеж"), 0),
    (("им гр", "и", "им гр"),
     (EqualityCondition("падеж"),)): ("им гр", ("род", "числ", "падеж"), 0),
}

participal_rules = {
    (("прич полн", "им гр"), ()): ("прич об", ("род", "числ", "падеж"), 0),
    (("прич об", "им гр"), ()): ("прич об", ("род", "числ", "падеж"), 0),
    (("им гр", ",", "прич об", ","), (EqualityCondition("падеж"),)): ("им гр", ("род", "числ", "падеж"), 0),
    (("им гр", ",", "прич об"), (EqualityCondition("падеж"),)): ("им гр", ("род", "числ", "падеж"), 0),
    (("прич об", "им гр"), (EqualityCondition("падеж"),)): ("им гр", ("род", "числ", "падеж"), 0),
    (("прич полн",), ()): ("прич об", ("род", "числ", "падеж"), 0),
}

verb_rules = {
    (("глаг", "им гр"), ()): ("действ", ("род", "числ", "падеж", "лицо"), 0),
    (("глаг", "нареч"), ()): ("действ", ("род", "числ", "падеж", "лицо"), 0),
    (("глаг", "им гр"), ()): ("действ", ("род", "числ", "падеж", "лицо"), 0),
    (("глаг",), ()): ("действ", ("род", "числ", "падеж", "лицо"), 0),

    (("действ", "действ"), (ExactFeatureCondition("числ", "None", 1),)): (
    "действ", ("род", "числ", "падеж", "лицо"), 0),
    (("действ", "им гр"), ()): ("действ", ("род", "числ", "падеж", "лицо"), 0),
    (("действ", "предл", "им гр"), ()): ("действ", ("род", "числ", "падеж", "лицо"), 0),
    (("действ", "нареч"), ()): ("действ", ("род", "числ", "падеж", "лицо"), 0),
}

sentence_rules = {
    (("им гр", "действ"),
     (EqualityCondition("числ"),
      ExactFeatureCondition("падеж", "имен", 0),
      ActionCoherence())): ("предлож", None, 0),
    (("действ", "им гр"),
     (EqualityCondition("числ"),
      ExactFeatureCondition("падеж", "имен", 1),
      ActionCoherence())): ("предлож", None, 0),
    (("действ",), ()): ("предлож", None, 0),
    (("им гр", "—", "им гр"), (ExactFeatureCondition("падеж", "имен", 0),)): ("предлож", None, 0),
}

union_rules = {
    (("предлож", "предлож"), ()): ("предлож"),
    (("предлож", "союз соч", "предлож"), ()): ("предлож"),
    (("предлож", "союз подч", "предлож"), ()): ("предлож"),
    (("союз подч", "предлож", "союз подч", "предлож"), ()): ("предлож")  # если, то
}

all_rules = [
    (adjective_rules, False),
    (name_rules, False),
    (noun_rules, True),
    (participal_rules, True),
    (verb_rules, True),
    (sentence_rules, False),
    (union_rules, False)
]


def apply_rules(tokens):
    def check_conditions(loc_tokens, conds):
        if len(conds) == 0:
            return True
        check_reses = [cond.check(loc_tokens)
                       for cond in conds]
        return False not in check_reses

    def derive_features(loc_tokens, comb_replacement):
        if comb_replacement[1] is None:
            return comb_replacement[0]

        derives = {fea: loc_tokens[comb_replacement[2]].split("-")[ALL_FEATURES.index(fea)]
                   for fea in comb_replacement[1]}

        return comb_replacement[0] + "-" + "-".join([derives.get(fea, "None")
                                                     for i, fea in enumerate(ALL_FEATURES[1:])])

    for (rules, is_reversed) in all_rules:
        poses = [token.split("-")[0] for token in tokens]
        pos_rule_keys = [key[0] for key in rules.keys()]
        pos_rule_key_lens = sorted(list(set([len(key)
                                             if type(key) is not str else 1
                                             for key in pos_rule_keys])))[::-1]
        iter_rng = reversed(range(len(tokens))) if is_reversed else range(len(tokens))
        ## print(iter_rng)
        for i in iter_rng:
            for (rule_comb, rule_conds), rule_replace in rules.items():
                pos_rule_len = len(rule_comb)

                if len(poses[i:i + pos_rule_len]) != pos_rule_len:
                    continue

                loc_pos_comb = tuple(poses[i:i + pos_rule_len])

                if rule_comb != loc_pos_comb:
                    continue

                if check_conditions(tokens[i:i + pos_rule_len], rule_conds):
                    replacement = derive_features(tokens[i:i + pos_rule_len], rule_replace)

                    new_tokens = tokens[:i] + [replacement] + tokens[i + pos_rule_len:]
                    sep_by_commas = (i - 1 < 0 or tokens[i - 1] == ',') and (
                                i + pos_rule_len >= len(tokens) or tokens[i + pos_rule_len] == ',')
                    if (replacement == "предлож" and len(new_tokens) > 1 and not sep_by_commas):
                        continue

                    return new_tokens, ((i, i + pos_rule_len - 1), replacement.split("-")[0])

    return tokens, None