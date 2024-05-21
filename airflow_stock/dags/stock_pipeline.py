from datetime import datetime, timedelta
import sys
import os

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

from airflow.providers.postgres.operators.postgres import PostgresOperator

def get_sql_query():
    # Đọc dữ liệu từ file
    with open(f'dags/stock.csv', 'r') as file:
        lines = file.readlines()

    # Tạo chuỗi SQL INSERT
    insert_stmt = "INSERT INTO stock (code, reference_price, celling_price, floor_price, price, volume, total_volume, total_value, highest_price, lowest_price, average_price, created_time) VALUES "
    values = []
    for line in lines[1:]:  # Bỏ qua dòng tiêu đề
        fields = line.strip().split(',')
        stock_code, reference_price, celling_price, floor_price, price, volume, total_volume, total_value, highest_price, lowest_price, average_price, time = fields
        values.append(f"('{stock_code}', {reference_price}, {celling_price}, {floor_price}, {price}, {volume}, {total_volume}, {total_value}, {highest_price}, {lowest_price}, {average_price}, '{time}')")

    insert_stmt += ", ".join(values) + ";"
    return insert_stmt


default_args = {
    'owner': 'stocks',
    'depends_on_past': True,
    'start_date' : datetime(2024, 5, 20, 0, 0, 0, 0),
    'end_date' : datetime(2024, 5, 30, 0, 0, 0, 0),
    'email_on_failure': False,
    'email_on_retry': False,
    #'retries': 1,
    #'retry_delay': timedelta(minutes=15),
    'catchup': False
}

dag_name = 'stock_pipeline'
dag = DAG(dag_name,
          default_args=default_args,
          description='Load stock data to PostgreSQL',
          schedule_interval='@daily',
          max_active_runs = 10
        )

start_operator = EmptyOperator(task_id='Begin_execution',  dag=dag)

create_table = PostgresOperator(
    task_id="create_table",
    postgres_conn_id="postgres_demo",
    sql="""
            CREATE TABLE IF NOT EXISTS stock(
            code VARCHAR(5) PRIMARY KEY,
            reference_price FLOAT(2),
            celling_price FLOAT(2),
            floor_price FLOAT(2),
            price FLOAT(2),
            volume FLOAT(2),
            total_volume FLOAT(2),
            total_value BIGINT,
            highest_price FLOAT(2),
            lowest_price FLOAT(2),
            average_price FLOAT(2),
            created_time timestamp
            );
          """,
    dag=dag,
)

delete_data = PostgresOperator(
    task_id="delete_data",
    postgres_conn_id="postgres_demo",
    sql="TRUNCATE stock;",
    dag=dag
)

insert_data = PostgresOperator( 
    task_id="insert_table",
    postgres_conn_id="postgres_demo",
    sql=get_sql_query(),
    dag=dag
)

end_operator = EmptyOperator(task_id='End_execution',  dag=dag)

start_operator >> create_table >> delete_data >> insert_data >> end_operator


