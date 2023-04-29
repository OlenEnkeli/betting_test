#!/bin/bash

poetry run uvicorn --reload app.main:app --port 8000 --timeout-keep-alive 10000 --env-file .env
