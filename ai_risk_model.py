def calculate_ai_risk_score(metrics):

    score = 100

    # DSCR check
    if metrics["DSCR"] < 1.5:
        score -= 40
    elif metrics["DSCR"] < 2:
        score -= 20

    # Leverage check
    if metrics["Debt_to_Equity"] > 2:
        score -= 30
    elif metrics["Debt_to_Equity"] > 1:
        score -= 15

    return max(score, 0)


def assign_credit_grade(score):

    if score >= 85:
        return "AAA"
    elif score >= 70:
        return "AA"
    elif score >= 55:
        return "A"
    elif score >= 40:
        return "BBB"
    else:
        return "HIGH RISK"
