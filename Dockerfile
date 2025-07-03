FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY *.py ./

# Install dependencies
RUN uv sync --frozen

# Expose port
EXPOSE 8000

# Run the server
CMD ["python", "server.py"]