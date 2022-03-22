import requests
import time
from redis import Redis
import asyncio
import docker
# import numpy
import math

redis = Redis(host='localhost', port=6379)

swarm_master_ip = 'localhost'

# parameters for auto scaling algorithm
upper_threshold = 1
lower_threshold = 5
monitoring_interval = 10
req_per_container = 3

def auto_scale(service):
    # while True:
    start_monitoring_time = time.time()
    response_times = []
    prev_hits = int(redis.get('hits').decode())
    while(time.time() - start_monitoring_time < monitoring_interval):
        try:
            request = requests.get('http://' + swarm_master_ip + ':8000/')
            response_time = request.elapsed.total_seconds()
            response_times.append(response_time)
        except Exception as e:
            print(e)
            break
    curr_hits = int(redis.get('hits').decode())

    if len(response_times) > 0:
        average_response_time = sum(response_times) / len(response_times)
        num_req = curr_hits - prev_hits
        print("number of requests: " + str(num_req))
        
        if average_response_time > upper_threshold or average_response_time < lower_threshold:
            num_containers = math.ceil(num_req / req_per_container)
            service.scale(num_containers)

print(docker.from_env().services.list())
service = next(service for service in docker.from_env().services.list() if service.name == 'auto-scaler')
auto_scale(service)