Markdown

# 🎓 Advanced College Insights Dashboard

This project is an end-to-end data analytics solution that provides a comprehensive dashboard for a college administration. It leverages Python for data processing, analysis, and machine learning, with a user-friendly interface built using Streamlit. The dashboard offers key insights into student performance, attendance, and predictive analytics to identify at-risk students.

## ✨ Key Features

* **Data Ingestion & Cleaning:** Processes raw student data from multiple CSV files, including marks, attendance, and personal details, into a single, clean dataset.
* **Data Analysis & Reporting:** Performs advanced statistical analysis to calculate metrics like subject pass rates, top student rankings, and the correlation between attendance and marks.
* **Dynamic Visualizations:** Generates and displays interactive charts (bar charts, pie charts, scatter plots) that provide clear insights into academic trends.
* **Predictive Modeling:** Utilizes a **Logistic Regression** model to predict a student's pass/fail status, enabling proactive intervention for at-risk students.
* **Interactive Dashboard:** A modern, multi-tab Streamlit application allows users to filter data by department and interact with the predictive model in real-time.

## 📁 Project Structure

college-insights-dashboard/
│
├── 📁 data/                  # Raw & processed datasets
├── 📁 notebooks/              # Jupyter notebooks for EDA and ML
├── 📁 src/                    # All Python source code
│   ├── load_data.py          # Data loading, cleaning, and merging
│   ├── sql_utils.py          # Functions for executing SQL queries
│   ├── analysis.py           # Core data analysis logic
│   ├── visualize.py          # Functions for generating visualizations
│   └── model.py              # ML model training and saving
│
├── 📁 outputs/                # Generated reports and charts
├── 📁 streamlit_app/          # Streamlit dashboard application
├── README.md                 # Project overview
└── requirements.txt          # Project dependencies


## 🛠️ Technologies Used

* **Python 3.9+**
* **Pandas:** For data manipulation and analysis.
* **Streamlit:** For building the interactive web dashboard.
* **Scikit-learn:** For the predictive modeling.
* **Matplotlib & Seaborn:** For data visualization.
* **Jupyter:** For exploratory data analysis in the notebooks.

## 🚀 Setup and Installation

Follow these steps to get the project up and running on your local machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/college-insights-dashboard.git](https://github.com/your-username/college-insights-dashboard.git)
cd college-insights-dashboard
2. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

Bash

python -m venv venv
# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
3. Install Dependencies
Install all the required libraries using the requirements.txt file.

Bash

pip install -r requirements.txt
4. Run the Machine Learning Model (Optional but Recommended)
To ensure the predictive analysis tab works, train the model first. This will save model.pkl to the outputs folder.

Bash

python src/model.py
5. Run the Streamlit Dashboard
Now, launch the Streamlit application from the project's root directory.

Bash

streamlit run streamlit_app/app.py
Your browser will automatically open a new tab with the running dashboard.

🤝 Contribution
Feel free to open issues or submit pull requests to improve the project.

© 2024 [Dharshan Sondi]