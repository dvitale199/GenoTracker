FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

COPY . /app

EXPOSE 8080

CMD ["streamlit", "run", "genotracker/frontend/streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]


# use this for local testing only
# COPY scripts/wait-for-it.sh /usr/local/bin/wait-for-it.sh
# RUN chmod +x /usr/local/bin/wait-for-it.sh
# ENV GOOGLE_APPLICATION_CREDENTIALS=/run/secrets/gcloud-service-account
# CMD wait-for-it.sh genotracker-fastapi-3wsqie35cq-uc.a.run.app -- streamlit run genotracker/frontend/streamlit_app.py --server.port=8501 --server.address=0.0.0.0