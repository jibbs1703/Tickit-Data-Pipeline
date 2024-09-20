# Tickit Data Pipeline
## Overview

This repository contains a data pipeline that extracts, transforms and loads data from an AWS S3 bucket into
an AWS Redshift table using AWS Glue. The raw data is made available in AWS S3 in its raw form and then the 
pipeline enables AWS Glue extract the raw data from S3 bucket. 

A Glue Crawler catalogs the raw data while a Glue Job runs the Glue script to perform needed transformations
on the data, and stores it into Redshift Cluster. The pipeline ensures that data is efficiently moved 
from a data lake (AWS S3) to a data warehouse (AWS Redshift), using an automated orchestration tool (AWS Glue).

## Project Dataset 

This project uses TICKIT, a sample database provided by AWS. The dataset is acquired in its flat file format since
this project aims to take these flat files and transform them into separate tables that make up a database in AWS
Redshift. The database consists of seven tables: two fact tables and five dimensions. To ensure the full ETL process
is demonstrated, a few columns would be added to some of the database tables before it is loaded to the target
storage in AWS Redshift. The final database would have the schema below, with some extra columns beyond the 
original database. 

![Alt text](diagram/tickitdb.png "Tickit Database Schema")

## Getting Raw Data into the Data Lake (AWS S3 Bucket)

The first step is to upload the raw data tables to the data lake (AWS S3). Here, the tables are in their raw 
and untransformed state. The [extract_to_datalake.py](extract_to_datalake.py) file enables the raw data to be
moved from its primary source (SQL server, flat files like txt or csv files, XML, JSON, AWS S3 bucket, AWS RDS) 
into the data lake.

## Getting Validated Data into the Data Lake (AWS S3 Bucket)

The raw data is then validated for datatype accuracy using the pydantic library. The pydantic BaseModel is 
used in schema validation of the raw data. The transformed and validated data is then uploaded using a 
custom-written python class that accesses S3 buckets based on permissions given. In this example, the user
was given read and write access to a specific S3 bucket.

However, the extraction and transformation of the data in the data lake depends on business needs. In this
project, the assumption is that the business executives want several columns of each table extracted,
transformed and loaded into a database where it could be easily queried for business analytics tasks and 
machine learning model development.
