mkdir -p project/{agents,data/{cache},examples/generated_app,tests,utils}
touch project/main.py
touch project/agents/{__init__.py,collector_agent.py,generator_agent.py,validator_agent.py,coordinator_agent.py}
touch project/utils/{__init__.py,firecrawl_wrapper.py,nemo_utils.py}
touch project/tests/test_cases.py
touch project/examples/Dockerfile
touch project/.env
touch project/config/__init__.py 
mkdir -p project/examples/{templates,generated_code,docker}
touch project/examples/docker/Dockerfile.base
touch project/examples/docker/Dockerfile.test
touch project/examples/docker/docker-compose.yml
touch project/examples/templates/{flask_app.py,django_app.py,fastapi_app.py}
touch project/README.md 