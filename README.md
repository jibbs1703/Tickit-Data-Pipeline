# Tickit Data Pipeline

## Overview

This repository contains a data pipeline that extracts, transforms and loads data from an AWS S3 bucket into
an AWS Redshift table using AWS Glue. The raw data is made available in AWS S3 in its raw form and then the 
pipeline enables AWS Glue extract the raw data from S3 bucket. 

A Glue Crawler catalogs the raw data while a Glue Job runs the Glue script to perform needed transformations
on the data, and stores it into Redshift Cluster. The pipeline ensures that data is efficiently moved 
from a data lake (AWS S3) to a data warehouse (AWS Redshift), using an ETL tool (AWS Glue). The whole pipeline is
orchestrated using Apache-Airflow. 

All AWS services are put into a custom python module containing classes for each of the AWS service used in the
ETL process. The airflow DAGs orchestrate the whole ETL process using the AWS services. 

## Project Dataset and Business Goal

This project uses TICKIT, a sample database provided by AWS. The dataset is acquired in its flat file format since
this project aims to take these flat files and transform them into separate tables that make up a database in AWS
Redshift. The database consists of seven tables: two fact tables and five dimensions. 

In this project, the business goal is to provide business executives with an idea of which sellers sold the most 
tickets, what region of the country saw the most sales during the year and what region brought in the most sales
commission for the year.

The final database would combine information from all the tables into one consolidated format. The data includes
users who sold tickets, venues where events took place, events and their categories, dates, ticket listings, and
sales details. 

![Alt text](diagram/tickitdb.png "Tickit Database Schema")

## Getting Raw Data into the Data Lake (AWS S3 Bucket)

The first step is to upload the raw data tables to the data lake (AWS S3). Here, the tables are in their raw 
and untransformed state. The [extract_to_datalake.py](extract_to_datalake.py) file enables the raw data to be
moved from its primary source (SQL server, flat files like txt or csv files, XML, JSON, AWS S3 bucket, AWS RDS) 
into the data lake. 

This first step orchestrated by Airflow and since this pipeline performs the ETL process on data in batches, 
the ingestion into the data lake can be put at specific intervals.

However, in this project, this first step is skipped as it is not performed within the data pipeline constructed.

## Getting Validated Data into the Data Lake (AWS S3 Bucket)

The raw data is then validated for datatype accuracy using the pydantic library. The pydantic BaseModel is 
used in schema validation of the raw data. The transformed and validated data is then uploaded using a 
custom-written python class that accesses S3 buckets based on permissions given. In this example, the user
was given read and write access to a specific S3 bucket.

However, the extraction and transformation of the data in the data lake depends on business needs. In this
project, the assumption is that the business executives want several columns of each table extracted,
transformed and loaded into a database where it could be easily queried for business analytics tasks and 
machine learning model development.

However, in this project, the raw and untransformed data had been validated while it was ingested into the
landing area and the data engineer needs not worry about the data validation and type testing with Pydantic.

## Getting Required IAM Access to Use Services

To access the AWS resources needed for this data pipeline, the appropriate roles and permissions need to be
assigned. This was done on the AWS console but an IAM role file could also be used to create roles and permissions
via IaaC services like Terraform or AWS CloudFormation on the command line.

For this data pipeline, the IAM role created allowed access to AWS RedShift, AWS Glue, and AWS S3. The role was 
configured such that the user could use Glue to access S3, Redshift, and the Glue data catalog.

## Data Warehouse Setup

As part of the pipeline design, the target destination needs to match the incoming transformed data. To prepare the 
data warehouse, AWS Redshift is database is provisioned by first creating a Redshift cluster, then creating a database
within the cluster and finally, creating a table in the required schema in the redshift cluster. This table and its schema
must match the schema of the incoming data after transformation has been done.

## Cataloging Raw Data in Data Lake (AWS S3)

To catalog the raw data stored in the data lake (AWS S3), an AWS Glue Crawler was created and run. This glue crawler
connects to S3 bucket with the raw data, infers data schemas, and creates metadata table definitions in a Data Catalog.
The Glue Crawler populates the Data Catalog with table metadata from the raw data.

## Data Transformation and Loading into Data Warehouse

After the data catalog is developed, the next step is to define the ETL jobs with transformation scripts to move and 
process the raw data. The data transformation script is stored in a separate S3 bucket as [tickit_etl_script] 
(tickit_etl_script) and to perform the data transformation, a glue job is created and run to access the script in S3
and run the contents, thereby transforming the data. 

As part of the glue job, the script also contains the redshift connection to load the results of the data 
transformation into the created AWS Redshift Database. Alternatively, this pipeline could be modified such that the 
transformed data is loaded to a destination S3 bucket and then copied into Redshift on arrival using the 'COPY' command.


## Further Out-of-Scope Solutions

As part of designing a cost-effective data pipeline, each batch of the data could be aggregated and put in cold storage 
at certain intervals depending on the volume of the data. This helps save costs in the datalake and take out already 
processed data from the datalake. 


