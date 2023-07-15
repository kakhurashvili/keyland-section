FROM python:3.8-alpine

# Install GDAL dependencies
RUN apk add --update --no-cache \
    gdal-dev \
    geos-dev \
    proj-dev \
    build-base \
    musl-dev \
    icu-data-full

# Set working directory
WORKDIR /usr/src/app

# Copy requirements.txt
COPY requirements.txt .

# Install pipenv (optional)
RUN pip install pipenv

# Create and activate a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    libc-dev \
    linux-headers \
    postgresql-dev \
    musl-dev \
    zlib-dev \
    jpeg-dev \
    libffi-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# Copy the rest of your application
COPY . .
RUN python src/manage.py collectstatic

# Set the entrypoint
ENTRYPOINT ["python"]
EXPOSE 8080

# Set the default command
CMD ["src/manage.py", "runserver", "0.0.0.0:8080"]
