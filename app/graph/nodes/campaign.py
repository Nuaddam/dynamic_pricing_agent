def apply_campaign_rule(state):
    base = state["base_price"]
    sentiment = state["sentiment"]
    campaign = state["campaign"]

    if campaign == "FLASHSALE":
        price = base * 0.8
    elif campaign == "CLEARANCE":
        price = base * 0.7 if sentiment == "negative" else base * 0.9
    elif campaign == "MEMBER":
        price = base * 0.9
    elif campaign == "PRE-ORDER":
        price = base * 1.05 if sentiment == "positive" else base
    elif campaign == "BMSM":
        price = base * 0.85
    else:
        price = base

    return {"campaign_price": price}

def apply_campaign_rule_v2(state: dict) -> dict:
    # ref: https://gemini.google.com/share/876ae8fcd494
    base = state["base_price"]
    campaign = state.get("campaign", "NONE")
    
    # Standardize input strings to protect against casing anomalies
    sentiment = str(state.get("sentiment", "neutral")).strip().lower()

    # 5-Tier Config Matrix
    PRICING_MATRIX = {
        "FLASHSALE": {
            "strongly negative": 0.70, "negative": 0.75, "neutral": 0.80, "positive": 0.85, "strongly positive": 0.90
        },
        "CLEARANCE": {
            "strongly negative": 0.60, "negative": 0.70, "neutral": 0.80, "positive": 0.90, "strongly positive": 1.00
        },
        "MEMBER": {
            "strongly negative": 0.80, "negative": 0.85, "neutral": 0.90, "positive": 0.95, "strongly positive": 0.98
        },
        "PRE-ORDER": {
            "strongly negative": 0.90, "negative": 0.95, "neutral": 1.00, "positive": 1.05, "strongly positive": 1.15
        },
        "BMSM": {
            "strongly negative": 0.75, "negative": 0.80, "neutral": 0.85, "positive": 0.90, "strongly positive": 0.95
        }
    }
    
    # Lookup resolution sequence
    campaign_rules = PRICING_MATRIX.get(campaign, {})
    
    # Fallback cascade: if sentiment string is mangled, fallback to 'neutral'
    # If campaign doesn't exist, fallback to 1.0 multiplier
    multiplier = campaign_rules.get(sentiment, campaign_rules.get("neutral", 1.0))
    
    # Apply multiplier & enforce a strict global minimum safety floor (50% of base)
    final_price = max(base * multiplier, base * 0.50)
    
    return {
        "campaign_price": round(final_price, 2),
        "applied_multiplier": multiplier,
        "resolved_sentiment": sentiment
    }