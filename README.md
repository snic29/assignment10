# Module 10

This FastAPI project includes a SQLAlchemy user model with unique usernames and
emails, bcrypt password hashing, Pydantic user schemas, and a calculator API.

## Run Locally

Start PostgreSQL. With the provided Compose service, the default database is
`fastapi_db` at `localhost:5432`, so you do not need to set `DATABASE_URL` to
run `pytest`. The test fixtures drop and recreate tables in the configured
database; only use a disposable database, not one containing data you need.

```bash
# Use Python 3.11 or newer
docker compose up -d db
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install --with-deps chromium
pytest
```

To isolate tests in a separate database instead of the default, create it
once and set `DATABASE_URL` for the test command:

```bash
docker compose exec db createdb -U postgres assignment10_test
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/assignment10_test pytest
```

The test suite includes unit, PostgreSQL integration, and Playwright end-to-end
tests. To run the application directly, use `python3 main.py`; it
serves the calculator at `http://localhost:8000` and reports container health
at `/health`.

## Docker Hub

The published image is [https://hub.docker.com/r/stelni/assignment10](https://hub.docker.com/r/stelni/assignment10).
Pull and run it with:

```bash
docker pull stelni/assignment10:latest
docker run --rm -p 8000:8000 stelni/assignment10:latest
```

See [REFLECTION.md](./REFLECTION.md) for my development and deployment reflection.
