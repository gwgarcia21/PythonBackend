"""Integration Test a Simple API: Create a simple Flask API 
with a single endpoint that returns a list of users from a database. 
Write an integration test for this endpoint using pytest. Use a 
fixture to create and populate the database with test data."""

from flask import Flask, jsonify

def create_app(get_users_fn):
    app = Flask(__name__)

    @app.route('/api/users', methods=['GET'])
    def get_users():
        return jsonify(get_users_fn())

    return app

# Função real usada em produção
def db_users():
    return {'users': [{'name': "John"}, {'name': "Bob"}, {'name': "Rihanna"}]}

# Usar se rodar diretamente
if __name__ == '__main__':
    app = create_app(db_users)
    app.run(debug=True)