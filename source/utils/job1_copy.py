import boto3
import sys
from vaultUtil import VaultClient
from awsUtils import AWSConnector

VAULT_URL = "http://127.0.0.1:8200"
ROLE_ID = "f127dd51-47ae-be9f-fdac-8633205417c6"
SECRET_ID = "96d9db52-dd21-f678-f75b-e26534590179"
SECRET_PATH = "secret/data/aws"

vault_client = VaultClient(VAULT_URL, ROLE_ID, SECRET_ID, SECRET_PATH)
token = vault_client.authenticate_with_approle()

if token:
    secret_data = vault_client.get_secret(token)
    if secret_data:
        print("Secret data:", secret_data)

        aws_access_key = secret_data['data']['sh-accesskey']
        aws_secret_key = secret_data['data']['sh-secretkey']

        region = 'us-east-1'  # Replace with your preferred AWS region

        client = 'iam'
        aws_connector = AWSConnector(aws_access_key, aws_secret_key, client, region)

        # Access the IAM client through the instance
        iam_client = aws_connector.aws_client_conn

        # Now you can use iam_client to perform IAM operations
        response = iam_client.list_groups()

        print("IAM groups:", response)

    else:
        print("Failed to retrieve secret.")
else:
    print("Failed to authenticate with AppRole.")




# # Replace these with your Snowflake account details
# account = 'lqa91709.east-us-2.azure.snowflakecomputing.com'

# SECRET_PATH = "secret/data/snow"

# vault_client = VaultClient(VAULT_URL, ROLE_ID, SECRET_ID, SECRET_PATH)
# token = vault_client.authenticate_with_approle()

# if token:
#     secret_data = vault_client.get_secret(token)
#     if secret_data:
#         print("Secret data:", secret_data)
#     else:
#         print("Failed to retrieve secret.")
# else:
#     print("Failed to authenticate with AppRole.")


# user = secret_data['data']['bw-snow-serviceusername-dev']
# password = secret_data['data']['bw-snow-serviceuserpassword-dev']


# # user = 'RMAHAJAN'
# # password = 'Brainworks@2023'



# warehouse = 'COMPUTE_WH'
# database = 'SNOWFLAKE_SAMPLE_DATA'
# schema = 'TPCH_SF1'

# # Create an instance of SnowflakeConnector
# snowflake_conn = SnowflakeConnector(account, user, password, warehouse, database, schema)

# # Connect to Snowflake
# snowflake_conn.connect()

# # Execute a query
# query_result = snowflake_conn.execute_query("SELECT * from SUPPLIER")

# # Print the result
# print("Current Date in Snowflake:", query_result[0][0])

# # Close the connection
# snowflake_conn.close_connection()