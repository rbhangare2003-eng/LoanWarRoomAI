# LoanWarRoomAI – AI Powered Multi-Agent Loan Decision System

## Project Overview

LoanWarRoomAI is an AI-driven multi-agent system designed to simulate real-world bank loan approval processes. The system uses financial analysis, risk scoring, compliance checks, and AI-based credit grading to make intelligent loan decisions.

This project demonstrates how modern financial institutions use automated decision engines to evaluate loan applications.

---

## System Architecture

The system consists of multiple intelligent agents:

1. Sales Agent – Evaluates business strength and revenue stability  
2. Risk Agent – Analyzes financial risk ratios (DSCR, Debt-to-Equity)  
3. Compliance Agent – Performs regulatory and red flag checks  
4. AI Risk Model – Calculates AI-based risk score and credit grade  
5. Streamlit Dashboard – Interactive user interface for decision simulation  

---

## Key Features

- PDF Financial Statement Parsing  
- Automatic Financial Metric Extraction  
- Multi-Agent Decision Engine  
- AI-Based Credit Score Calculation  
- Credit Rating Assignment (AAA, AA, A, BBB, High Risk)  
- Streamlit Web Dashboard  

---

## Financial Ratios Used

- DSCR (Debt Service Coverage Ratio)  
- Debt-to-Equity Ratio  
- Revenue & EBITDA Analysis  

---

## AI Risk Scoring Logic

The AI model assigns risk scores based on:

- Cash flow stability  
- Leverage ratio  
- Repayment capacity  

Higher score → Lower risk → Better credit grade.

---

## Technology Stack

- Python 3.12  
- Streamlit  
- pypdf  
- Pandas  
- ReportLab  
- Git & GitHub  

---

## How to Run the Project

1. Create virtual environment:
   python3 -m venv loanenv

2. Activate environment:
   source loanenv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run main engine:
   python pdf_parser.py

5. Run web dashboard:
   streamlit run app.py

---

## Sample Output

AI Risk Score: 100  
Credit Grade: AAA  
Final Decision: APPROVED  

---

## Author

Ravindra Bhangare  
Electronics & Telecommunication Engineering  
AI & Financial Technology Enthusiast  

---

## Project Use Case

This system can be used in:

- Banking Loan Departments  
- FinTech Ris
