import streamlit as st
import pandas as pd
import pickle
import time

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Smart Bank Loan Portal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD MODEL ---------------- #

model = pickle.load(open("loan_approval_model.pkl", "rb"))
normalizer = pickle.load(open("normalizer.pkl", "rb"))
# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.stApp{
    background-color:#f4f7fc;
}

.main-header{
    background:linear-gradient(135deg,#003366,#0055aa);
    padding:25px;
    border-radius:15px;
    text-align:center;
    color:white;
    margin-bottom:20px;
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.1);
    margin-bottom:20px;
}

.stButton > button{
    background:#003366;
    color:white;
    font-size:18px;
    font-weight:bold;
    width:100%;
    height:55px;
    border-radius:10px;
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

    education = st.selectbox(
        "Education",
        ["Graduate", "Not Graduate"]
    )

with col2:

    self_employed = st.selectbox(
        "Employment Type",
        ["No", "Yes"]
    )

    no_of_dependents = st.slider(
        "Dependents",
        0, 10, 2
    )

    cibil_score = st.slider(
        "CIBIL Score",
        300, 900, 750
    )

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

    loan_term = st.slider(
        "Loan Term (Years)",
        1, 20, 5
    )

    max_loan = income_annum * 5

    st.metric(
        "Maximum Eligible Loan",
        f"₹ {max_loan:,.0f}"
    )

st.markdown('</div>', unsafe_allow_html=True)
# ---------------- CREDIT ANALYSIS ---------------- #

if cibil_score >= 750:
    st.success("🟢 Excellent Credit Score")

elif cibil_score >= 650:
    st.warning("🟡 Average Credit Score")

else:
    st.error("🔴 High Risk Customer")
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

# Total Assets

total_assets = (
    residential_assets_value +
    commercial_assets_value +
    luxury_assets_value +
    bank_asset_value
)

st.metric(
    "💎 Total Assets",
    f"₹ {total_assets:,.0f}"
)

st.markdown('</div>', unsafe_allow_html=True)
# ---------------- ASSET ANALYSIS ---------------- #

if total_assets >= 1000000:

    st.success(
        "🟢 Strong Asset Portfolio"
    )

elif total_assets >= 500000:

    st.warning(
        "🟡 Moderate Asset Portfolio"
    )

else:

    st.error(
        "🔴 Weak Asset Portfolio"
    )




# ---------------- APPLICATION SUMMARY ---------------- #

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("📋 Application Summary")

# Risk Category

if cibil_score >= 750:
    risk_category = "🟢 Low Risk"

elif cibil_score >= 650:
    risk_category = "🟡 Medium Risk"

else:
    risk_category = "🔴 High Risk"

st.info(f"""
👤 Customer Name : {customer_name}

🆔 Customer ID : {customer_id}

💰 Annual Income : ₹ {income_annum:,.0f}

🏦 Loan Amount : ₹ {loan_amount:,.0f}

📅 Loan Term : {loan_term} Years

⭐ CIBIL Score : {cibil_score}

⚠ Risk Category : {risk_category}

💎 Total Assets : ₹ {total_assets:,.0f}
""")

st.markdown('</div>', unsafe_allow_html=True)




# ---------------- DASHBOARD METRICS ---------------- #

st.subheader("📊 Banking Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Income",
        f"₹ {income_annum:,.0f}"
    )

with col2:
    st.metric(
        "Loan Amount",
        f"₹ {loan_amount:,.0f}"
    )

with col3:
    st.metric(
        "CIBIL Score",
        cibil_score
    )

with col4:
    st.metric(
        "Total Assets",
        f"₹ {total_assets:,.0f}"
    )





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
# ---------------- NORMALIZATION ---------------- #

input_normalized = normalizer.transform(input_data)
with st.expander("🔍 View Model Input"):

    st.dataframe(input_data)




# ---------------- LOAN DECISION ENGINE ---------------- #

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("🏦 Loan Decision Engine")

if st.button("🔍 Process Loan Application"):

    # Progress Bar

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    # Banking Validation Rules

    if loan_amount > income_annum * 5:

        st.error(
            "❌ Loan Rejected: Requested amount exceeds eligibility."
        )

    elif cibil_score < 600:

        st.error(
            "❌ Loan Rejected: Low CIBIL Score."
        )

    else:

        prediction = model.predict(
            input_normalized
        )[0]

        st.write(
            f"Model Prediction Value: {prediction}"
        )

        # Approved = 1
        # Rejected = 0

        if prediction == 1:

            st.balloons()

            st.success(
                "✅ LOAN APPROVED"
            )

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

            st.error(
                "❌ LOAN REJECTED"
            )

            st.markdown(f"""
### Rejection Details

**Customer Name:** {customer_name}

**Customer ID:** {customer_id}

**Reason:**
- Risk assessment criteria not satisfied
- Model decision returned Rejected
""")

st.markdown('</div>', unsafe_allow_html=True)




report = f"""
SMART BANK LOAN REPORT

Customer Name: {customer_name}

Customer ID: {customer_id}

Annual Income: ₹ {income_annum}

Loan Amount: ₹ {loan_amount}

Loan Term: {loan_term} Years

CIBIL Score: {cibil_score}

Total Assets: ₹ {total_assets}

Status: APPROVED
"""

st.download_button(
    label="📄 Download Loan Report",
    data=report,
    file_name="loan_report.txt",
    mime="text/plain"
)




# ---------------- FOOTER ---------------- #

st.markdown("---")

st.markdown(
    """
    <center>
    <h4>🏦 Smart Bank Loan Approval System</h4>
    <p>Powered by Machine Learning & Streamlit</p>
    </center>
    """,
    unsafe_allow_html=True
)
