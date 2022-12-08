# Role Based Access Control HTTP File Server

## Description
This project will store files over a distributed MooseFS cluster, users must authenticate themselves via the role-based access control server and have appropriate permissions for the category they wish to access. Users can upload files, retrieve a list of accessible files in a category and download a file.

## Structure
### DB
This folder contains the initial schema for the database including some example users and roles
### Diagrams
This folder contains architecture diagrams for the project
### MooseFS-Chunkserver
This folder contains the DockerFile for the indidvidual chunkservers for MooseFS
### MooseFS-Master
This folder contains the DockerFile for the MooseFS master server
### RBAC-Server
This folder contains the code for the role-based access control server

## Running
### Prerequisites
This project requires Docker.
### Building
To build the containers, issue the following command in the root directory:

    docker-compose build

This will create the seven containers required to run the project.
### Running
To run the project, issue the following command in the root directory:

	docker-compose up

This will start the seven containers required:
1. mfschunkserver1-4 - The four chunk servers where data will be stored
2. mfsmaster - The master server used to communicate with the chunk servers
3. rbac-server - The public facing API used to access the files
4. rbac-db - The database storing user information

## Default Configuration
### Access
To access the API, import the Postman_endpoints.json into Postman, where several example requests are included, by default the server will run on localhost:5000

### Accounts
The project is set up with two default roles and five user accounts, each with varying permissions, those permissions are as shown:

| Username | Password   | ex_role_1 |       | ex_role_2 |       |
|----------|------------|-----------|-------|-----------|-------|
|          |            | read      | write | read      | write |
| user_a   | password_a | Yes       | Yes   | Yes       | Yes   |
| user_b   | password_b | Yes       | No    | Yes       | No    |
| user_c   | password_c | No        | Yes   | No        | Yes   |
| user_d   | password_d | Yes       | Yes   | No        | No    |
| user_e   | password_e | No        | No    | No        | No    |

