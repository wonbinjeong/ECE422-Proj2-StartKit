import requests
from time import time, sleep
from redis import Redis
import asyncio
import docker
# import numpy
import math
import os
import websockets
import socket
import json
import subprocess

redis = Redis(host='redis', port=6379)
swarm_master_ip = '10.2.12.208'

# parameters for auto scaling algorithm
upper_threshold = 1
lower_threshold = 5
monitoring_interval = 10
req_per_container = 3

# arrays for plotting
workload_plot = []
response_time_plot = []
num_replicas_plot = []
time_plot = []

num_containers = 1
average_response_time = 0

def get_web_service():
    web_service = None
    for service in docker.from_env().services.list():
        print(service.name)
        if service.name == 'auto_scale_web':
            web_service = service
    return web_service

async def auto_scale(websocket, path):
    # get the web service
    '''web_service = get_web_service()
    web_service.scale(5)
    sleep(5)
    web_service = get_web_service()
    web_service.scale(6)
    sleep(5)
    web_service = get_web_service()
    web_service.scale(5)
    sleep(5)
    web_service = get_web_service()
    web_service.scale(4)
    sleep(5)
    web_service = get_web_service()
    web_service.scale(8)'''
    '''client = docker.APIClient(base_url="unix:/var/run/docker.sock")
    print(client.version)
    replica_mode = docker.types.ServiceMode('replicated', replicas=5)
    web_service = None
    for service in docker.from_env().services.list():
        print(service.name)
        if service.name == 'app_name_web':
            web_service = service
    svc_version = client.inspect_service(web_service.id)['Version']['Index']
    client.update_service(web_service.id, svc_version, mode=replica_mode)

    replica_mode = docker.types.ServiceMode('replicated', replicas=6)
    client.update_service(web_service.id, svc_version, mode=replica_mode)
    start_time = time()'''
    start_time = time()
    # start auto scaler
    while True:
        # monitor response time
        start_monitoring_time = time()
        response_times = []
        prev_hits = int(redis.get('hits').decode())
        while(time() - start_monitoring_time < monitoring_interval):
            try:
                request = requests.get('http://' + swarm_master_ip + ':8000/')
                response_time = request.elapsed.total_seconds()
                response_times.append(response_time)
            except Exception as e:
                print("Requests exception")
                print(e)
                print("breaking...")
                continue
        curr_hits = int(redis.get('hits').decode())

        requests_per_sec = (curr_hits - prev_hits) / monitoring_interval
        workload_plot.append(requests_per_sec)
        
        # scale web service if needed
        if len(response_times) > 0:
            average_response_time = sum(response_times) / len(response_times)
            num_req = curr_hits - prev_hits
            print("number of requests: " + str(num_req))
            
            if average_response_time > upper_threshold or average_response_time < lower_threshold:
                num_containers = math.ceil(num_req / req_per_container)
                print(f"scaling to {num_containers} containers")
                try:
                    web_service = get_web_service()
                    result = web_service.scale(num_containers)                    
                    print("scaled", result)
                except Exception as e:
                    print("exception while scaling")
                    print(e)
        
        # update plots
        response_time_plot.append(average_response_time)
        num_replicas_plot.append(num_containers)
        current_time = time() - start_time
        print(current_time)
        time_plot.append(current_time)
        data = {
            "workload": {"x": time_plot, "y": workload_plot},
            "response_time": {"x": time_plot, "y": response_time_plot},
            "application_size": {"x": time_plot, "y": num_replicas_plot}
        }
        try:
            await websocket.send(json.dumps(data))
        except Exception as e:
            print("socket error")
            print(e)

'''print("starting...")
start_server = websockets.serve(auto_scale, '0.0.0.0', 7000)
print("socket open")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()'''

async def main():
    async with websockets.serve(auto_scale, '0.0.0.0', 7000):
        await asyncio.Future()  # run forever

asyncio.run(main())