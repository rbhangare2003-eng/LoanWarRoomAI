from ai_risk_model import calculate_ai_risk_score, assign_credit_grade
from pypdf import PdfReader
from sales_agent import evaluate_sales
from risk_agent import evaluate_risk
from compliance_agent import evaluate_compliance

import re
import json
from pypdf import PdfReader

from sales_agent import evaluate_sales
from risk_agent import evaluate_risk
from compliance_agent import evaluate_compliance


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_number(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return float(match.group(1).replace(",", ""))
    return None


def extract_financial_metrics(text):
    metrics = {}

    metrics["Revenue"] = extract_number(r"Revenue\s*[:\-]?\s*\$?([\d,]+)", text)
    metrics["EBITDA"] = extract_number(r"EBITDA\s*[:\-]?\s*\$?([\d,]+)", text)
    metrics["Debt"] = extract_number(r"Debt\s*[:\-]?\s*\$?([\d,]+)", text)
    metrics["Equity"] = extract_number(r"Equity\s*[:\-]?\s*\$?([\d,]+)", text)
    metrics["Interest"] = extract_number(r"Interest\s*[:\-]?\s*\$?([\d,]+)", text)

    if metrics["Debt"] and metrics["Equity"]:
        metrics["Debt_to_Equity"] = round(metrics["Debt"] / metrics["Equity"], 2)

    if metrics["EBITDA"] and metrics["Interest"]:
        metrics["DSCR"] = round(metrics["EBITDA"] / metrics["Interest"], 2)

    return metrics
    
    raroc_score = calculate_raroc(metrics)
    print("\nRAROC Score:", raroc_score)

if __name__ == "__main__":

    file_path = input("Enter PDF file name (with .pdf): ")

    text = extract_text_from_pdf(file_path)

    metrics = extract_financial_metrics(text)

    print("\nExtracted Financial Metrics:\n")
    print(metrics)

    # --- SALES ---
    sales_result = evaluate_sales(metrics)
    print("\nSales Agent Output:\n", sales_result)

    # --- RISK ---
    risk_result = evaluate_risk(metrics)
    print("\nRisk Agent Output:\n", risk_result)

    # --- COMPLIANCE ---
    compliance_result = evaluate_compliance(metrics)
    print("\nCompliance Agent Output:\n", compliance_result)

    # AI Risk Scoring
    ai_score = calculate_ai_risk_score(metrics)
    credit_grade = assign_credit_grade(ai_score)

    print("\nAI Risk Score:", ai_score)
    print("Credit Grade:", credit_grade)


    # --- FINAL DECISION LOGIC ---
    if compliance_result["Compliance_Status"] == "BLOCK":
        final_decision = "REJECTED"
    elif risk_result["Risk_Decision"] == "REJECT":
        final_decision = "REJECTED"
    else:
        final_decision = "APPROVED"

    print("\nFINAL LOAN DECISION:", final_decision)




































