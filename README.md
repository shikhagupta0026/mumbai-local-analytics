# 🚆 Mumbai Local Train Analytics Dashboard

An interactive data analytics dashboard for exploring Mumbai suburban railway train operations, routes, destinations, travel times, railway lines, and train frequency.

🔗 **Live Dashboard:** https://mumbai-local-analytics.streamlit.app/

🔗 **GitHub Repository:** https://github.com/shikhagupta0026/mumbai-local-analytics

---

## 📊 Project Overview

Mumbai's suburban railway network operates thousands of train services across multiple railway lines.

This project analyzes Mumbai local train timetable data and presents the results through an interactive Streamlit dashboard.

The dashboard helps users explore:

- Train service distribution by railway line
- Local vs AC train services
- Most frequent routes
- Top destinations
- Top originating stations
- Average travel time
- Average distance
- Train frequency by time period
- Fastest and slowest route segments
- Train frequency by train type
- SQL-based analytical insights

> **Note:** This project analyzes timetable and train-service data. It does not represent real-time passenger crowd levels or live train delays.

---

## 🎯 Project Objectives

The main objectives of this project are:

1. Clean and prepare Mumbai local train timetable data.
2. Store structured data using SQLite.
3. Perform exploratory data analysis using Python.
4. Perform analytical queries using SQL.
5. Create meaningful visualizations.
6. Build an interactive dashboard using Streamlit.
7. Deploy the dashboard online for public access.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Data processing and analysis |
| Pandas | Data cleaning and manipulation |
| SQLite | Database storage and SQL analysis |
| SQL | Analytical queries |
| Plotly | Interactive visualizations |
| Streamlit | Dashboard development |
| Git | Version control |
| GitHub | Code hosting |
| Streamlit Community Cloud | Deployment |

---

## 📁 Project Structure

```text
Mumbai-Local-Analytics/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── cleaned/
│   │   └── timetables_cleaned.csv
│   │
│   ├── raw/
│   │   └── all_timetables.csv
│   │
│   └── mumbai_local.db
│
├── image/
│   └── mumbai_train.png
│
├── outputs/
│   ├── charts/
│   ├── dashboard_kpis.csv
│   ├── line_summary.csv
│   └── route_summary.csv
│
├── sql/
│   ├── 01_analysis.sql
│   └── 02_analysis.sql
│
├── src/
│   ├── clean_all_timetables.py
│   ├── clean_stations.py
│   ├── clean_timetable.py
│   ├── create_database.py
│   ├── eda.py
│   ├── fetch_all_timetables.py
│   ├── fetch_timetable.py
│   ├── inspect_data.py
│   ├── inspect_timetable.py
│   ├── kpi_analysis.py
│   ├── sql_analysis.py
│   └── visualize.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
🔄 Data Analytics Workflow
Raw Train Timetable Data
          ↓
     Data Cleaning
          ↓
 Feature Engineering
          ↓
     SQLite Database
          ↓
   SQL Analysis + EDA
          ↓
    Data Visualization
          ↓
 Streamlit Dashboard
          ↓
   Streamlit Deployment
🧹 Data Cleaning

The project uses Python and Pandas to clean the raw timetable data.

The cleaning process includes:

Standardizing column names
Removing unnecessary spaces
Converting numeric columns
Cleaning departure and arrival times
Creating departure hour and minute
Calculating travel time
Handling midnight crossings
Creating route identifiers
Creating train IDs
Categorizing train types
Creating time-period categories
Handling missing speed values
Removing duplicate records
Checking invalid travel times
Checking missing values
🗄️ SQL Analysis

The cleaned data is stored in a SQLite database.

SQL analysis includes:

Total train records
Train count by railway line
Train type distribution
Top destinations
Most frequent routes
Average travel time by line
Average distance by line
Train frequency by time period
Slowest routes
Fastest routes
Most frequent trains
Railway line vs train type
Top originating stations
Travel time by train type
Longest route segments
📈 Key Dataset Statistics

The current dataset contains:

3,550 train timetable records
5 railway line categories
Local and AC train services
Multiple train origins and destinations
Route-level travel time and distance information
Railway Lines
Code	Railway Line
CR	Central Railway
WR	Western Railway
HR	Harbour Line
TH	Trans-Harbour
PL	Port Line
📊 Dashboard Sections
1. Overview

Provides a high-level summary of Mumbai local train operations.

2. Train Operations

Explores:

Railway line distribution
Train types
Train frequency
Train origins and destinations
3. Route Intelligence

Analyzes:

Most frequent routes
Longest routes
Fastest routes
Slowest routes
4. Station Analysis

Explores station-level train service activity.

5. Travel Performance

Analyzes:

Average travel time
Average distance
Travel time by railway line
Travel time by train type
6. SQL Insights

Displays analytical results generated using SQL queries.

🚀 Running the Project Locally
1. Clone the repository
git clone https://github.com/shikhagupta0026/mumbai-local-analytics.git
2. Navigate to the project
cd mumbai-local-analytics
3. Create a virtual environment
python -m venv venv
4. Activate the environment

Windows:

venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
6. Run the Streamlit dashboard
python -m streamlit run dashboard/app.py

The dashboard will open at:

http://localhost:8501
🌐 Live Deployment

The dashboard is deployed using Streamlit Community Cloud.

🔗 Live Application:

https://mumbai-local-analytics.streamlit.app/

📌 Important Note About the Analysis

The project currently uses timetable/service data.

Therefore:

Train frequency represents recorded timetable services.
"Most frequent routes" represents routes with the highest number of timetable records.
Travel time is calculated from timetable departure and arrival information.
The project does not measure actual passenger crowd density.
The project does not provide real-time train delay information.

Future versions can incorporate real-time train data, passenger crowd data, and historical delay information.

🔮 Future Improvements

Possible future enhancements include:

Real-time Mumbai local train status
Passenger crowd estimation
Train delay analysis
Peak-hour crowd prediction
Station congestion analysis
Interactive Mumbai railway network map
Machine learning for delay prediction
Machine learning for crowd prediction
Real-time API integration
Weather impact analysis
Historical trend analysis
💡 Skills Demonstrated

This project demonstrates practical experience with:

Data Cleaning
Exploratory Data Analysis
SQL
SQLite
Python
Pandas
Data Visualization
Plotly
Streamlit
Dashboard Development
Feature Engineering
Git & GitHub
Cloud Deployment
Data Storytelling
👩‍💻 Author

Shikha Gupta

B.Sc. Computer Science

GitHub:
https://github.com/shikhagupta0026

Portfolio:
https://shikhagupta0026.github.io/Shikha_portfolio/

📄 License

This project is licensed under the MIT License.


### Then save it

In VS Code:

**Ctrl + S**

Then push the README to GitHub:

```cmd
git add README.md
git commit -m "Add professional project README"
git push

Your GitHub repository will then look much more professional when a recruiter opens it.
