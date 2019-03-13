#!/bin/bash


# Immediately exits if any error occurs during the script
# execution. If not set, an error could occur and the
# script would continue its execution.
set -o errexit


# Main execution:
# - verifies if all environment variables are set
# - runs the SQL code to create user and database
main() {
  init_user_and_db
}



# Performs the initialization in the already-started PostgreSQL
# using the preconfigured POSTGRE_USER user.
init_user_and_db() {
  psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
	CREATE DATABASE mydb;
	CREATE TABLE mydb."log" (
		"id" INTEGER NULL DEFAULT NULL,
		"user" INTEGER NULL DEFAULT NULL,
		"x" CHAR(50) NULL DEFAULT NULL
	);
EOSQL
}

# Executes the main routine with environment variables
# passed through the command line. We don't use them in
# this script but now you know 🤓
main "$@"
