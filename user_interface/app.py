import streamlit as st
import pandas as pd
import pickle
import time
import os

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Smart Bank Loan Portal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD MODEL ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "loan_approval_model.pkl")
normalizer_path = os.path.join(BASE_DIR, "normalizer.pkl")

model = pickle.load(open(model_path, "rb"))
normalizer = pickle.load(open(normalizer_path, "rb"))

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>
.stApp {
    background-color: #f4f7fc;
}

.main-header {
    background: linear-gradient(135deg,#003366,#0055aa);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.stButton > button {
    background: #003366;
    color: white;
    font-size: 18px;
    font-weight: bold;
    width: 100%;
    height: 55px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

with st.sidebar:
    st.title("🏦 Smart Bank")
    st.markdown("---")
    st.write("Loan Management Portal")
    st.markdown("---")
    st.success("AI Powered Loan Approval System")

# ---------------- HEADER ---------------- #

st.markdown("""
<div class="main-header">
<h1>🏦 SMART BANK LOAN APPROVAL SYSTEM</h1>
<p>AI Powered Banking Decision Platform</p>
</div>
""", unsafe_allow_html=True)

# ---------------- CUSTOMER INFORMATION ---------------- #

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("👤 Customer Information")

col1, col2 = st.columns(2)

with col1:
    customer_name = st.text_input("Customer Name")
    customer_id = st.text_input("Customer ID")
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])

with col2:
    self_employed = st.selectbox("Employment Type", ["Yes", "No"])
    no_of_dependents = st.slider("Dependents", 0, 10, 2)
    cibil_score = st.slider("CIBIL Score", 300, 900, 750)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LOAN INFORMATION ---------------- #

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("💰 Loan Information")

col1, col2 = st.columns(2)

with col1:
    income_annum = st.number_input(
        "Annual Income (₹)",
        min_value=50000,
        max_value=10000000,
        value=500000
    )

    loan_amount = st.number_input(
        "Loan Amount (₹)",
        min_value=10000,
        max_value=5000000,
        value=300000
    )

with col2:
    loan_term = st.slider("Loan Term (Years)", 1, 20, 5)

    max_loan = income_annum * 5
    st.metric("Maximum Eligible Loan", f"₹ {max_loan:,.0f}")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ASSETS INFORMATION ---------------- #

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🏠 Assets Information")

col1, col2 = st.columns(2)

with col1:
    residential_assets_value = st.number_input(
        "Residential Assets Value (₹)",
        min_value=0,
        value=200000
    )

    commercial_assets_value = st.number_input(
        "Commercial Assets Value (₹)",
        min_value=0,
        value=100000
    )

with col2:
    luxury_assets_value = st.number_input(
        "Luxury Assets Value (₹)",
        min_value=0,
        value=50000
    )

    bank_asset_value = st.number_input(
        "Bank Asset Value (₹)",
        min_value=0,
        value=150000
    )

total_assets = (
    residential_assets_value +
    commercial_assets_value +
    luxury_assets_value +
    bank_asset_value
)

st.metric("💎 Total Assets", f"₹ {total_assets:,.0f}")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ANALYSIS ---------------- #

if cibil_score >= 750:
    risk_category = "🟢 Low Risk"
    st.success("🟢 Excellent Credit Score")
elif cibil_score >= 650:
    risk_category = "🟡 Medium Risk"
    st.warning("🟡 Average Credit Score")
else:
    risk_category = "🔴 High Risk"
    st.error("🔴 High Risk Customer")

# ---------------- APPLICATION SUMMARY ---------------- #

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📋 Application Summary")

st.info(f"""
👤 Customer Name: {customer_name}

🆔 Customer ID: {customer_id}

💰 Annual Income: ₹ {income_annum:,.0f}

🏦 Loan Amount: ₹ {loan_amount:,.0f}

📅 Loan Term: {loan_term} Years

⭐ CIBIL Score: {cibil_score}

⚠ Risk Category: {risk_category}

💎 Total Assets: ₹ {total_assets:,.0f}
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DASHBOARD METRICS ---------------- #

st.subheader("📊 Banking Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Income", f"₹ {income_annum:,.0f}")
col2.metric("Loan Amount", f"₹ {loan_amount:,.0f}")
col3.metric("CIBIL Score", cibil_score)
col4.metric("Total Assets", f"₹ {total_assets:,.0f}")

# ---------------- ENCODING ---------------- #

education_encoded = 0 if education == "Graduate" else 1
self_employed_encoded = 1 if self_employed == "Yes" else 0

# ---------------- INPUT DATAFRAME ---------------- #

input_data = pd.DataFrame({
    ' no_of_dependents': [no_of_dependents],
    ' education': [education_encoded],
    ' self_employed': [self_employed_encoded],
    ' income_annum': [income_annum],
    ' loan_amount': [loan_amount],
    ' loan_term': [loan_term],
    ' cibil_score': [cibil_score],
    ' residential_assets_value': [residential_assets_value],
    ' commercial_assets_value': [commercial_assets_value],
    ' luxury_assets_value': [luxury_assets_value],
    ' bank_asset_value': [bank_asset_value]
})

with st.expander("🔍 View Model Input"):
    st.dataframe(input_data)

# ---------------- LOAN DECISION ENGINE ---------------- #

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🏦 Loan Decision Engine")

final_status = "Not Processed"

if st.button("🔍 Process Loan Application"):

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    if loan_amount > income_annum * 5:
        final_status = "REJECTED"
        st.error("❌ Loan Rejected: Requested amount exceeds eligibility.")

    elif cibil_score < 600:
        final_status = "REJECTED"
        st.error("❌ Loan Rejected: Low CIBIL Score.")

    else:
        input_normalized = normalizer.transform(input_data)
        prediction = model.predict(input_normalized)[0]

        st.write(f"Model Prediction Value: {prediction}")

        if prediction == 1:
            final_status = "APPROVED"
            st.balloons()
            st.success("✅ LOAN APPROVED")

            st.markdown(f"""
### 🎉 Loan Sanction Details

**Customer Name:** {customer_name}

**Customer ID:** {customer_id}

**Approved Amount:** ₹ {loan_amount:,.0f}

**Loan Term:** {loan_term} Years

**CIBIL Score:** {cibil_score}

**Total Assets:** ₹ {total_assets:,.0f}
""")

        else:
            final_status = "REJECTED"
            st.error("❌ LOAN REJECTED")

            st.markdown(f"""
### Rejection Details

**Customer Name:** {customer_name}

**Customer ID:** {customer_id}

**Reason:**
- Risk assessment criteria not satisfied
- Model decision returned Rejected
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- REPORT DOWNLOAD ---------------- #

report = f"""
SMART BANK LOAN REPORT

Customer Name: {customer_name}
Customer ID: {customer_id}
Annual Income: ₹ {income_annum}
Loan Amount: ₹ {loan_amount}
Loan Term: {loan_term} Years
CIBIL Score: {cibil_score}
Total Assets: ₹ {total_assets}
Risk Category: {risk_category}
Status: {final_status}
"""

st.download_button(
    label="📄 Download Loan Report",
    data=report,
    file_name="loan_report.txt",
    mime="text/plain"
)

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.markdown("""
<center>
<h4>🏦 Smart Bank Loan Approval System</h4>
<p>Powered by Machine Learning & Streamlit</p>
</center>
""", unsafe_allow_html=True)
