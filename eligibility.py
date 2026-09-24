"""
A tiny declarative rule engine. Instead of one hand-written boolean function
per scheme, every scheme's eligibility is a JSON object like:

    {"occupation": "farmer", "income_max": 500000}
    {"or": [{"gender": "female"}, {"category_in": ["sc", "st"]}]}

`is_eligible` interprets that structure generically, so adding a new scheme
never requires new code -- only new data.
"""
import re


def _matches_simple(rule, profile):
    if "state" in rule and profile.get("state") != rule["state"]:
        return False
    if "gender" in rule and profile.get("gender") != rule["gender"]:
        return False
    if "occupation" in rule and profile.get("occupation") != rule["occupation"]:
        return False
    if "occupation_not" in rule and profile.get("occupation") == rule["occupation_not"]:
        return False
    if "occupation_in" in rule and profile.get("occupation") not in rule["occupation_in"]:
        return False
    if "category_in" in rule and profile.get("category") not in rule["category_in"]:
        return False
    if "age_min" in rule and (profile.get("age") or 0) < rule["age_min"]:
        return False
    if "age_max" in rule and (profile.get("age") or 0) > rule["age_max"]:
        return False
    if "income_max" in rule and (profile.get("income") if profile.get("income") is not None else 10**9) > rule["income_max"]:
        return False
    if "other_info_regex" in rule:
        text = profile.get("other_info") or ""
        if not re.search(rule["other_info_regex"], text, re.IGNORECASE):
            return False
    return True


def is_eligible(rule, profile):
    if not _matches_simple(rule, profile):
        return False
    if "or" in rule:
        return any(is_eligible(sub, profile) for sub in rule["or"])
    return True


def match_schemes(schemes, profile):
    return [s for s in schemes if is_eligible(s["rule"], profile)]
