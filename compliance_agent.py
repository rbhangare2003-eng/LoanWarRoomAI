def evaluate_compliance(metrics):
    flags = []
    decision = "CLEAR"

    # Simple AML simulation logic
    if metrics.get("Revenue") and metrics["Revenue"] < 100000:
        decision = "BLOCK"
        flags.append("Suspiciously low declared revenue")

    return {
        "Compliance_Status": decision,
        "Flags": flags
    }
