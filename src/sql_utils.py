import sqlite3
import pandas as pd
import logging
from src.load_data import load_all_data

# Set up logging for informative output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_sql_query(query, df):
    """
    Executes a SQL query on a pandas DataFrame using an in-memory SQLite database.

    Args:
        query (str): The SQL query string to execute.
        df (pd.DataFrame): The DataFrame to be used as the data source.

    Returns:
        pd.DataFrame or None: A DataFrame with the query results, or None if an error occurs.
    """
    conn = None
    try:
        # Create an in-memory SQLite database connection
        conn = sqlite3.connect(':memory:')
        
        # Write the pandas DataFrame to a SQL table named 'student_data'
        df.to_sql('student_data', conn, index=False, if_exists='replace')
        
        # Execute the query and fetch results into a new DataFrame
        result_df = pd.read_sql_query(query, conn)
        
        return result_df
    except Exception as e:
        logging.error(f"❌ Error executing SQL query: {e}")
        return None
    finally:
        if conn:
            conn.close()

def demonstrate_queries(df):
    """
    Demonstrates key SQL queries for the dashboard and prints the results.
    """
    logging.info("--- Demonstrating Advanced SQL Queries ---")
    
    # Query 1: Top 5 students by average marks
    query_top_students = """
        SELECT student_name, AVG(marks) as avg_marks
        FROM student_data
        GROUP BY student_name
        ORDER BY avg_marks DESC
        LIMIT 5;
    """
    top_students = run_sql_query(query_top_students, df)
    logging.info("\n📊 SQL Query: Top 5 students by average marks")
    print(top_students)

    # Query 2: Pass percentage by subject (using conditional aggregation)
    query_pass_percentage = """
        SELECT subject_name, 
               CAST(SUM(CASE WHEN pass_status = 'Pass' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS pass_rate
        FROM student_data
        GROUP BY subject_name
        ORDER BY pass_rate DESC;
    """
    pass_percentage = run_sql_query(query_pass_percentage, df)
    logging.info("\n📊 SQL Query: Pass percentage by subject")
    print(pass_percentage)

    # Query 3: Students with attendance < 75%
    query_low_attendance = """
        SELECT DISTINCT student_name, department, attendance, subject_name
        FROM student_data
        WHERE attendance < 75
        ORDER BY attendance ASC;
    """
    low_attendance = run_sql_query(query_low_attendance, df)
    logging.info("\n📊 SQL Query: Students with low attendance (< 75%)")
    print(low_attendance)

if __name__ == '__main__':
    # This block allows you to run the script directly to test the queries
    df = load_all_data(path='../data/')
    if df is not None:
        demonstrate_queries(df)