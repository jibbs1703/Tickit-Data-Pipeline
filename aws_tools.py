import os
import tempfile
import logging
import boto3
import psycopg2
import joblib
import psycopg2
from botocore.exceptions import ClientError
from io import StringIO
from dotenv import load_dotenv


class S3Buckets:
    @classmethod
    def credentials(cls, region=None):
        """
        The credentials @classmethod runs when the S3Buckets class is initialized. This method accesses
        the secret and access keys for the user. These keys are specified in a hidden env file in the
        directory. When a region is specified, the S3 Bucket methods called are executed in the specified
        region and if no region is specified, AWS assigns a region while using the services.
        the region argument

        :param region:
        :return: secret key, access key, region specified by user
        """
        # Load the User's Access and Secret Key from .env file
        load_dotenv()
        secret = os.getenv("SECRET_KEY")
        access = os.getenv("ACCESS_KEY")
        return cls(secret, access, region)

    def __init__(self, secret, access, region):
        """
        The __init__ method for the S3Buckets class creates the client for accessing the user's AWS account.
        The client is created using the boto3 module and is made globally available in the S3Buckets class
        for subsequent methods in the class.

        :param secret: user secret key (loaded from .env file)
        :param access: ser access key (loaded from .env file)
        :param region: specified region during instantiation of class
        """
        if region is None:
            self.client = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
            print(secret, access, region)
        else:
            self.location = {'LocationConstraint': region}
            self.client = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret, region_name=region)

    def list_buckets(self):
        """
        This method returns a list of bucket names available in the user's AWS account.

        :return: a list of the s3 bucket instances present in the accessed account
        """
        response = self.client.list_buckets()
        buckets = response["Buckets"]
        all_buckets = [bucket["Name"] for bucket in buckets]
        return all_buckets

    def create_bucket(self, bucket_name):
        """
        This method creates an S3 bucket in the user's AWS account in the region specified while
        instantiating the class. A new bucket is created if the bucket name passed into the
        method has not been previously created. If a region is not specified, the bucket is
        created in the S3 default region (us-east-1).

        :param bucket_name:
        """
        if bucket_name in self.list_buckets():
            print(f"The bucket {bucket_name} already exists")
            pass
        else:
            print("A new bucket will be created in your AWS account")
            self.client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=self.location)
            print(f"The bucket {bucket_name} has been successfully created")

    def upload_file(self, file_name, bucket_name, object_name=None):
        """
        This method uploads a file to an S3 bucket in the user's AWS account

        :param file_name: File to upload to S3 Bucket
        :param bucket_name: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        # If S3 object_name is not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)
        try:
            self.client.upload_file(file_name, bucket_name, object_name)

        except ClientError as e:
            logging.error(e)
            return False
        return True

    def download_file(self, bucket_name, object_name, file_name):
        """
        This method downloads a file from an S3 bucket in the user's AWS account.

        :param bucket_name: Bucket to download file from
        :param object_name: File to download from S3 Bucket
        :param file_name: Filename to save the file to.
        :return: Downloaded file
        """
        file = self.client.download_file(bucket_name, object_name, file_name)
        return file

    def read_file(self, bucket_name, object_name):
        """
        This method reads a file from an S3 bucket in the user's AWS account, returns an object
        containing the file read.

        :param bucket_name: Bucket to read file from
        :param object_name: File to read from S3 Bucket
        :return: an object containing the file read from the S3 Bucket.
        """
        response = self.client.get_object(Bucket=bucket_name, Key=object_name)
        file = StringIO(response['Body'].read().decode('utf-8'))
        return file

    def save_model_to_s3(self, model, bucket_name, model_name):
        """
        This method uploads a model to an S3 bucket in the user's AWS account.

        :param bucket_name: S3 Bucket to upload model to.
        :param model_name: name for model in S3 Bucket.
        :return: Message if model is successfully uploaded.
        """
        with tempfile.TemporaryFile() as fp:
            joblib.dump(model, fp)
            fp.seek(0)
            self.client.put_object(Body=fp.read(), Bucket=bucket_name, Key=model_name)
            print(f"The model {model_name} has been uploaded to the S3 bucket {bucket_name}")

    def load_model_from_s3(self, bucket_name, model_name):
        """
        This method downloads a file from an S3 bucket in the user's AWS account.

        :param bucket_name: Bucket to download saved model from
        :param model_name: model to download from S3 Bucket
        :return: Loaded Model
        """
        with tempfile.TemporaryFile() as fp:
            self.client.download_fileobj(Fileobj=fp, Bucket=bucket_name, Key=model_name)
            fp.seek(0)
            model = joblib.load(fp)
            return model

    def delete_file(self, bucket_name, object_name):
        """
        This method removes an object/file from an S3 Bucket instance in the user's AWS account.

        :param bucket_name: S3 Bucket where file exists.
        :param object_name: File to remove from specified S3 Bucket
        :return: "Delete Successful" if method wa completed.
        """
        self.client.delete_object(Bucket=bucket_name, Key=object_name)
        print("Delete Successful")

    def upload_dataframe_to_s3(self, df, bucket_name, object_name):
        """
        This method uploads a pandas dataframe to an S3 bucket in the user's AWS account

        :param df: dataframe to upload to S3 Bucket
        :param bucket_name: Bucket to upload dataframe to
        :param object_name: name dataframe takes in the is user's s3 bucket.
        :return: Success message if file was uploaded.
        """
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, header=True, index=False)
        self.client.put_object(Bucket=bucket_name, Body=csv_buffer.getvalue(), Key = object_name)
        print("Dataframe is saved as CSV in S3 bucket.")


class RedShift:
    @classmethod
    def credentials(cls, region=None):
        # Load the User's Access and Secret Key from .env file
        load_dotenv()
        secret = os.getenv("SECRET_KEY")
        access = os.getenv("ACCESS_KEY")
        return cls(secret, access, region)

    def __init__(self, secret, access, region):
        if region is None:
            self.client = boto3.client('redshift', aws_access_key_id=access, aws_secret_access_key=secret)
            self.db_credentials = None
        else:
            self.location = {'LocationConstraint': region}
            self.client = boto3.client('redshift', aws_access_key_id=access, aws_secret_access_key=secret, region_name=region)
            self.db_credentials = None

    def create_redshift_cluster(self, cluster_identifier, node_type, master_username, master_user_password, db_name, iam_role, number_of_nodes):
        try:
            response = self.client.create_cluster(
                ClusterIdentifier=cluster_identifier,
                NodeType=node_type,
                MasterUsername=master_username,
                MasterUserPassword=master_user_password,
                DBName=db_name,
                NumberOfNodes=number_of_nodes,
                IamRoles=[iam_role]
            )
            print(f"Cluster {cluster_identifier} has been created.")

        except Exception as e:
            print(f"Error creating Redshift cluster: {e}")

    def create_database(self, cluster_identifier, db_name, db_user, db_password, port):
        try:
            cluster_props = self.client.describe_clusters(ClusterIdentifier=cluster_identifier)['Clusters'][0]
            endpoint = cluster_props['Endpoint']['Address']

            conn = psycopg2.connect(
                dbname=db_name,  # Typically the default DB in Redshift
                user=db_user,
                password=db_password,
                host=endpoint,
                port=port
            )
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE {db_name};")
            conn.commit()
            cur.close()
            conn.close()
            print(f"Database {db_name} created successfully.")
        except Exception as e:
            print(f"Error creating database: {e}")

    def drop_database(self, cluster_identifier, db_name, db_user, db_password):
        try:
            cluster_props = self.client.describe_clusters(ClusterIdentifier=cluster_identifier)['Clusters'][0]
            endpoint = cluster_props['Endpoint']['Address']
            port = cluster_props['Endpoint']['Port']

            # Assuming you have psycopg2 installed for PostgreSQL connection to Redshift
            import psycopg2
            conn = psycopg2.connect(
                dbname="dev",  # Typically the default DB in Redshift
                user=db_user,
                password=db_password,
                host=endpoint,
                port=port
            )
            cur = conn.cursor()
            cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
            conn.commit()
            cur.close()
            conn.close()
            print(f"Database {db_name} dropped successfully.")
        except Exception as e:
            print(f"Error dropping database: {e}")








class Glue:
    @classmethod
    def credentials(cls, region=None):
        # Load the User's Access and Secret Key from .env file
        load_dotenv()
        secret = os.getenv("SECRET_KEY")
        access = os.getenv("ACCESS_KEY")
        return cls(secret, access, region)

    def __init__(self, secret, access, region):
        if region is None:
            self.client = boto3.client('glue', aws_access_key_id=access, aws_secret_access_key=secret)
        else:
            self.location = {'LocationConstraint': region}
            self.client = boto3.client('glue', aws_access_key_id=access, aws_secret_access_key=secret,
                                       region_name=region)

    def create_glue_crawler(self, crawler_name, iam_role, bucket_name, db_name):

        try:
            response = self.client.create_crawler(
                Name=crawler_name,
                Role=iam_role,
                DatabaseName=db_name,
                Targets={'S3Targets': [{'Path': f's3://{bucket_name}/'}]})

            print(f"Crawler '{crawler_name}' created successfully.")
            return response

        except Exception as e:
            print(f"Error creating crawler: {e}")

    def start_glue_crawler(self, crawler_name):
        # Start the crawler
        self.client.start_crawler(Name=crawler_name)
        print("Glue Crawler created and started.")
