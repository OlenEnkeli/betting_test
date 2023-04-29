#!/bin/bash

poetry run uvicorn --reload app.main:app --port 8001 --timeout-keep-alive 10000 --env-file .env
