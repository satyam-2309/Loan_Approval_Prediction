import streamlit as st
import pandas as pd
import pickle
import os

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Smart Loan Approval System",
    page_icon="🏦",
    layout="wide"
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
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

h1 {
    color: #38bdf8;
    text-align: center;
    font-size: 50px;
    font-weight: bold;
}

.bank-card {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 0px 20px rgba(0,255,255,0.2);
}

.stButton>button {
    background: linear-gradient(to right, #06b6d4, #2563eb);
    color: white;
    border-radius: 12px;
    height: 3.5em;
    width: 100%;
    font-size: 20px;
    font-weight: bold;
    border: none;
}

.result-box {
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-top: 20px;
}

.approved {
    background-color: rgba(34,197,94,0.2);
    color: #22c55e;
}

.rejected {
    background-color: rgba(239,68,68,0.2);
    color: #ef4444;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.markdown(
    "<h1>🏦 Smart Loan Approval System</h1>",
    unsafe_allow_html=True
)

st.markdown("""
<div class='bank-card'>
<h3>AI Powered Banking Loan Approval Interface</h3>
Predict whether a customer loan will be approved or rejected using Machine Learning.
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- INPUT SECTION ---------------- #

col1, col2 = st.columns(2)

with col1:

    no_of_dependents = st.slider(
        "Number of Dependents",
        0, 10, 2
    )

    income_annum = st.number_input(
        "Annual Income",
        min_value=50000,
        max_value=10000000,
        value=500000
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=10000,
        max_value=5000000,
        value=300000
    )

    loan_term = st.slider(
        "Loan Term (Years)",
        1, 20, 5
    )

    cibil_score = st.slider(
        "CIBIL Score",
        300, 900, 750
    )

with col2:

    education = st.selectbox(
        "Education",
        ["Graduate", "Not Graduate"]
    )

    self_employed = st.selectbox(
        "Self Employed",
        ["Yes", "No"]
    )

    residential_assets_value = st.number_input(
        "Residential Assets Value",
        min_value=0,
        value=200000
    )

    commercial_assets_value = st.number_input(
        "Commercial Assets Value",
        min_value=0,
        value=100000
    )

    luxury_assets_value = st.number_input(
        "Luxury Assets Value",
        min_value=0,
        value=50000
    )

    bank_asset_value = st.number_input(
        "Bank Asset Value",
        min_value=0,
        value=150000
    )

# ---------------- ENCODING ---------------- #

education = 0 if education == "Graduate" else 1
self_employed = 1 if self_employed == "Yes" else 0

# ---------------- CREATE DATAFRAME ---------------- #

input_data = pd.DataFrame({
    ' no_of_dependents': [no_of_dependents],
    ' education': [education],
    ' self_employed': [self_employed],
    ' income_annum': [income_annum],
    ' loan_amount': [loan_amount],
    ' loan_term': [loan_term],
    ' cibil_score': [cibil_score],
    ' residential_assets_value': [residential_assets_value],
    ' commercial_assets_value': [commercial_assets_value],
    ' luxury_assets_value': [luxury_assets_value],
    ' bank_asset_value': [bank_asset_value]
})

# ---------------- PREDICTION ---------------- #

if st.button("Predict Loan Approval"):

    input_normalized = normalizer.transform(input_data)

    if loan_amount > income_annum * 5:

        st.markdown("""
        <div class='result-box rejected'>
        ❌ Loan Amount Too High Compared To Income
        </div>
        """, unsafe_allow_html=True)

    elif cibil_score < 600:

        st.markdown("""
        <div class='result-box rejected'>
        ❌ Low CIBIL Score
        </div>
        """, unsafe_allow_html=True)

    else:

        prediction = model.predict(input_normalized)[0]

        # 1 = Approved
        # 0 = Rejected

        if prediction == 1:

            st.markdown("""
            <div class='result-box approved'>
            ✅ Loan Approved
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class='result-box rejected'>
            ❌ Loan Rejected
            </div>
            """, unsafe_allow_html=True)