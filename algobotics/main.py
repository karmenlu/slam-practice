#!/usr/bin/python3

import sensors
import pygame
import math
from env import Colors, BuildEnv

EXTERNAL_MAP = "floor_plans/floor_plan_2.png"
MAP_DIMENSIONS = (600, 1200)
MAP_WINDOW_NAME = "RRT Path Planning"
environment = BuildEnv(EXTERNAL_MAP, MAP_DIMENSIONS, MAP_WINDOW_NAME)
environment.original_map = environment.map.copy()
laser=sensors.LaserSensor(200, 100, environment.original_map, (0.5,0.01))
environment.map.fill(Colors.BLACK.value)
environment.infomap = environment.map.copy()

running=True

while running:
    sensor_on=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        if pygame.mouse.get_focused():
            sensor_on=True
        elif not pygame.mouse.get_focused():
            sensor_on=False
    if sensor_on:
        position=pygame.mouse.get_pos()
        laser.s_pos=position
        sensor_data=laser.sense_obstacles()
        environment.data_storage(sensor_data)
        environment.show_sensor_data()
    environment.map.blit(environment.infomap, (0,0))
    pygame.display.update()
