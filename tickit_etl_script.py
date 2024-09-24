import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as SqlFuncs

# Get Job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'REDSHIFT_DB', 'REDSHIFT_TABLE', 'REDSHIFT_USER', 'REDSHIFT_PASSWORD', 'REDSHIFT_ENDPOINT'])


# Initialize Glue context and job
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load the data from Glue Data Catalog
datasource_customer = glueContext.create_dynamic_frame.from_catalog(
    database="ecommerce_sales_database",
    table_name="etl_customer_csv"
)

datasource_product = glueContext.create_dynamic_frame.from_catalog(
    database="ecommerce_sales_database",
    table_name="etl_product_csv"
)

datasource_order = glueContext.create_dynamic_frame.from_catalog(
    database="ecommerce_sales_database",
    table_name="etl_order_csv"
)

# Step 1: Mapping/Schema Change
# Rename columns
Category_ChangeSchema = datasource_customer.apply_mapping([
    ("customer id", "bigint", "c_customer_id", "bigint"),
    ("first_name", "string", "first_name", "string"),
    ("last_name", "string", "last_name", "string"),
    ("email", "string", "email", "string"),
    ("gender", "string", "gender", "string"),
    ("phone", "string", "phone", "string"),
    ("address", "string", "address", "string")
])

Product_ChangeSchema = datasource_product.apply_mapping([
    ("product id", "bigint", "p_product_id", "bigint"),
    ("name", "string", "product_name", "string"),
    ("description", "string", "description", "string"),
    ("price", "double", "p_price", "float"),
    ("stock quantity", "bigint", "stock_quantity", "bigint")
])

Order_ChangeSchema = datasource_order.apply_mapping([
    ("order id", "bigint", "order_id", "bigint"),
    ("customer id", "bigint", "customer_id", "bigint"),
    ("product id", "bigint", "product_id", "bigint"),
    ("quantity", "bigint", "quantity", "bigint"),
    ("price", "double", "price", "float"),
    ("order date", "string", "order_date", "string")
])

# Step 2: Drop Duplicates
drop_duplicates_customer =  DynamicFrame.fromDF(Customer_ChangeSchema.toDF().dropDuplicates(), glueContext, "drop_duplicates_customer")
drop_duplicates_product =  DynamicFrame.fromDF(Product_ChangeSchema.toDF().dropDuplicates(), glueContext, "drop_duplicates_product")
drop_duplicates_order =  DynamicFrame.fromDF(Order_ChangeSchema.toDF().dropDuplicates(), glueContext, "drop_duplicates_order")

# Step 3: Drop Fields
CustomerDropFields = DropFields.apply(frame=drop_duplicates_customer, paths=["email", "phone", "address"])
ProductDropFields = DropFields.apply(frame=drop_duplicates_product, paths=["description", "p_price"])

# Step 4: Data Cleaning
# Drop null fields in CustomerID and Invoice
cleaned_order = Filter.apply(frame=drop_duplicates_order, f=lambda x: x["customer_id"] is not None and x["order_id"] is not None and x["product_id"] is not None)
cleaned_customer = Filter.apply(frame=CustomerDropFields, f=lambda x: x["c_customer_id"] is not None)
cleaned_product = Filter.apply(frame=ProductDropFields, f=lambda x: x["p_product_id"] is not None)

# Filter out rows where Quantity or Price are negative
filtered_order = Filter.apply(frame=cleaned_order, f=lambda x: x["quantity"] > 0 and x["price"] > 0)

filtered_product = Filter.apply(frame=cleaned_product, f=lambda row: row["stock_quantity"] >= 0)

# Step 5: Add New Column
# Calculate TotalAmount as Quantity * unit_price
# Define a function to calculate the derived column
def add_total_amount(row):
    row["total_amount"] = row["quantity"] * row["price"]
    return row
new_column_order = Map.apply(frame=filtered_order, f=add_total_amount)

# Script for node Join
Join_Product_Order= Join.apply(frame1=new_column_order, frame2=filtered_product, keys1=["product_id"], keys2=["p_product_id"])

# Script for node Join
Join_Customer_Order = Join.apply(frame1=Join_Product_Order, frame2=cleaned_customer, keys1=["customer_id"], keys2=["c_customer_id"])

# Script for node Drop Fields
cleaned_dynamic_frame = DropFields.apply(frame=Join_Customer_Order, paths=["c_customer_id", "p_product_id"])

# Function to drop fields with null values
def drop_null_fields(rec):
    return {key: value for key, value in rec.items() if value is not None}

# Apply the function to the DynamicFrame using Map transformation
Final_dyf = Map.apply(frame=cleaned_dynamic_frame, f=drop_null_fields)


# Specify the Redshift connection options
redshift_options = {
    "url": "jdbc:redshift://ecommerce-cluster.csdvfepxn6le.us-east-2.redshift.amazonaws.com:5439/dev_ecommerce",
    "user": "awsuser",
    "password": "Password123",
    "dbtable": "ecommerce_orders",
    "aws_iam_role": "arn:aws:iam::024848463817:role/Glue_Sales_ETL_Role",
    "tempdir": "s3://ecommerce-sales-etl-bucket/temp/",
}

# Write to Redshift
response = glueContext.write_dynamic_frame.from_jdbc_conf(
    frame = Final_dyf,
    catalog_connection = "",
    connection_options = redshift_options,
    redshift_tmp_dir = "s3://ecommerce-sales-etl-bucket/temp/"
)

# Commit the job
job.commit()