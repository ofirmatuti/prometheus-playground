docker stop flask
docker rm flask

docker build -t flask flask_app

docker run --name flask --network="prometheus_default" -d -p 5000:5000 flask
