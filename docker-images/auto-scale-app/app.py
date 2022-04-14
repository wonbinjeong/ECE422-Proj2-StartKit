import requests
import time
from redis import Redis
import asyncio
import docker
# import numpy
import math
import os
import websockets
import socket
import json

redis = Redis(host='redis', port=6379)
swarm_master_ip = '10.2.12.208'
ENABLED = os.getenv('ENABLED')

# parameters for auto scaling algorithm
upper_threshold = 1
lower_threshold = 5
monitoring_interval = 10
req_per_container = 3

# arrays for plotting
workload = []
response_time = []
num_replicas = []
time = []

num_containers = 1
average_response_time = 0

async def auto_scale(websocket, path):
    # get the web service
    web_service = None
    for service in docker.from_env().services.list():
        print(service.name)
        if service.name == 'app_name_web':
            web_service = service
    start_time = time.time()
    # start auto scaler
    while True:
        if ENABLED == 1:
            # monitor response time
            start_monitoring_time = time.time()
            response_times = []
            prev_hits = int(redis.get('hits').decode())
            while(time.time() - start_monitoring_time < monitoring_interval):
                try:
                    request = requests.get('http://' + swarm_master_ip + ':8000/')
                    response_time = request.elapsed.total_seconds()
                    response_times.append(response_time)
                except Exception as e:
                    print("Requests exception")
                    print(e)
                    print("breaking...")
                    break
            curr_hits = int(redis.get('hits').decode())

            requests_per_sec = (curr_hits - prev_hits) / monitoring_interval
            workload.append(requests_per_sec)
            
            # scale web service if needed
            if len(response_times) > 0:
                average_response_time = sum(response_times) / len(response_times)
                num_req = curr_hits - prev_hits
                print("number of requests: " + str(num_req))
                
                if average_response_time > upper_threshold or average_response_time < lower_threshold:
                    num_containers = math.ceil(num_req / req_per_container)
                    print(f"scaling to {num_containers} containers")
                    web_service.scale(num_containers)
                    print("scaled")
            
            # update plots
            response_time.append(average_response_time)
            num_replicas.append(num_containers)
            time.append(time.time() - start_time)
            data = {
                "workload": {"x": time, "y": workload},
                "response_time": {"x": time, "y": response_time},
                "application_size": {"x": time, "y": num_replicas}
            }
            websocket.send(json.dumps(data))
        else:
            print("auto scaler disabled")

'''async def main():
    print("starting websocket...")
    async with websockets.serve(auto_scale, "0.0.0.0", 3000):
        await asyncio.Future()

print("test")
asyncio.run(main())'''

print("starting...")
start_server = websockets.serve(auto_scale, '0.0.0.0', 3000)
print("socket open")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()