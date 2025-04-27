# Tickit Data Pipeline

## Overview
Welcome to the Tickit Data Lake project! The Tickit Data Lake project demonstrates the construction
of a scalable and robust data pipeline, leveraging the power of Apache Airflow for orchestration
and automation. This project provides a practical example of building a modern data pipeline capable of 
handling the extraction, loading, and transformation (ELT) of batch data, specifically designed to support
the analytical needs of a business using the Tickit Dataset as a case study. 

## Key Features and Technologies:

- Automated Orchestration:  Airflow is the core orchestration engine, responsible for scheduling, monitoring,
and managing the entire data pipeline.  It defines the workflow as a Directed Acyclic Graph (DAG), ensuring
dependencies between tasks are correctly handled.  Airflow's robust features enable task retries, logging,
and alerting, ensuring pipeline reliability. 

- Integration of Multiple Data Sources: The project seamlessly integrates with various data sources including:
1. On-premises SQL and NoSQL databases
2. Cloud-hosted SQL and NoSQL databases

## Value
This project serves as a valuable example of building a modern data pipelines using Airflow, showcasing best
practices for data ingestion, processing, and transformation.  It provides a solid foundation for building a 
robust data platform to support a wide range of analytical needs.

## Project Setup
- Clone the repository.
   ```bash
    git clone https://github.com/jibbs1703/Tickit-Data-Pipeline
   ```
- Create a virtual environment.
   ```bash
    python3 -m venv venv
   ```
- Activate the virtual environment.
   ```bash
    source venv/bin/activate
   ```
- Install the dependencies.
   ```bash
    pip install -r requirements.txt
   ```c