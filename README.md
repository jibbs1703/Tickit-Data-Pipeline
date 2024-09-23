# Tickit Data Pipeline

## Overview

This repository contains a data pipeline that extracts, transforms and loads data from an AWS S3 bucket into
an AWS Redshift table using AWS Glue. The raw data is made available in AWS S3 in its raw form and then the 
pipeline enables AWS Glue extract the raw data from S3 bucket. 

A Glue Crawler catalogs the raw data while a Glue Job runs the Glue script to perform needed transformations
on the data, and stores it into Redshift Cluster. The pipeline ensures that data is efficiently moved 
from a data lake (AWS S3) to a data warehouse (AWS Redshift), using an automated orchestration tool (AWS Glue).

All AWS services are put into a custom python module containing classes for each of the AWS service used in the
ETL process. 

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

## Getting Validated Data into the Data Lake (AWS S3 Bucket)

The raw data is then validated for datatype accuracy using the pydantic library. The pydantic BaseModel is 
used in schema validation of the raw data. The transformed and validated data is then uploaded using a 
custom-written python class that accesses S3 buckets based on permissions given. In this example, the user
was given read and write access to a specific S3 bucket.

However, the extraction and transformation of the data in the data lake depends on business needs. In this
project, the assumption is that the business executives want several columns of each table extracted,
transformed and loaded into a database where it could be easily queried for business analytics tasks and 
machine learning model development.
