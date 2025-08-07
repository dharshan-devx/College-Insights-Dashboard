import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging
from src.load_data import load_all_data
from src.analysis import get_pass_rate_by_subject, get_correlation_matrix

# Set up logging for clear, informative feedback
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_visualizations(df):
    """
    Generates and saves a series of advanced visualizations to the outputs/charts directory.

    Args:
        df (pd.DataFrame): The main DataFrame containing student data.
    """
    output_dir = 'outputs/charts'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created output directory: {output_dir}")

    # Set the seaborn style for better aesthetics
    sns.set_theme(style="whitegrid")
    
    # 1. Bar chart: Pass Percentage by Subject
    pass_rates = get_pass_rate_by_subject(df)['Pass_Percentage']
    plt.figure(figsize=(12, 7))
    sns.barplot(x=pass_rates.index, y=pass_rates.values, palette='viridis')
    plt.title('Pass Percentage by Subject', fontsize=16, fontweight='bold')
    plt.xlabel('Subject', fontsize=12)
    plt.ylabel('Pass Percentage (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'pass_rate_by_subject.png'))
    plt.close()
    logging.info("📈 Generated 'pass_rate_by_subject.png'")

    # 2. Pie chart: Overall Grade Distribution
    grade_counts = df['pass_status'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#F44336'])
    plt.title('Overall Grade Distribution', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'grade_distribution.png'))
    plt.close()
    logging.info("📈 Generated 'grade_distribution.png'")

    # 3. Line plot: Attendance vs Marks (Regression Plot)
    plt.figure(figsize=(10, 6))
    sns.regplot(x='attendance', y='marks', data=df, scatter_kws={'alpha':0.6}, line_kws={'color':'red', 'linestyle':'--'})
    plt.title('Attendance vs Marks with Regression Line', fontsize=16, fontweight='bold')
    plt.xlabel('Attendance Percentage (%)', fontsize=12)
    plt.ylabel('Marks', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'attendance_vs_marks.png'))
    plt.close()
    logging.info("📈 Generated 'attendance_vs_marks.png'")

    # 4. Heatmap: Correlation Matrix
    corr_matrix = get_correlation_matrix(df)
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
    plt.title('Correlation Matrix of Marks & Attendance', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'correlation_matrix.png'))
    plt.close()
    logging.info("📈 Generated 'correlation_matrix.png'")

    logging.info("✅ All visualizations successfully generated and saved.")

if __name__ == '__main__':
    # This block allows you to run the script directly to generate the charts
    df = load_all_data(path='../data/')
    if df is not None:
        generate_visualizations(df)