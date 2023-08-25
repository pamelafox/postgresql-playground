# PostgreSQL Dev Container / Codespace

This is a PostgreSQL dev container for use with VS Code Remote Containers or GitHub Codespaces.
The devcontainer.json uses a docker-compose.yaml to set up a local PostgreSQL server inside the container.

For use with the local PostgreSQL server,  copy `.env.devcontainer` into `.env`.

For use with an Azure PostgreSQL server,  copy `.env.azure` into `.env` and adjust the host name, user name, and password.

Then run either `main_psycopg.py` or `main_sqlalchemy.py` to interact with the database.