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