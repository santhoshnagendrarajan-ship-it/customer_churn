import streamlit as st
import pandas as pd
import pickle

# Load the model and encoder
#with open("D:\GUVI\PROJECTS\Final project\model.pkl", "rb") as model_file:
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("Contract_encoder.pkl", "rb") as encoder_file:
    Contract_encoder = pickle.load(encoder_file)
with open("gender_encoder.pkl", "rb") as encoder_file:
    gender_encoder = pickle.load(encoder_file)    
with open("OnlineSecurity_encoder.pkl", "rb") as encoder_file:
    OnlineSecurity_encoder = pickle.load(encoder_file)
with open("PaymentMethod_encoder.pkl", "rb") as encoder_file:
    PaymentMethod_encoder = pickle.load(encoder_file)

# Streamlit application title
st.title("Churn Prediction App")

# User input fields
total_charges = st.number_input("Total Charges", min_value=0.0, format="%.2f")
tenure = st.number_input("Tenure (in months)", min_value=0, max_value=120)
gender = st.selectbox("Gender", options=["Male", "Female"])
contract_type = st.selectbox("Contract Type", options=["Month-to-month", "One year", "Two year"])
payment_method = st.selectbox("Payment Method", options=["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
online_security = st.selectbox("Online Security", options=["Yes", "No"])

# Prepare input data for prediction
input_data = pd.DataFrame({
    "TotalCharges": [total_charges],
    "tenure": [tenure],
    "Contract": [contract_type],
    "PaymentMethod": [payment_method],
    "OnlineSecurity": [online_security],
    "gender": [gender]
})
st.dataframe(input_data)
#categorical_cols = ["Contract", "PaymentMethod","OnlineSecurity","gender"]
input_data["Contract"] = Contract_encoder.transform(input_data[["Contract"]])
input_data["PaymentMethod"] = PaymentMethod_encoder.transform(input_data[["PaymentMethod"]])
input_data["OnlineSecurity"] = OnlineSecurity_encoder.transform(input_data[["OnlineSecurity"]])
input_data["gender"] =  gender_encoder.transform(input_data[["gender"]]) 

#encoded_input = encoder.transform(input_data)
st.dataframe(input_data)
# Make prediction
prediction = model.predict(input_data)

# Display prediction result
if st.button("Predict Churn"):
    if prediction[0] == 1:
        st.success("The model predicts that the customer will churn.")
    else:
        st.success("The model predicts that the customer will not churn.")