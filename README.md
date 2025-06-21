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
- 🐳 **Dockerized Environment**: Airflow + PostgreSQL run in containers.
- ⚙️ **Environment Configurable**: Easy setup using a `.env` file.
- 🧠 **Conditional Inserts**: Data inserted only if daily conditions are met.

---

## 📁 Project Structure
.
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
├── docker-compose.yml # Docker config for Airflow + Postgres
├── .env.example # Template for environment variables
├── requirements.txt # Optional Python dependencies
└── README.md # This file


---

## 🛠️ Technologies Used

- **[Apache Airflow](https://airflow.apache.org/)** – Workflow orchestration
- **Python 3.8+** – Scripting and pipeline logic
- **PostgreSQL** – Data storage and audit logging
- **SQL** – Sensors and inserts
- **Jinja2/HTML** – Email templating
- **XComs & Trigger Rules** – Task flow control
- **Docker Compose** – Local deployment of Airflow & Postgres

---

## 🧪 Trigger Rules

Airflow DAG uses conditional task execution:
- Skip steps if data already exists for the current date
- Insert data only if at least 1 record exists and fewer than 150 records are already present

---

## 📬 Example Email Report

The email contains:
- Number of records ingested
- Timestamp of ingestion
- DAG execution status  
All presented in a clean, structured HTML template.

---

## 🧰 Setup Instructions

### 1️⃣ Clone the Repository

##  Start the Pipeline Locally
```bash
git clone https://github.com/Ramesh9392/data_pipeline.git
cd data_pipeline
```
Configure Environment Variables
Copy the example config file:

```bash
cp .env_example .env

```
Edit .env and update your local values:
```bash
# Airflow Admin Login
AIRFLOW_ADMIN_USERNAME=admin
AIRFLOW_ADMIN_PASSWORD=admin123

# PostgreSQL Config
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# SMTP Email Settings
smtp_server=smtp.example.com
smtp_port=587
smtp_username=your_username
smtp_password=your_password
smtp_sender_email=airflow@example.com
```

## 3️⃣ Start the Pipeline Locally


```bash
go to project by using cd and in project folder run the following command:

docker compose up --build
```
This will:

Start Airflow and Postgres services

Initialize the metadata DB

Create an admin user

Launch the webserver and scheduler

## 🌐 Access the Airflow UI:

http://localhost:8080

## 4️⃣ Stop the Pipeline
```bash
docker compose down
```
To also remove DB volumes and logs:
```bash
docker compose down -v
```