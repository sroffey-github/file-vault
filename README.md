
# File-Vault

A simple password protected file sharing application written with the python framework **Flask**

## Docker

This application can be run using docker

- create a `data` directory (the files and database will be stored here for persistance)
- pull the docker image from githubs registry
- run the container with the command below

```
docker pull ghcr.io/sroffey-github/file-vault
docker run --rm -dp 8080:8080 -v <absolute path to your data directory>:/app/data ghcr.io/sroffey-github/file-vault
```