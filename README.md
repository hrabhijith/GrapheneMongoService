
# GraphQL server using Flask and MongoDB

This API is built on Flask Python Framework. This server API implements GraphQL query language using Graphene module and connects to MongoDB for storage (Mongoengine). This API authenticates the client access by creating and serving JWT token.


## GraphQL- What and Why?

1. GraphQL is an improvised language/architecture to implement Server and Client connections on HTTP, mainly to access databases. It has only two main operations, mentioned below, compared to similar and most widely used architecture 'REST'.

   * 'Query' - compared to GET method of REST based implementation.
   * 'Mutation' - compared to POST, PUT, DELETE methods of REST based implementation.

2. GraphQL server can be consumed by a variety of clients and the servers can also be bulit in several languages. [Click here for more details] (https://graphql.org/)

3. **Queries can be modified from client side for filtering the response before the request**, which gives the ability to use same query for multiple types of data access and avoids excess data transfer between server and client.

4. Authentication using GraphQL queries.

5. Easy integration with any server frameworks and database servers.

6. All CRUD operations using similar GraphQL syntax.


## Local Installation [only documented for windows]

1. Clone or Download the project in to a directory.

2. Install latest stable version of Python 3. [https://www.python.org/downloads/]

3. Install virtual environment for Python. [https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/]

    * In terminal, type the below command to install virtual environment.

    `py -m pip3 install --user virtualenv`

    * Type the below command in the project directory to create virtual environment.

    `py -m venv env`

    * Type the below command in the project directory to activate the virtual environment.

    `.\env\Scripts\activate`

4. Type the below command in the project directory to install all required modules.

`pip3 install -r requirements.txt`

5. Execute the below command to run the application.

`python3 app.py`

6. The application will start running at 'localhost:5000'.

7. Clients can connect to this server at 'localhost:5000/graphql' using required client modules.


## Installation and Execution using Docker

1. Make sure you have installed Docker. [https://docs.docker.com/get-docker/] 

2. Download the already built image from Docker hub, using the command below.

    `docker pull hrabhijith/gql-mongo`

3. Run the below command in the terminal.

    `docker run --name <container name> -p 5000:5000 hrabhijith/gql-mongo`

4. The application will start running at 'localhost:5000'.


## Configuration variables

Before running the project either the python command in local or docker run in docker container, the environment variables need to be set.

**Local Execution on Windows**

Run the following commands in CMD terminal.

For Developemnt server

`set CONFIG_ENV=config.DevConfig`

For Production Serve (Not Ideal)

`set CONFIG_ENV=config.ProdConfig`

Set the secret for JWT token creation

`set JWT_SECRET_KEY=yoursecret`

Set the database URI and name

`set DATABASE_URI=databaseuri`

`set DATABASE_NAME=qualiexplore01`

If needed, set the host name and port number(Default: localhost:5000)

`set HOST=hostIP`

`set PORT=portnumber`


**Docker container execution**




## GraphQL Playground

Graphene provides an UI to execute the implemented Queries and Mutations in the server, visualize the input and return value types for those queries and mutations. **Also, the same query syntax is used in all consumable client languages.**

The MongoDb collection (Tables/Documents) used for this demo application is shown below.

**Collection name: Selections**

**Main Document Structure:**

    
    {
        id : Unique String
        name: String
        options: List of embedded documents (Shown below)
    }


**Embedded document Structure:**


    [
        {
            selection_id: String
            value: String
        },

        {
            ...
        }
    ]
    

After the above installation and execution steps, Open a browser and go to 'localhost:5000/graphql'. The UI provides an input field to put quries or mutations, run them and see the results. Below are the inputs in GraphQL language implemented in this API.


1. Generate JWT token. Currently works for all usernames and passwords. When the token expires, refresh token is enough to generate new access token. (See 5)

    ```graphql
     mutation {
          login(password: "", username: "") {
             accessToken
             refreshToken
          }
       }
    ```

**Important step**

2. After the generation of JWT token, a authentication header needs to be set from the client side application. Every request to this server must have this auth header. 

For example, from Apollo Angular client.

```js
const auth = setContext((operation, context) => {
    const token = localStorage.getItem('accessToken');

    if (token === null) {
      return {};
    } else {
      return {
        headers: new HttpHeaders().set('Authorization', `Bearer ${token}`)
      };
    }
  });
```

For more information see GraphQL client documentation page.

3. Examples for 'Query'.

    ```graphql
    query{
        allSelections(){
                id
                name
                options {
                    selectionId
                    value
                }
            }
        }


    query{
        selectionsByName(name: "Goals"){
                id
                name
                options {
                    selectionId
                    value
                }
            }
        }
    ```


4. Examples for 'Mutation'.

    ```graphql
    mutation {
        createData(name: "", options: [{selectionId: "", value: ""}]){
            ok 
            data {
                id 
                options {
                    selectionId
                    value
                    }
                }
            }
        }


    mutation {
        updateData(name: "", options: [{selectionId: "", value: ""}, 
                                                {selectionId: "", value: ""}]){
            ok 
            data {
                id 
                name
                options {
                    selectionId
                    value
                    }
                }
            }
        }

    mutation {
        deleteData(name: "", selectionId: ""){
            ok 
            data {
                id 
                name
                options{
                    selectionId 
                    value
                    }
                }
            }
        }
    ```


5. Example for query results filtering before the request. Multiple usage of same queries methods. **One of the main advantages of GraphQL.** Same method can be used to get many or one item. 

    ```graphql
    query{
        allSelections(){
            options {
                value
                }
            }
        }
        
    query{
        allSelections(){
            id
            name
            }
        }
    ```

Both the above queries are valid. The first returns just the 'value' from 'options' list from all documents. 

The second returns 'id' and 'name' from all documents.

Likewise, return values can be selected from the client side for all the implementations.


6. Generate refresh token.

    ```graphql
    mutation {
          refresh(refreshToken: "") {
             newToken
          }
       }
    ```

