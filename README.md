
# File-Vault

A simple password protected file sharing application written with the python framework **Flask**

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DATABASE_PATH`

`FILES_PATH`

Note: if running this project using docker, use the following environment variable values:

`DATABASE_PATH=/app/data/`
`FILES_PATH=/app/data/files`

## Usage

```
git clone https://github.com/sroffey-github/file-vault.git
cd file-vault
mkdir -p data/files
```

## Docker

This application can be run using docker, first you will have to build the image and then run it with the correct mounted volumes

```
docker build -t file-vault .
docker run -dp 8080:8080 -v <path to data directory>:/app/data --name file-vault file-vault
```
