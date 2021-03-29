echo "Building Docker image..."
docker build -t file-rest -f Dockerfile .

echo "Running Docker image..."
docker run -ti -p 8080:8080 file-rest

pause