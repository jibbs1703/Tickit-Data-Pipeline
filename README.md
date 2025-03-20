# Tickit Data Lake : Building a Data Lake Using an Orchestrator + AWS Resources

## Overview
Welcome to the Tickit Data Lake project! The Tickit Data Lake project demonstrates the construction
of a scalable and robust 3-tier data lake on AWS, leveraging the power of Apache Airflow for orchestration
and automation. This project provides a practical example of building a modern data pipeline capable of 
handling the extraction, loading, and transformation (ELT) of batch data, specifically designed to support
the analytical needs of a business using the Tickit Dataset. 

## Key Features and Technologies:

- Automated Orchestration:  Airflow is the core orchestration engine, responsible for scheduling, monitoring,
and managing the entire data pipeline.  It defines the workflow as a Directed Acyclic Graph (DAG), ensuring
dependencies between tasks are correctly handled.  Airflow's robust features enable task retries, logging,
and alerting, ensuring pipeline reliability. 

- AWS Integration: The project seamlessly integrates with various AWS resources, including:
1. EC2: Reliable and highly available computing for running the orchestrator.

2. S3: Scalable object storage for the Bronze, Silver, and Gold layers.

3. Redshift: Scalable data warehouse used for providing a high-performance analytical database.

## Value
This project serves as a valuable example of building a modern data lake on AWS using Airflow, showcasing best
practices for data ingestion, processing, and transformation.  It provides a solid foundation for building a 
robust data platform to support a wide range of analytical needs.

Feel free to fork, clone or zip the contents of this repository for your needs. 