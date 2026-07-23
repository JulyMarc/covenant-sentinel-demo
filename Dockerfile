FROM python:3.11-slim

WORKDIR /app
COPY . /app

CMD ["python", "covenant_sentinel.py", "report", "--out", "reports/demo_report.md"]
