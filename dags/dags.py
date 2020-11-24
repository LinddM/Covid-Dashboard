from airflow import DAG
from airflow.contrib.hooks.fs_hook import FSHook
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import sqlalchemy as db
import os

path1 = os.getcwd() + "/dags/deaths.csv"
path2 = os.getcwd() + "/dags/confirmed.csv"
path3 = os.getcwd() + "/dags/recovered.csv"

def etl_process(**kwargs):
    engine = db.create_engine("mysql+mysqldb://test:test123@192.168.99.100:3306/test")
    engine.connect()

    df1 = pd.read_csv(path1)
    df2 = pd.read_csv(path2)
    df3 = pd.read_csv(path3)

    with engine.begin() as connection:
        df1.to_sql('deaths', con=connection, schema='test', if_exists='replace', index=False)
        df2.to_sql('confirmed', con=connection, schema='test', if_exists='replace', index=False)
        df3.to_sql('recovered', con=connection, schema='test', if_exists='replace', index=False)

    engine.execute("SELECT * FROM deaths").fetchall()
    engine.execute("SELECT * FROM confirmed").fetchall()
    engine.execute("SELECT * FROM recovered").fetchall()


dag = DAG('mainDAG', description="Dag to Ingest CSV's",
          default_args={
              'owner': 'MaiBoris',
              'depends_on_past': False,
              'max_active_runs': 1,
              'start_date': days_ago(5)
          },
          schedule_interval='0 1 * * *',
          catchup=False)

sensor1 = FileSensor(task_id="file_sensor_deaths",
                    dag=dag,
                    filepath='deaths.csv',
                    fs_conn_id='my_file_system',
                    poke_interval=10,
                    timeout=600)

sensor2 = FileSensor(task_id="file_sensor_confirmed",
                    dag=dag,
                    filepath='confirmed.csv',
                    fs_conn_id='my_file_system',
                    poke_interval=10,
                    timeout=600)

sensor3 = FileSensor(task_id="file_sensor_recovered",
                    dag=dag,
                    filepath='recovered.csv',
                    fs_conn_id='my_file_system',
                    poke_interval=10,
                    timeout=600)

etl = PythonOperator(task_id="load_to_db",
                     provide_context=True,
                     python_callable=etl_process,
                     dag=dag
                     )

[sensor1, sensor2, sensor3] >> etl