def apply_campaign(base_price, campaign, sentiment):

    if campaign == "FLASHSALE":
        return base_price * 0.8

    if campaign == "CLEARANCE":
        return base_price * 0.7 if sentiment == "negative" else base_price * 0.9

    if campaign == "MEMBER":
        return base_price * 0.9

    if campaign == "PRE-ORDER":
        return base_price * 1.05 if sentiment == "positive" else base_price

    if campaign == "BMSM":
        return base_price * 0.85

    return base_price