def calculate_probability_of_default(metrics):

    dscr = metrics["DSCR"]
    leverage = metrics["Debt_to_Equity"]

    # Base probability
    pd = 5.0  

    # Adjust based on DSCR
    if dscr < 1.2:
        pd += 20
    elif dscr < 1.5:
        pd += 10
    elif dscr < 2:
        pd += 5
    else:
        pd -= 2

    # Adjust based on leverage
    if leverage > 2:
        pd += 15
    elif leverage > 1:
        pd += 5
    else:
        pd -= 2

    # Keep between 0 and 100
    pd = max(min(pd, 100), 0)

    return round(pd, 2)


def categorize_risk(pd):

    if pd < 5:
        return "Low Risk"
    elif pd < 15:
        return "Moderate Risk"
    else:
        return "High Risk"
