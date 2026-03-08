def calculate_ai_risk_score(metrics):
    score = 100

    if metrics.get("DSCR", 0) < 1.5:
        score -= 40
    elif metrics.get("DSCR", 0) < 2:
        score -= 20

    if metrics.get("Debt_to_Equity", 0) > 2:
        score -= 30
    elif metrics.get("Debt_to_Equity", 0) > 1:
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
