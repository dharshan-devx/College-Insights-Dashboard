import pandas as pd
import logging
import os

# Set up logging for clear, informative feedback
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_all_data(path='data/'):
    """
    Loads and merges all datasets from CSV files into a single, cleaned DataFrame.

    Args:
        path (str): The directory path where the CSV files are located.

    Returns:
        pd.DataFrame or None: The combined and cleaned DataFrame, or None if an error occurs.
    """
    files = {
        'students': 'students.csv',
        'subjects': 'subjects.csv',
        'marks': 'marks.csv',
        'attendance': 'attendance.csv'
    }

    data_frames = {}
    try:
        for name, file_name in files.items():
            file_path = os.path.join(path, file_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Missing file: {file_path}")
            data_frames[name] = pd.read_csv(file_path)

    except FileNotFoundError as e:
        logging.error(f"❌ Error loading data: {e}. Please ensure all CSV files are in the '{path}' directory.")
        return None

    # Merge the DataFrames on their respective keys
    try:
        combined_df = data_frames['marks'].merge(data_frames['students'], on='student_id', how='left')
        combined_df = combined_df.merge(data_frames['subjects'], on='subject_id', how='left')
        combined_df = combined_df.merge(data_frames['attendance'], on=['student_id', 'subject_id'], how='left')
    except KeyError as e:
        logging.error(f"❌ KeyError during merge. Check column names in CSVs. Error: {e}")
        return None
    
    # Clean the merged data
    
    # 1. Drop rows with any missing values, ensuring a clean dataset
    combined_df.dropna(inplace=True)
    
    # 2. Rename columns for clarity and consistency across the project
    combined_df.rename(columns={
        'name_x': 'student_name',
        'name_y': 'subject_name',
        'department': 'department',
        'marks': 'marks',
        'attendance_percentage': 'attendance'
    }, inplace=True)
    
    # 3. Create a new 'pass_status' column for analysis
    # Assuming a passing mark is >= 40
    combined_df['pass_status'] = combined_df['marks'].apply(lambda x: 'Pass' if x >= 40 else 'Fail')
    
    # 4. Cast data types for efficiency and consistency
    combined_df['student_id'] = combined_df['student_id'].astype('int32')
    combined_df['marks'] = combined_df['marks'].astype('float32')
    combined_df['attendance'] = combined_df['attendance'].astype('float32')
    combined_df['pass_status'] = combined_df['pass_status'].astype('category')
    
    logging.info("✅ Data loaded, cleaned, and merged successfully.")
    return combined_df

if __name__ == '__main__':
    # This block allows you to run the script directly to test data loading
    df = load_all_data(path='../data/')
    if df is not None:
        print("\n--- Final Merged DataFrame Info ---")
        df.info()
        print("\n--- First 5 Rows of the DataFrame ---")
        print(df.head())