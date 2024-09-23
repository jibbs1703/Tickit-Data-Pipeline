import yaml
from aws_tools import RedShift, Glue

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Connect to AWS Redshift
redshift = RedShift.credentials(config['AWS_REGION'])

# Create Redshift Cluster with Predefined Variables in Config File
redshift.create_redshift_cluster(cluster_identifier=config['CLUSTER_IDENTIFIER'],
                                 db_name=config['DB_NAME'],
                                 master_username=config['MASTER_USERNAME'],
                                 master_user_password=config['MASTER_USER_PASSWORD'],
                                 node_type=config['NODE_TYPE'],
                                 number_of_nodes=config['NUMBER_OF_NODES'],
                                 iam_role=config['REDSHIFT_IAM_ROLE'])

# Connect to Redshift Cluster and Create Database in Redshift
redshift.create_database(cluster_identifier=config['CLUSTER_IDENTIFIER'],
                         db_name=config['DB_NAME'],
                         db_user=config['MASTER_USERNAME'],
                         db_password=config['MASTER_USER_PASSWORD'],
                         port=config['PORT'])

# Connect to AWS Glue
glue = Glue.credentials(config['AWS_REGION'])

# Create Glue Crawler to Catalog Raw Data Tables
glue.create_glue_crawler(crawler_name=config['CRAWLER_NAME'],
                         db_name=config['DB_NAME'],
                         iam_role=config['REDSHIFT_IAM_ROLE'],
                         bucket_name=config['S3_LANDING_BUCKET'])

glue.start_glue_crawler(crawler_name=config['CRAWLER_NAME'])