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
    engine = db.create_engine("mysql+mysqldb://test:test123@192.168.99.100:3306/test") # db
    engine.connect()

    # engine.execute("DROP TABLE IF EXISTS `confirmed_melted`; DROP TABLE IF EXISTS `deaths_melted`; DROP TABLE IF EXISTS `recovered_melted`;")

    deaths = pd.read_csv(path1)
    confirmed = pd.read_csv(path2)
    recovered = pd.read_csv(path3)

    variables = [
    "Province/State",
    "Country/Region",
    "Lat",
    "Long"
    ]
    
    confirmed_melted = pd.melt(frame=confirmed, id_vars= variables, var_name="fecha",value_name="confirmed")
    confirmed_melted["confirmed"] = confirmed_melted["confirmed"].astype(int)
    confirmed_melted=confirmed_melted.rename(columns={'Lat': 'lat' , 'Long': 'lon'})

    deaths_melted = pd.melt(frame=deaths, id_vars= variables, var_name="fecha",value_name="deaths")
    deaths_melted["deaths"] = deaths_melted["deaths"].astype(int)
    deaths_melted=deaths_melted.rename(columns={'Lat': 'lat' , 'Long': 'lon'})

    recovered_melted = pd.melt(frame=recovered, id_vars= variables, var_name="fecha",value_name="recovered")
    recovered_melted["recovered"] = recovered_melted["recovered"].astype(int)
    recovered_melted=recovered_melted.rename(columns={'Lat': 'lat' , 'Long': 'lon'})

    with engine.begin() as connection:
        deaths_melted.to_sql('deaths_melted', con=connection, schema='test', if_exists='replace', index=False)
        confirmed_melted.to_sql('confirmed_melted', con=connection, schema='test', if_exists='replace', index=False)
        recovered_melted.to_sql('recovered_melted', con=connection, schema='test', if_exists='replace', index=False)

    engine.execute("SELECT * FROM deaths_melted").fetchall()
    engine.execute("SELECT * FROM confirmed_melted").fetchall()
    engine.execute("SELECT * FROM recovered_melted").fetchall()


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

# sensor1 >> sensor2 >> sensor3 >> etl
[sensor1, sensor2, sensor3] >> etl