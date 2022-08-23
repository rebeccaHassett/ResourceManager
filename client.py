from python_graphql_client import GraphqlClient
from datetime import  datetime

# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="http://localhost:5000/graphql")

# Create the query string and variables required for the request.
mutation = """
    mutation updateAccount($selectedUid: String!, $lastAccountActivity: String) {
        updateAccount(selectedUid: $selectedUid, lastAccountActivity: $lastAccountActivity) {
            __typename
            ... on UpdateAccountError {
                errorMessage
            }
            ... on UpdateAccountSuccess {
            account {
                uid
                gecos
                uidNumber
                eppns
                status {
                    trainingUptodate
                    lastAccountActivity
                }
            }
            }
        }
    }
"""
variables = {"selectedUid": "wns", "lastAccountActivity": datetime.now().isoformat()}

data = client.execute(query=mutation, variables=variables)
print(data)
