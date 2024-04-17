#!/usr/bin/env python3
"""
Main module for the API
"""
from flask import Flask, jsonify
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(401)
def unauthorized(error):
    """Error handler for unauthorized requests"""
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == "__main__":
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
