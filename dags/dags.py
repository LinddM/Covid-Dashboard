from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args={
    'owner': 'mai',
    'depends_on_past': False,
    'max_active_runs': 5,
    'start_date': days_ago(5)
    }

# dag = DAG(
#    'tutorial',
#     schedule_interval="0 1 * * *",
#     template_searchpath=tmpl_search_path,
#     default_args=default_args
# )

scriptPath = '/data-manipulation/'

dag = DAG('task_test', description='Another tutorial DAG',
          default_args=default_args,
          schedule_interval='0 1 * * *',
          catchup=True)

t1 = BashOperator(
    task_id='t1',
    dag=dag,
    bash_command='python3 '+ scriptPath +'dataManipulation.py "{{ execution_date }}"',
    retries=2
)

# def process_func(**kwargs):
#     print(kwargs["execution_date"])

# t1 = PythonOperator(
#     task_id='t1',
#     dag=dag,
#     python_callable=process_func,
#     provide_context=True,
#     op_kwargs={
#     }
# )

# t2 = PythonOperator(
#     task_id='t2',
#     dag=dag,
#     python_callable=process_func,
#     provide_context=True,
#     op_kwargs={

#     }
# )

# t3 = PythonOperator(
#     task_id='t3',
#     dag=dag,
#     python_callable=process_func,
#     provide_context=True,
#     op_kwargs={

#     }
# )

# t4 = PythonOperator(
#     task_id='t4',
#     dag=dag,
#     python_callable=process_func,
#     provide_context=True,
#     op_kwargs={
#     }
# )

t1 # >> [t2, t3] >> t4 