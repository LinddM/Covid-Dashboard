# Covid-Dashboard Pipeline

Data Products final project

* [About the Project](#about-the-project)
  * [Built With](#built-with)
  * [Design](#design)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)

## About the Project

The project consists of a data pipeline that processes 3 csv files, inserts them into a database, and then based on the processed data builds a dashboard that allows you to analyze the statistics of each of the files.

### Built With

* airflow
* docker
* docker-compose

### Design

We basically orchestate airflow and the dashboard inside docker-compose. The usage of the airflow UI is described in the [Usage](#usage) title

#### docker-compose.yaml

It initializes 4 containers:

  - <i> postgres and webserver </i> for airflow
  - <i> db </i> for mysql
  - <i> dashboard </i> for streamlit dashboard

#### Dockerfile

It helps us to put our streamlit dashboard inside a docker container to call it in the docker-compose

#### requirements.txt

Contains dependencies to build our streamlit dashboard

#### data.py

Contains the streamlit dashboard that calls its data from a mysql db

#### dags.py

Contains the tasks for the DAG to execute in the airflow UI:
 
 * 3 file sensor for the csv's
 * 1 python operator to load the csv's data to mysql db

## Getting Started

### Prerequisites

* docker
* docker-compose

### Installation

Clone the repo

```sh
git clone https://github.com/LinddM/Covid-Dashboard.git
```

## Usage

1. Build the project

```sh
docker-compose build
```

2. Run the project

```sh
docker-compose up
```

3. View the UI

Insert ```localhost:8080``` or ```<your-docker-machine-ip>:8080```<strong>**</strong> in your web navigator

    3.1 Check the connection

    3.1.1 Click Admin > Connections and search for "my_file_system"

  <img src="readme_img/connections.png">

    3.1.2 Try to edit "my_file_system" connection

  <img src="readme_img/fs.png">

  You should see something like this. If not, delete the connection and create it again

    3.2. Run the DAG

    3.2.1. Be sure to turn on the DAG

  <img src="readme_img/on_dag.png">

    3.2.2. Trigger the DAG

  <img src="readme_img/trigger_dag.png">

4. View the Dashboard

Insert ```localhost:8501``` or ```<your-docker-machine-ip>:8501```<strong>**</strong> in your web navigator

<img src="readme_img/streamlit.gif">

Here you can browse COVID-19 stats by metric, date and country

<strong>**</strong><i>To find you docker machine ip you can insert in the command line "docker-machine ip"</i>