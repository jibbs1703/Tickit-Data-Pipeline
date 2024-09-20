import yaml
from aws_services import RedShift

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

redshift = RedShift.credentials(config['AWS_REGION'])
redshift.create_redshift_cluster(cluster_identifier=config['CLUSTER_IDENTIFIER'],
                                 db_name=config['DB_NAME'],
                                 master_username=config['MASTER_USERNAME'],
                                 master_user_password=config['MASTER_USER_PASSWORD'],
                                 node_type=config['NODE_TYPE'],
                                 number_of_nodes=config['NUMBER_OF_NODES'],
                                 iam_role=config['REDSHIFT_IAM_ROLE'])