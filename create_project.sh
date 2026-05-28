#!/bin/bash

PROJECT_NAME="vertex-mock-framework"

echo "Creating project: $PROJECT_NAME"

# Create folders
mkdir -p $PROJECT_NAME/app
mkdir -p $PROJECT_NAME/tests

# Create app files
touch $PROJECT_NAME/app/__init__.py
touch $PROJECT_NAME/app/vertex_client.py
touch $PROJECT_NAME/app/responses.py

# Create test files
touch $PROJECT_NAME/tests/__init__.py
touch $PROJECT_NAME/tests/test_vertex_client.py

# Create root files
touch $PROJECT_NAME/conftest.py
touch $PROJECT_NAME/requirements.txt
touch $PROJECT_NAME/README.md

echo "✅ Project structure created successfully!"
echo "➡️ Run: cd $PROJECT_NAME"
