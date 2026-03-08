def evaluate_sales(metrics):
    decision = "APPROVE"
    arguments = []

    revenue = metrics.get("Revenue", 0)
    ebitda = metrics.get("EBITDA", 0)

    if revenue > 1000000:
        arguments.append("Strong revenue base")

    if ebitda > 0:
        arguments.append("Positive operating profitability")

    if not arguments:
        decision = "REVIEW"
        arguments.append("Limited financial growth evidence")

    return {
        "Sales_Decision": decision,
        "Arguments": arguments
    }
