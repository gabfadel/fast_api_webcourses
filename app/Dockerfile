FROM python:3.10 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.10 AS runtime
WORKDIR /app
ENV PATH="/root/.local/bin:${PATH}"
COPY --from=builder /root/.local/ /root/.local/
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]