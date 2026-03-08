def evaluate_fraud(metrics):
    fraud_score = 0
    flags = []

    revenue = metrics.get("Revenue", 0)
    ebitda = metrics.get("EBITDA", 0)
    debt = metrics.get("Debt", 0)
    equity = metrics.get("Equity", 0)
    interest = metrics.get("Interest", 0)
    dscr = metrics.get("DSCR", 0)
    debt_to_equity = metrics.get("Debt_to_Equity", 0)

    # 1. Basic missing / weak data checks
    if revenue <= 0:
        fraud_score += 30
        flags.append("Revenue missing or zero")

    if ebitda <= 0:
        fraud_score += 20
        flags.append("EBITDA missing or zero")

    if equity <= 0:
        fraud_score += 25
        flags.append("Equity missing or zero")

    # 2. Logical consistency checks
    if ebitda > revenue and revenue > 0:
        fraud_score += 35
        flags.append("EBITDA greater than Revenue")

    if interest > debt and debt > 0:
        fraud_score += 25
        flags.append("Interest greater than Debt")

    if debt == 0 and interest > 0:
        fraud_score += 20
        flags.append("Interest exists but Debt is zero")

    # 3. Suspicious ratio checks
    if dscr > 15:
        fraud_score += 20
        flags.append("DSCR unusually high")

    if dscr == 0 and interest > 0 and ebitda > 0:
        fraud_score += 15
        flags.append("DSCR inconsistent with EBITDA and Interest")

    if debt_to_equity > 10:
        fraud_score += 25
        flags.append("Debt-to-Equity extremely high")

    # 4. Pattern-based suspicious number checks
    suspicious_values = [100000, 500000, 1000000, 2000000, 5000000, 10000000]
    exact_round_matches = 0

    for value in [revenue, ebitda, debt, equity, interest]:
        if value in suspicious_values:
            exact_round_matches += 1

    if exact_round_matches >= 4:
        fraud_score += 15
        flags.append("Too many perfectly rounded values")

    # 5. Revenue / profit sanity
    if revenue > 0 and ebitda > 0:
        margin = ebitda / revenue
        if margin > 0.8:
            fraud_score += 20
            flags.append("EBITDA margin suspiciously high")

    # Final status
    if fraud_score >= 70:
        fraud_status = "HIGH"
    elif fraud_score >= 35:
        fraud_status = "MEDIUM"
    else:
        fraud_status = "LOW"

    return {
        "Fraud_Score": min(fraud_score, 100),
        "Fraud_Status": fraud_status,
        "Flags": flags
    }
