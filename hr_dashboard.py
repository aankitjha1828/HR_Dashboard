import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="HR Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("hr_data_sample.csv", parse_dates=["Date"])
    return df

df = load_data()

# Extract year and month
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Title
st.title("📊 HR Dashboard – Recruitment | Onboarding | Offboarding")

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")

# --- Year Filter ---
years = sorted(df['Year'].unique(), reverse=True)
years.insert(0, "All")
selected_year = st.sidebar.selectbox("Select Year", years)

# Apply year filter
if selected_year == "All":
    year_filtered_df = df.copy()
else:
    year_filtered_df = df[df['Year'] == selected_year]

# --- Department Filter ---
departments = sorted(year_filtered_df['Department'].unique())
departments.insert(0, "All")
selected_departments = st.sidebar.multiselect("Select Department(s)", departments, default=["All"])

# Apply department filter
if "All" in selected_departments:
    filtered_df = year_filtered_df.copy()
else:
    filtered_df = year_filtered_df[year_filtered_df['Department'].isin(selected_departments)]

# KPIs
recruited = filtered_df[filtered_df['Status'] == 'Recruited'].shape[0]
onboarded = filtered_df[filtered_df['Status'] == 'Onboarded'].shape[0]
offboarded = filtered_df[filtered_df['Status'] == 'Offboarded'].shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("📥 Recruited", recruited)
col2.metric("🧑‍💻 Onboarded", onboarded)
col3.metric("📤 Offboarded", offboarded)

# Pie Chart
st.subheader("📊 Status Distribution")

fig1, ax1 = plt.subplots()
status_counts = filtered_df['Status'].value_counts()
ax1.pie(
    status_counts,
    labels=status_counts.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=["#4CAF50", "#2196F3", "#F44336"]
)
ax1.axis('equal')
st.pyplot(fig1)

# Monthly Bar Chart
st.subheader("📅 Monthly HR Activity Breakdown")

fig2, ax2 = plt.subplots()
monthly_data = filtered_df.groupby(['Month', 'Status']).size().unstack(fill_value=0)
monthly_data.plot(kind='bar', stacked=True, ax=ax2)
ax2.set_xlabel("Month")
ax2.set_ylabel("No. of Employees")
ax2.set_title("Monthly Activities")
st.pyplot(fig2)

# Data Table
st.subheader("📋 Detailed Data View")
st.dataframe(filtered_df)
