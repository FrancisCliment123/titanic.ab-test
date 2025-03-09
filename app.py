import streamlit as st
import pandas as pd
import random
import time
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

# Ensure correct data types
df["survived"] = df["survived"].astype(int)
df["pclass"] = df["pclass"].astype(int)
df["age"] = pd.to_numeric(df["age"], errors='coerce')  # Handle missing values

# Business Question
st.title("Titanic Survival Analysis: Which Passenger Group Had the Highest Survival Rate?")

# Select random chart (A or B)
if "chart" not in st.session_state:
    st.session_state.chart = None
    st.session_state.start_time = None
    st.session_state.end_time = None

# Function to create Chart A (Bar Chart by Class)
def create_chart_A():
    fig, ax = plt.subplots()
    survival_rates = df.groupby("pclass")["survived"].mean()
    survival_rates.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_title("Survival Rate by Passenger Class (Bar Chart)")
    ax.set_ylabel("Survival Rate")
    ax.set_xlabel("Passenger Class")
    st.pyplot(fig)

# Function to create Chart B (Box Plot for Age Distribution of Survivors vs Non-Survivors)
def create_chart_B():
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df, x="survived", y="age", ax=ax, palette="coolwarm")
    ax.set_title("Age Distribution of Survivors vs Non-Survivors (Box Plot)")
    ax.set_ylabel("Age")
    ax.set_xlabel("Survival (0 = No, 1 = Yes)")
    st.pyplot(fig)

# Button to show a random chart
if st.button("Show a Random Chart"):
    st.session_state.chart = random.choice(["A", "B"])
    st.session_state.start_time = time.time()
    
    if st.session_state.chart == "A":
        create_chart_A()
    else:
        create_chart_B()
    
    st.button("I answered your question", key="answer_button")

# Measure response time
if "answer_button" in st.session_state:
    st.session_state.end_time = time.time()
    elapsed_time = round(st.session_state.end_time - st.session_state.start_time, 2)
    st.write(f"⏳ Time taken to answer: {elapsed_time} seconds")
