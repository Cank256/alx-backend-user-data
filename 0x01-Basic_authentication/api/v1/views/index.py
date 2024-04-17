#!/usr/bin/env python3
"""
Index module for API
"""
from flask import Blueprint, abort

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

@app_views.route('/unauthorized', methods=['GET'])
def unauthorized():
    """Route to trigger unauthorized error"""
    abort(401)

