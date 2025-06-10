# Tickit Data Pipeline

## Overview
Welcome to the Tickit Data Lake project! The Tickit Data Lake project demonstrates the construction
of a scalable and robust data pipeline, leveraging the power of Apache Airflow for orchestration
and automation. This project provides a practical example of building a modern data pipeline capable of 
handling the extraction, loading, and transformation (ELT) of batch data, specifically designed to support
the analytical needs of a business. 

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
   cd Tickit-Data-Pipeline
   ```
   ```bash
   # Build Tickit Test Container 
   docker build -t test-tickit .
   ```

   ```bash
   # Run Tickit Test Container
   docker run -it --name tickit-test-container -v .:/app test-tickit
   ```

   ```bash
   # Clenup Tickit Test Container
   docker stop tickit-test-container
   docker rm tickit-test-container
   ```
   ```bash
   # Cleanup all containers
   docker rm $(docker ps -a -q)
   ```