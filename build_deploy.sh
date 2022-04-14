sudo docker build -t mrboisvert/auto-scaler:latest docker-images/auto-scale-app
sudo docker push mrboisvert/auto-scaler:latest
sudo docker build -t mrboisvert/auto-scaler-plots:latest docker-images/graphs
sudo docker push mrboisvert/auto-scaler-plots:latest
sudo docker stack deploy --compose-file docker-compose.yml app_name