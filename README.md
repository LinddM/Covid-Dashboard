# Covid-Dashboard

Data Products final project

* [About the Project](#about-the-project)
  * [Built With](#built-with)
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

1. Run the project

```sh
docker-compose up
```

2. View the UI

Insert ```localhost:8080``` or ```<your-docker-machine-ip>:8080``` in your web navigator

<i>To find you docker machine ip you can insert in the command line "docker-machine ip"</i>
