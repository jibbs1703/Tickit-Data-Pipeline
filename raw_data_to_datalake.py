import pandas as pd
import yaml
from aws_services import S3Buckets

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Get Dataset Tables from Source (Flat Files in this Project)
category = pd.read_csv('data/category.txt', sep='|', names=['CATID', 'CATGROUP', 'CATNAME', 'CATDESC'])
date = pd.read_csv('data/date.txt', sep='|', names=['DATEID', 'CALDATE', 'DAY', 'WEEK', 'MONTH', 'QTR', 'YEAR', 'HOLIDAY'])
event = pd.read_csv('data/event.txt', sep='|', names=['EVENTID', 'VENUEID', 'CATID','DATEID', 'EVENTNAME', 'STARTTIME'])
listing = pd.read_csv('data/listing.txt', sep='|', names=['LISTID', 'SELLERID', 'EVENTID', 'DATEID', 'NUMTICKETS', 'PRICEPERTICKET', 'TOTALPRICE', 'LISTTIME'])
sales = pd.read_csv('data/sales.txt', sep='|', names=['SALESID', 'LISTID', 'SELLERID', 'BUYERID', 'EVENTID', 'DATEID', 'QTYSOLD',	'PRICEPAID', 'COMMISSION', 'SALETIME'])
users = pd.read_csv('data/users.txt', sep='|', names=['USERID', 'USERNAME', 'FIRSTNAME', 'LASTNAME', 'CITY', 'STATE', 'EMAIL', 'PHONE', 'LIKESPORTS'])
venue = pd.read_csv('data/venue.txt', sep='|', names=['VENUEID', 'VENUENAME', 'VENUECITY', 'VENUESTATE', 'VENUESEATS'])

# Connect to AWS S3 Bucket
s3 = S3Buckets.credentials('us-east-2')

# Create Bucket if Given Full Access or Check for Bucket with Permissions Given
s3.create_bucket(config['S3_LANDING_BUCKET'])
print(s3.list_buckets())

# Upload Dataset Tables into AWS S3
s3.upload_dataframe_to_s3(df=category,bucket_name=config['S3_LANDING_BUCKET'], object_name='category.csv')
s3.upload_dataframe_to_s3(df=date,bucket_name=config['S3_LANDING_BUCKET'], object_name='date.csv')
s3.upload_dataframe_to_s3(df=event,bucket_name=config['S3_LANDING_BUCKET'], object_name='event.csv')
s3.upload_dataframe_to_s3(df=listing,bucket_name=config['S3_LANDING_BUCKET'], object_name='listing.csv')
s3.upload_dataframe_to_s3(df=sales,bucket_name=config['S3_LANDING_BUCKET'], object_name='sales.csv')
s3.upload_dataframe_to_s3(df=users,bucket_name=config['S3_LANDING_BUCKET'], object_name='users.csv')
s3.upload_dataframe_to_s3(df=venue,bucket_name=config['S3_LANDING_BUCKET'], object_name='venue.csv')