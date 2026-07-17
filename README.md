# DevOps Capstone Project

![Build Status](https://github.com/Sraman01-code/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)
[![License: Apache](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
![Python 3.9](https://img.shields.io/badge/Python-3.9-green.svg)

This repository contains the **Accounts** microservice — a Flask REST API for
managing customer accounts, built as part of the DevOps Capstone Project. It
demonstrates a complete DevOps workflow: Test Driven Development, CI with
GitHub Actions, containerization with Docker, deployment to Kubernetes /
OpenShift, and CD with Tekton pipelines.

## The Accounts Service

The service provides full CRUD operations on customer accounts:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service information |
| `/accounts` | POST | Create a new Account |
| `/accounts` | GET | List all Accounts |
| `/accounts/{id}` | GET | Read an Account |
| `/accounts/{id}` | PUT | Update an Account |
| `/accounts/{id}` | DELETE | Delete an Account |

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Run the test suite
nosetests -v

# Run lint checks
flake8 service

# Run the service (development)
flask --app service:app run

# Run the service (production)
gunicorn --bind 0.0.0.0:8080 service:app
```

## Project Layout

```text
service/            - microservice package
├── __init__.py     - app factory, Talisman + CORS setup
├── config.py       - configuration from environment
├── models.py       - Account model
└── routes.py       - REST API routes

tests/              - unit test package
├── factories.py    - test factories (factory-boy)
├── test_models.py  - model unit tests
└── test_routes.py  - route unit tests

.github/workflows/  - GitHub Actions CI
k8s/                - Kubernetes deployment manifests
tekton/             - Tekton CD pipeline
```

## License

Licensed under the Apache License. This project structure follows the IBM /
Skills Network "Introduction to DevOps" capstone project.
