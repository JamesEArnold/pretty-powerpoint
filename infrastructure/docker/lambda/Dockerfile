FROM public.ecr.aws/lambda/python:3.11

# Install UV
RUN pip install --no-cache-dir uv

# Copy project dependency files
COPY pyproject.toml uv.lock ${LAMBDA_TASK_ROOT}/

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Install dependencies using UV (much faster than pip)
RUN uv sync --frozen --no-dev

# Copy application code
COPY src/ ${LAMBDA_TASK_ROOT}/src/

# Set handler
CMD ["src.application.handlers.main.handler"]
