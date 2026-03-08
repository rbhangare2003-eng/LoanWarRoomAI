def evaluate_risk(metrics):
    decision = "APPROVE"
    reasons = []

    dscr = metrics.get("DSCR", 0)
    debt_equity = metrics.get("Debt_to_Equity", 0)

    if dscr < 1.2:
        decision = "REJECT"
        reasons.append("DSCR below safe threshold (1.2)")
    elif dscr < 2:
        decision = "REVIEW"
        reasons.append("Moderate DSCR risk")

    if debt_equity > 2:
        decision = "REJECT"
        reasons.append("High leverage (Debt-to-Equity > 2)")
    elif debt_equity > 1:
        reasons.append("Moderate leverage risk")

    return {
        "Risk_Decision": decision,
        "Reasons": reasons
    }
