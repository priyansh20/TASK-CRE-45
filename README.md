# TASK-CRE-45
# Build the Docker image
docker build -t task-cre-45-etl .

# Run the container, passing the database URI via environment variable
docker run -e DB_URI="postgresql://your_user:your_password@host.docker.internal:5432/your_db" task-cre-45-etl
