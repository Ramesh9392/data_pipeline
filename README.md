# 🌀 Random User Data Pipeline

A production-ready Apache Airflow pipeline that fetches random user data from an external API, processes and loads it into a PostgreSQL database, and sends a formatted email summary report. This DAG includes robust features such as data quality checks, conditional branching, audit logging, and notification management.

---

## 🚀 Features

- ✅ **Scheduled Ingestion**: Runs daily to pull random user data from an external API.
- 🔁 **Branching Logic**: Smart branching to skip steps if data already exists.
- 🗃️ **PostgreSQL Integration**: Loads data into a relational database using parameterized queries.
- 🧪 **Data Quality Check**: Uses SQL sensor to ensure data freshness before ingestion.
- 📧 **Email Notifications**: Sends an HTML summary email after each DAG run.
- 📜 **Audit Logging**: Logs ingestion metadata to a dedicated audit table.
- 🧱 **Modular Design**: Clean project structure for easy extension and testing.

---

## 📁 Project Structure
├── dags/
│ └── random_user_pipeline.py # Main DAG definition
├── ingestion/
│ └── api_fetcher/
│ └── fetch_random_user.py # Fetches data from external API
├── storage/
│ └── postgres_loader/
│ └── write_to_postgres.py # Loads data into PostgreSQL
├── utils/
│ ├── branch_decision.py # Decides whether to fetch data
│ ├── skip_task_xcoms.py # Handles XComs for skipped paths
│ └── email_content_template.html # HTML template for summary email
├── sql/
│ ├── check_fresh_data.sql # SQL sensor query
│ └── log_ingestion.sql # SQL audit logging
├── README.md
└── requirements.txt # Python dependencies (optional)
---

## 🛠️ Technologies Used

- **[Apache Airflow](https://airflow.apache.org/)** – Workflow orchestration
- **Python 3.8+** – Scripting and pipeline logic
- **PostgreSQL** – Data storage and audit logging
- **SQL** – Sensors and inserts
- **Jinja2/HTML** – Email templating
- **XComs & Trigger Rules** – Task flow control

---

Trigger Rules: Ensures tasks proceed only if upstream conditions are met

📬 Example Email Report
Includes user count, timestamps, and ingestion status in a visually structured HTML format.
