# Docker Example: Flask, Postgres, Nginx
A simple setup of a Flask app served over Nginx with Postgres back end 

## Running using Docker:
1. Clone the repo: `git clone https://github.com/kirillsavine/docker_example_flask_postgres_nginx.git`
2. Navigate to the root directory of the app: `cd docker_example_flask_postgres_nginx`
3. Run the app: `docker-compose up -d`

## Notes / Troubleshooting
- Ensure that the following network ports are available on your parent system:
	- 1234: for Flask API
	- 80: for Nginx server
	- 5432: for Postgres

- Only tested on Linux environment (Ubuntu 18.04.1 LTS)


## Docker Installation
To run this installation on a newly installed system, Docker and Docker Composed need to be installed first. Please refer to the following guide for Docker installation: https://docs.docker.com/compose/install/

Alternatively use commands for the following script: `install_docker.sh`


## Next Steps

Wrap Docker installation and deployment of the project into an Ansible playbook. I am planning to do this in the near future
