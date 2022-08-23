# ResourceManager

* Run microservice using Dockerfile:
    * docker build -t image-name .
    * docker run -p 5000:8000 --env-file=.env image-name
    * Visit "http://localhost:5000/graphql"
    
     
* Run getAccounts query in GraphiQL environment:
    
 ```graphql
query getAccounts {
  accounts {
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
```

 * Run updateAccount mutation in GraphiQL environment
 ```graphql
mutation  {
  updateAccount(selectedUid: "wns", updatedUid: "wns2", gecos: "Ben Smith", uidNumber: 1256, eppns: ["ben@gmail.com"], trainingUptodate: true, lastAccountActivity: "2022-08-27T21:28:09Z") {
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
```

* Note: updateAccount mutation allows arbitrary updates of any fields. The 
record that is updated depends on the selectedUid. An UpdateAccountError is thrown if:
    * There is no account with the selected uid
    * A duplicate uid or uidNumber is used since the database has unique index constraints on these fields
    * An invalid isoformat datetime string is used
    
* client.py sample program shows a statement for updating the "wns" user with the current time
in the "last_account_activity" field. The mutation validates the datetime format.

* updateAccountActivity mutation for updating "last_account_activity" to current time
```graphql
mutation  {
  updateAccountActivity(uid: "wns2") {
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
```

* Authentication & Authorization: 
    * MongoDB Cluster: The MongoDB Atlas cluster that stores the account records uses database
credentials for authentication. The database credentials are currently stored in the 
.env file. This file could be put in .gitignore for production, but will be committed for testing.
Authentication can also involve IP Address whitelisting. Only approved IP Addresses 
configured for the MongoDB Atlas database can access its data. For now, all IP Addresses have permission to access
the cluster's data for testing. MongoDB also has authorization functionality for setting roles with read/write permissions for database users. 
    
    * User Account Authentication: If implementing user account authentication, an authentication/authorization library 
such as Auth0 or Okta can be used for storing an authentication token on the server side to be verified by
Auth0. This would prevent handling passwords directly on the server. Auth0 also provides support for tracking
account permissions associated with a user's token. If implementing authentication using credentials
ourselves, the passwords must be encrypted.

* TECHNOLOGIES:
    * PROS:
        * Strawberry has a lightweight api that is easy to learn and implement graphql queries and mutations with.
        It uses both dataclasses and typehints. 
        
        * Mongodb is easy to use through its simple API as opposed to using the sqlite library where sql queries
        are executed by a cursor. Since this example didn't require joining multiple data sources 
        together with the account information, there wasn't any difficulty using MongoDB.
    
    * CONS:
        * Strawberry had no integration with MongoDB and very few examples. Graphene could have been a 
        better choice due to it having builtin support with Mongoengine which simplifies connecting
        GraphQL models to Mongo collections. Graphene also has more examples since its an
        older framework. The Strawberry framework is less stable since its much newer. 
        
        * If more relations between data sources is needed in the future, it might be better
        to switch to a SQL database schema since Mongodb support for Joins on collections was only
        recently added.