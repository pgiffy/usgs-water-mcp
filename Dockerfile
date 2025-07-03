FROM python:3.12-slim

WORKDIR /app

# Copy the project files
COPY . .

# Upgrade pip and install the project in editable mode
RUN pip install --upgrade pip \
    && pip install -e .

CMD ["python", "current_water_levels.py"]