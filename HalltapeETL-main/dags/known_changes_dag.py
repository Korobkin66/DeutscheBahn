from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='known_changes',
    default_args=DEFAULT_ARGS,
    description='Fetch XML from API and parse it into SQLite DB.db',
    start_date=datetime(2025, 5, 15),
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1,
    tags=['api','xml','sqlite'],
) as dag:

    # 1) Вызываем скрипт, который делает запрос к API и сохраняет XML
    fetch_xml = BashOperator(
        task_id='fetch_xml',
        bash_command=(
            'python3 /opt/airflow/Python_files_folder_for_dags/evaNo.py '
            '--output /opt/airflow/known_changes_folder/known_changes_xml.xml'
        ),
    )

    # 2) Вызываем скрипт, который парсит XML и пишет в SQLite
    parse_xml = BashOperator(
        task_id='parse_xml',
        bash_command=(
            'python3 /opt/airflow/Python_files_folder_for_dags/PARSER_known_changes.py '
            '--input /opt/airflow/known_changes_folder/known_changes_xml.xml'
            '--db sqlite:////opt/airflow/DB.db'
        ),
    )

    fetch_xml >> parse_xml
