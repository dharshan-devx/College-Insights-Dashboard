import pandas as pd
import os
import logging
from src.load_data import load_all_data

# Set up logging for informative output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_pass_rate_by_subject(df):
    """
    Calculates the pass percentage for each subject.

    Args:
        df (pd.DataFrame): The main DataFrame containing student data.

    Returns:
        pd.DataFrame: A DataFrame with each subject's pass percentage.
    """
    subject_stats = df.groupby('subject_name')['pass_status'].value_counts(normalize=True).unstack().fillna(0)
    subject_stats['Pass_Percentage'] = subject_stats['Pass'] * 100
    return subject_stats.sort_values(by='Pass_Percentage', ascending=False)

def get_top_students_by_department(df, n=5):
    """
    Identifies the top N students in each department based on average marks.

    Args:
        df (pd.DataFrame): The main DataFrame containing student data.
        n (int): The number of top students to retrieve per department.

    Returns:
        pd.DataFrame: A DataFrame with the top students ranked by average marks.
    """
    # Compute average marks for each student
    avg_marks = df.groupby(['student_name', 'department'])['marks'].mean().reset_index()
    
    # Rank students within each department
    avg_marks['rank'] = avg_marks.groupby('department')['marks'].rank(method='min', ascending=False)
    
    return avg_marks[avg_marks['rank'] <= n].sort_values(by=['department', 'rank'])

def get_correlation_matrix(df):
    """
    Generates a correlation matrix for numerical features (marks and attendance).

    Args:
        df (pd.DataFrame): The main DataFrame.

    Returns:
        pd.DataFrame: The correlation matrix.
    """
    numerical_df = df[['marks', 'attendance']]
    return numerical_df.corr()

def get_at_risk_students(df, attendance_threshold=75):
    """
    Finds students with attendance below a specified threshold.

    Args:
        df (pd.DataFrame): The main DataFrame.
        attendance_threshold (int): The attendance percentage below which a student is considered at-risk.

    Returns:
        pd.DataFrame: A DataFrame of students at risk.
    """
    at_risk_df = df[df['attendance'] < attendance_threshold]
    return at_risk_df[['student_name', 'department', 'subject_name', 'attendance', 'marks']]

def generate_at_risk_report(df, filename='at_risk_students_report.xlsx'):
    """
    Generates an Excel report of at-risk students and saves it to the reports folder.

    Args:
        df (pd.DataFrame): The main DataFrame.
        filename (str): The name of the Excel file to save.
    """
    output_dir = 'outputs/reports'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    at_risk_df = get_at_risk_students(df)
    
    if at_risk_df.empty:
        logging.info("🎉 No at-risk students found. No report generated.")
        return
        
    report_path = os.path.join(output_dir, filename)
    
    try:
        at_risk_df.to_excel(report_path, index=False)
        logging.info(f"✅ At-risk student report successfully generated at: {report_path}")
    except Exception as e:
        logging.error(f"❌ Failed to save report: {e}")

if __name__ == '__main__':
    # This block runs when the script is executed directly
    df = load_all_data()
    if df is not None:
        logging.info("--- Running Analysis and Report Generation ---")
        
        pass_rates = get_pass_rate_by_subject(df)
        logging.info("\n🏆 Pass Rate by Subject:")
        print(pass_rates)

        top_students = get_top_students_by_department(df)
        logging.info("\n🥇 Top Students by Department:")
        print(top_students)

        correlation_matrix = get_correlation_matrix(df)
        logging.info("\n📈 Correlation Matrix:")
        print(correlation_matrix)
        
        generate_at_risk_report(df)