# import boto3
#
#
# def create_movie_table(dynamodb=None):
#     if not dynamodb:
#         dynamodb = boto3.resource('dynamodb')
#
#     table = dynamodb.create_table(
#         TableName='page_statistic',
#         KeySchema=[
#             {
#                 'AttributeName': 'page_id',
#                 'KeyType': 'HASH'  # Partition key
#             }
#         ],
#         AttributeDefinitions=[
#             {
#                 'AttributeName': 'id',
#                 'AttributeType': 'N'
#             },
#             {
#                 'AttributeName': 'owner',
#                 'AttributeType': 'S'
#             },
#             {
#                 'AttributeName': 'owner_email',
#                 'AttributeType': 'S'
#             },
#             {
#                 'AttributeName': 'uuid',
#                 'AttributeType': 'S'
#             },
#             {
#                 'AttributeName': 'tags',
#                 'AttributeType': 'SS'
#             },
#             {
#                 'AttributeName': 'followers',
#                 'AttributeType': 'SS'
#             },
#             {
#                 'AttributeName': 'following',
#                 'AttributeType': 'SS'
#             },
#             {
#                 'AttributeName': 'name',
#                 'AttributeType': 'S'
#             },
#             {
#                 'AttributeName': 'description',
#                 'AttributeType': 'S'
#             },
#             {
#                 'AttributeName': 'image',
#                 'AttributeType': 'S'
#             },
#             {
#                 'AttributeName': 'is_private',
#                 'AttributeType': 'BOOL'
#             },
#             {
#                 'AttributeName': 'follow_requests',
#                 'AttributeType': 'SS'
#             },
#
#         ],
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 10,
#             'WriteCapacityUnits': 10
#         }
#     )
#     return table
#
#
# if __name__ == '__main__':
#     movie_table = create_movie_table()
#     print("Table status:", movie_table.table_status)
