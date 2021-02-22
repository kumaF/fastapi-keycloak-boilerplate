# Fastapi Keycloak Boilerplate

## Dependencies

- Keycloak
- MongoDB

## Fixes in keycloak

In Admin console
1) Realm -> Client Scopes -> "roles" -> edit
2) Mappers -> Create
3) Add client_id to Audience
   
    ```
    Add to ID Token: on
    Add to access token: on
    Add to userinfo: off
    ```

## Test in development environment

- Setup a virtual environment and install dependencies

    ```
    sudo apt install python3.8

    python3 -m pip install --user virtualenv

    virtualenv venv -p python3.8

    source venv/bin/activate

    pip install -r requirements.txt
    ```
- Dependencies
  - Keycloak
   
    ```
    docker run -p 8080:8080 -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=password -d quay.io/keycloak/keycloak:11.0.3
    ```
  - MongoDB

    ```
    docker run --name mongo -d -p 27017:27017 -v $HOME/mongodb/data:/data/db mongo
    ```
- Start the server

    ```
    uvicorn app.main:app --reload
    ```

### Deploy into production

  - Make sure keycloak is connected to a mysql db
  - Refer to the given k8 configs to get to know how to deploy MySQL & Mongo persistant volumes with persistant volume claims
