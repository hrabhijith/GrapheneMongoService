
# GraphQL server using Flask and MongoDB

This API is built on Flask Python Framework. This server API implements GraphQL query language using Graphene module and connects to MongoDB for storage (Mongoengine). This API authenticates the access by creating and serving JWT token.

## GraphQL- What and Why?

1. GraphQL is an improvised language/architecture to implement Server and Client connections on HTTP, mainly to access databases. It has only two main operations, mentioned below, compared to similar and most widely used architecture 'REST'.

   * 'Query' - compared to GET method of REST based implementation.
   * 'Mutation' - compared to POST, PUT, DELETE methods of REST based implementation.

2. GraphQL server can be consumed by a variety of clients and the servers can also be bulit in several languages. [Click here for more details] (https://graphql.org/)

3. Queries can be modified from client side, which gives the ability to use same query for multiple types of data access and avoids excess data transfer between server and client.

4. Authentication using GraphQL queries.

5. Easy integration with any server frameworks and database servers.

6. All CRUD operations using similar GraphQL syntax.


## Local Installation [only documented for windows]

1. Clone or Download the project in to a directory.

2. Install latest stable version of Python 3. [Download] (https://www.python.org/downloads/)

3. Install virtual environment for Python. [More details] (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

In terminal, type the below command to install virtual environment.
`py -m pip3 install --user virtualenv`

Type the below command in the project directory to create virtual environment.
`py -m venv env`

Type the below command in the project directory to activate the virtual environment.
`.\env\Scripts\activate`

4. Type the below command in the project directory to install all required modules.
`pip3 install -r requirements.txt`

5. Execute the below command to run the application.
`python3 app.py`

6. The application will start running at 'localhost:5000'.

7. Clients can connect to this server at 'localhost:5000/graphql' using required client modules.


## GraphQL Playground

Graphene provides an UI to execute the implemented Queries and Mutations in the server, visualize the input and return value types for those queries and mutations. **Also, the same query syntax is used in all consumable client languages.**

1. After the above installation and execution steps, Open a browser and go to 'localhost:5000/graphql'
![GraphQL Playground!](/assets/graphql1.jpg "GraphQL Playground")

2. Generate JWT token.


