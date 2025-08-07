import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Import functions from src directory
# This try-except block ensures the app runs even if src is not in the path
try:
    from src.load_data import load_all_data
    from src.analysis import get_pass_rate_by_subject, get_top_students_by_department, get_correlation_matrix
    from src.sql_utils import run_sql_query
except ImportError as e:
    st.error(f"Error importing modules: {e}. Please ensure you are running the app from the root directory with `streamlit run streamlit_app/app.py`.")
    st.stop()

# --- 1. SET PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Advanced College Insights Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CACHE DATA AND MODEL ---
@st.cache_data
def load_data_and_model():
    """
    Loads data and the trained ML model, caching the results to improve performance.
    """
    df = load_all_data()
    model = None
    model_path = 'outputs/model.pkl'
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        st.warning("⚠️ Predictive model file not found. Please run `python src/model.py` to train and save the model.")
    return df, model

df, model = load_data_and_model()

# --- 3. DASHBOARD LAYOUT & UI ---
st.title("🎓 College Insights Dashboard")
st.markdown("### A data-driven analytics platform for academic performance.")
st.markdown("---")

if df is not None:
    # --- Sidebar for filters ---
    st.sidebar.header("Filter Data")
    departments = sorted(df['department'].unique().tolist())
    selected_dept = st.sidebar.multiselect(
        'Select Department(s)', 
        options=departments, 
        default=departments
    )
    
    # Filter the DataFrame based on sidebar selections
    filtered_df = df[df['department'].isin(selected_dept)]

    # --- Tabbed Navigation ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Subject Trends", "🏆 Student Performance", "🧠 Predictive Analysis"])

    with tab1:
        st.header("Dashboard Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Students", filtered_df['student_id'].nunique())
        with col2:
            st.metric("Total Subjects", filtered_df['subject_name'].nunique())
        with col3:
            avg_marks = filtered_df['marks'].mean()
            st.metric("Average Marks", f"{avg_marks:.2f}%")
        with col4:
            pass_rate = (filtered_df['pass_status'].eq('Pass').sum() / filtered_df.shape[0]) * 100
            st.metric("Overall Pass Rate", f"{pass_rate:.2f}%")
        
        st.markdown("---")
        st.subheader("Raw Data Table")
        st.dataframe(filtered_df.head(10).style.highlight_max(axis=0))

    with tab2:
        st.header("Subject-wise Trends")
        
        st.subheader("Pass Percentage by Subject")
        pass_rates = get_pass_rate_by_subject(filtered_df)['Pass_Percentage']
        fig1, ax1 = plt.subplots(figsize=(12, 7))
        sns.barplot(x=pass_rates.index, y=pass_rates.values, palette='viridis', ax=ax1)
        ax1.set_title('Pass Percentage by Subject', fontsize=16)
        ax1.set_xlabel('Subject', fontsize=12)
        ax1.set_ylabel('Pass Percentage (%)', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        st.pyplot(fig1)

        st.subheader("Correlation between Marks and Attendance")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.regplot(x='attendance', y='marks', data=filtered_df, scatter_kws={'alpha':0.6}, line_kws={'color':'red'}, ax=ax2)
        ax2.set_title('Attendance vs Marks with Regression Line', fontsize=16)
        ax2.set_xlabel('Attendance Percentage (%)', fontsize=12)
        ax2.set_ylabel('Marks', fontsize=12)
        st.pyplot(fig2)
        st.info("A clear positive correlation indicates that higher attendance is strongly associated with higher marks.")
        
    with tab3:
        st.header("Student Performance")

        st.subheader("Top 5 Students by Average Marks")
        top_students = get_top_students_by_department(filtered_df, n=5)
        st.dataframe(top_students.set_index(['department', 'student_name']).style.background_gradient(cmap='Greens'))
        
        st.subheader("Students with Low Attendance (Below 75%)")
        low_attendance_students = run_sql_query("SELECT student_name, department, attendance, subject_name FROM student_data WHERE attendance < 75;", filtered_df)
        if low_attendance_students is not None and not low_attendance_students.empty:
            st.warning("🚨 The following students are at risk due to low attendance.")
            st.dataframe(low_attendance_students)
        else:
            st.success("🎉 All students in the selected departments have an attendance of 75% or higher.")

    with tab4:
        st.header("Predictive Analysis")
        st.markdown("This section uses a Logistic Regression model to predict a student's pass/fail status based on their marks and attendance.")
        
        if model is not None:
            st.subheader("Predict Student Status")
            with st.form("prediction_form"):
                attendance_input = st.slider("Attendance Percentage (%)", 0, 100, 85)
                marks_input = st.slider("Marks", 0, 100, 70)
                submit_button = st.form_submit_button("Predict")

                if submit_button:
                    input_data = pd.DataFrame([[attendance_input, marks_input]], columns=['attendance', 'marks'])
                    prediction = model.predict(input_data)[0]
                    proba = model.predict_proba(input_data)[0]
                    
                    if prediction == 1:
                        st.success(f"Prediction: **Pass**")
                        st.markdown(f"Probability of Passing: **{proba[1]*100:.2f}%**")
                        st.balloons()
                    else:
                        st.error(f"Prediction: **Fail**")
                        st.markdown(f"Probability of Failing: **{proba[0]*100:.2f}%**")
        else:
            st.warning("The predictive model is not available. Please train it first by running `python src/model.py`.")

else:
    st.error("Data could not be loaded. Please check your `data/` directory and ensure the CSV files are correct.")