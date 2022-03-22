import requests
import time
from redis import Redis
import asyncio
import docker
# import numpy
import math

redis = Redis(host='redis', port=6379)

swarm_master_ip = '0.0.0.0'

# parameters for auto scaling algorithm
upper_threshold = 1
lower_threshold = 5
monitoring_interval = 10
req_per_container = 3

def auto_scale(client):
    while True:
        start_monitoring_time = time.time()
        response_times = []
        prev_hits = redis.get('hits')
        while(time.time() - start_monitoring_time < monitoring_interval):
            try:
                request = requests.get('http://' + swarm_master_ip + ':8000/')
                response_time = request.elapsed.total_seconds()
                response_times.append(response_time)
            except:
                break
        curr_hits = redis.get('hits')

        if len(response_times) > 0:
            average_response_time = sum(response_times) / len(response_times)
            num_req = curr_hits - prev_hits
            print("number of requests: " + str(num_req))
            
            if average_response_time > upper_threshold or average_response_time < lower_threshold:
                num_containers = math.ceil(num_req / req_per_container)
                client.scale(num_containers)


client = docker.from_env()
auto_scale(client)