**Steps to run:**

1/ poetry install\
2/ poetry shell\
3/ Build Postgres database:
- cd db_compose
- docker compose up -d
- cd ..
- alembic upgrade head

4/ uvicorn app.main:app --host 0.0.0.0 --port 8000  --reload
