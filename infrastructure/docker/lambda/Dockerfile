FROM public.ecr.aws/lambda/python:3.11

# Copy requirements file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY src/ ${LAMBDA_TASK_ROOT}/src/

# Set handler
CMD ["src.application.handlers.main.handler"]
