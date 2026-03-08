def evaluate_compliance(metrics):
    flags = []
    decision = "CLEAR"

    if metrics.get("Revenue", 0) < 100000:
        decision = "BLOCK"
        flags.append("Suspiciously low declared revenue")

    return {
        "Compliance_Status": decision,
        "Flags": flags
    }
