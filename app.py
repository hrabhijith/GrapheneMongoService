from flask_graphql_auth.main import GraphQLAuth
from database import init_db
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema
from flask_cors import CORS, cross_origin


# Flask app configuration
app = Flask(__name__)

# Configuration for JWT token genearation
app.config["JWT_SECRET_KEY"] = "amazingapp"  # change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 10  # In minutes
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 1  # In days

cors = CORS(app)
auth = GraphQLAuth(app)

app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

@app.route("/graphql", methods=["GET", "POST"])
@cross_origin()
def graphql_playground():
    pass


if __name__ == '__main__':
    init_db()
    app.run()
