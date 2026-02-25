from pd_model import calculate_probability_of_default, categorize_risk
import streamlit as st
from pypdf import PdfReader
from sales_agent import evaluate_sales
from risk_agent import evaluate_risk
from compliance_agent import evaluate_compliance
from ai_risk_model import calculate_ai_risk_score, assign_credit_grade
import re

st.set_page_config(page_title="LendSynthetix - AI Loan War Room", layout="wide")

st.title("🏦 LendSynthetix - AI Loan Underwriting System")
st.write("Agentic AI-Based Automated Loan Decision Platform")

# PDF Text Extraction
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Metric Extraction
def extract_financial_metrics(text):

    def find_value(pattern):
        match = re.search(pattern, text)
        return float(match.group(1)) if match else 0.0

    revenue = find_value(r"Revenue:\s*(\d+)")
    ebitda = find_value(r"EBITDA:\s*(\d+)")
    debt = find_value(r"Debt:\s*(\d+)")
    equity = find_value(r"Equity:\s*(\d+)")
    interest = find_value(r"Interest:\s*(\d+)")

    debt_to_equity = debt / equity if equity else 0
    dscr = ebitda / interest if interest else 0

    return {
        "Revenue": revenue,
        "EBITDA": ebitda,
        "Debt": debt,
        "Equity": equity,
        "Interest": interest,
        "Debt_to_Equity": round(debt_to_equity, 2),
        "DSCR": round(dscr, 2)
    }

uploaded_file = st.file_uploader("Upload Loan Financial PDF", type="pdf")

if uploaded_file:

    text = extract_text_from_pdf(uploaded_file)
    metrics = extract_financial_metrics(text)

    st.subheader("📊 Extracted Financial Metrics")
    st.json(metrics)

    sales_result = evaluate_sales(metrics)
    risk_result = evaluate_risk(metrics)
    compliance_result = evaluate_compliance(metrics)

    st.subheader("🤝 Agent Decisions")
    st.write("Sales Agent:", sales_result)
    st.write("Risk Agent:", risk_result)
    st.write("Compliance Agent:", compliance_result)

    ai_score = calculate_ai_risk_score(metrics)
    credit_grade = assign_credit_grade(ai_score)

    st.subheader("🧠 AI Risk Scoring")
    # Probability of Default
    pd_value = calculate_probability_of_default(metrics)
    risk_category = categorize_risk(pd_value)

    st.subheader("📊 Probability of Default")
    st.write("Probability of Default (%):", pd_value)
    st.write("Risk Category:", risk_category)

    st.write("AI Risk Score:", ai_score)
    st.write("Credit Grade:", credit_grade)
    # Probability of Default
    pd_value = calculate_probability_of_default(metrics)
    risk_category = categorize_risk(pd_value)

    # Final Decision
    if compliance_result["Compliance_Status"] == "BLOCK":
        final_decision = "REJECTED"
    elif risk_result["Risk_Decision"] == "REJECT":
        final_decision = "REJECTED"
    else:
        final_decision = "APPROVED"

    st.subheader("🏦 Final Loan Decision")
    if final_decision == "APPROVED":
        st.success("LOAN APPROVED ✅")
    else:
        st.error("LOAN REJECTED ❌")
    st.subheader("📝 Decision Explanation")

    explanation = f"""
    Loan evaluation completed using multi-agent AI underwriting system.
    The applicant shows a DSCR of {metrics['DSCR']} and Debt-to-Equity ratio of {metrics['Debt_to_Equity']}.
    AI Risk Score is {ai_score} with Credit Grade {credit_grade}.
    Probability of Default estimated at {pd_value}% indicating {risk_category}.
    """

    st.info(explanation)
