#### About
Supports file uploads and reconciliation processing.

#### Features
- [x] Authentication.
- [x] Reconciliation.

#### Stack
- Django
- Django-restframework
- Postgres

#### How to Run locally 🚀

##### Docker Compose

1. Build the image:

   ```sh
   $ docker compose build
   ```

2. Run the image:

   ```sh
   $ docker compose up --build
   OR
   $ docker-compose up -d
   ```
3. Visit API sandbox navigate to
   ```sh
   http://localhost:8000/api/docs/
   ```

##### Manual Setup

1. Create and activate a virtual environment:

   ```sh
   $ python3 -m venv venv && source venv/bin/activate
   ```

2. Install the requirements:

   ```sh
   (venv) pip install -r requirements/base.txt
   (venv) pip install -r requirements/tests.txt
   ```

###### NOTE! Ensure a `DATABASE_NAME` is created with a `DATABASE_USER` that has a `CREATEDB` role

3. Create a file `env.sh` and paste the below contents, edit the values appropriately
    ```bash
    export DATABASE_NAME=recon_db
    export DATABASE_USER=recon_user
    export DATABASE_PASSWORD=recon_pass
    export DATABASE_HOST=localhost
    export DATABASE_PORT=5432
    export SECRET_KEY="SECRET_KEY"
    export DJANGO_DEBUG=True
  ```

4. Source the environment variables
   ```sh
   (venv)$ source env.sh
   ```
5. Create database
    ```sh
      (venv)$  chmod +x local_setup.sh
      (venv)$  sh local_setup.sh
   ```
6. Run the applicatiom
   ```sh
   (venv)$ python manage.py runserver --noreload
   ```


#### Running tests coverage
 ```sh
  (venv)$ tox -r
 ```

###### Crafted with ❤️ by Macharia Kariuki