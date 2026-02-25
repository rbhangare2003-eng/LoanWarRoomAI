def calculate_raroc(metrics):
    ebitda = metrics.get("EBITDA")
    interest = metrics.get("Interest")
    debt = metrics.get("Debt")

    if ebitda and interest and debt:
        net_return = ebitda - interest
        raroc = round(net_return / debt, 3)
        return raroc

    return None
