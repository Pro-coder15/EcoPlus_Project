import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier

# ---------------- APP TITLE ----------------
st.title("🌱 EcoPulse: Daily Sustainability Health Monitor")
st.write("Calendar-based AI Sustainability Analysis for Campuses")

# ---------------- LOAD DAILY DATA ----------------
daily_data = pd.read_csv("campus_daily_data.csv")
daily_data["date"] = pd.to_datetime(daily_data["date"])

# ---------------- CALENDAR DATE PICKER ----------------
st.header("📅 Select a Date")
selected_date = st.date_input(
    "Choose a date to view sustainability performance",
    daily_data["date"].min()
)

# ---------------- FILTER DATA FOR SELECTED DATE ----------------
selected_row = daily_data[daily_data["date"] == pd.to_datetime(selected_date)]

if selected_row.empty:
    st.warning("⚠ No data available for the selected date.")
    st.stop()

# ---------------- EXTRACT DAY DATA ----------------
energy = int(selected_row.iloc[0]["energy"])
water = int(selected_row.iloc[0]["water"])
waste = int(selected_row.iloc[0]["waste"])
green = int(selected_row.iloc[0]["green"])
transport = int(selected_row.iloc[0]["transport"])

# ---------------- DAILY SCORE CALCULATION ----------------
score = (
    energy * 0.30 +
    water * 0.20 +
    waste * 0.20 +
    green * 0.15 +
    transport * 0.15
)

st.subheader(f"🌍 EcoPulse Score for {selected_date}")
st.success(f"Sustainability Health Score: {round(score, 2)} / 100")

if score >= 80:
    st.write("🟢 Excellent Green Campus")
elif score >= 50:
    st.write("🟡 Moderate – Needs Improvement")
else:
    st.write("🔴 Poor – Immediate Action Required")

# ---------------- ML MODEL (TRAIN USING FULL YEAR DATA) ----------------
X = daily_data[["energy", "water", "waste", "green", "transport"]]

# Labels: 2-Green, 1-Moderate, 0-Poor
y = []
for _, row in X.iterrows():
    avg = row.mean()
    if avg >= 75:
        y.append(2)
    elif avg >= 50:
        y.append(1)
    else:
        y.append(0)

model = DecisionTreeClassifier()
model.fit(X, y)

prediction = model.predict([[energy, water, waste, green, transport]])

# ---------------- AI PREDICTION RESULT ----------------
st.header("🤖 AI Prediction Result")

if prediction[0] == 2:
    st.success("AI Prediction: 🌿 Green Campus")
elif prediction[0] == 1:
    st.warning("AI Prediction: 🟡 Moderate Campus")
else:
    st.error("AI Prediction: 🔴 Poor Campus")

# ---------------- AI-BASED RECOMMENDATIONS ----------------
st.header("💡 AI-Based Recommendations")

if energy < 60:
    st.write("⚡ Improve energy efficiency by installing LED lights and solar panels.")

if water < 60:
    st.write("💧 Implement rainwater harvesting and repair leakages.")

if waste < 60:
    st.write("🗑 Enhance waste segregation, recycling, and composting.")

if green < 60:
    st.write("🌱 Increase green cover by planting more trees and maintaining gardens.")

if transport < 60:
    st.write("🚲 Encourage electric vehicles, cycling, and public transport.")

if score >= 80:
    st.success("🎉 Campus sustainability performance is excellent!")

# ---------------- DAILY METRICS CHART ----------------
st.header("📊 Daily Sustainability Metrics")

labels = ["Energy", "Water", "Waste", "Green", "Transport"]
values = [energy, water, waste, green, transport]

fig, ax = plt.subplots()
ax.bar(labels, values)
ax.set_ylabel("Score")
ax.set_title(f"Sustainability Metrics on {selected_date}")

st.pyplot(fig)

# ---------------- TREND VIEW (OPTIONAL) ----------------
st.header("📈 Sustainability Trend (Last 30 Days)")

last_30_days = daily_data[daily_data["date"] <= pd.to_datetime(selected_date)].tail(30)
last_30_days["score"] = (
    last_30_days["energy"] * 0.30 +
    last_30_days["water"] * 0.20 +
    last_30_days["waste"] * 0.20 +
    last_30_days["green"] * 0.15 +
    last_30_days["transport"] * 0.15
)

st.line_chart(last_30_days.set_index("date")["score"])
