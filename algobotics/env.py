import math
import pygame
from enum import Enum

class Colors(Enum):
    BLACK = (0, 0, 0)
    GRAY = (70, 70, 70)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

class BuildEnv():
    def __init__(self, external_map, map_dimensions, map_window_name):
        pygame.init()
        self.point_cloud=[]
        self.external_map=pygame.image.load(external_map)
        self.map_h, self.map_w = map_dimensions
        self.map_window_name = map_window_name
        pygame.display.set_caption(self.map_window_name)
        self.map = pygame.display.set_mode((self.map_w, self.map_h))
        self.map.blit(self.external_map, (0,0))

    def ad2pos(self, distance, angle, pos):
        """
        Given an angle and distance from a position,
        computes the point.
        """
        x = distance * math.cos(angle)+pos[0]
        y = distance * math.sin(angle)+pos[1]
        return (int(x), int(y))

    def data_storage(self, data):
        print(len(self.point_cloud))
        for element in data:
            print("debug element:", element)
            if element and len(element) == 3:
                point = self.ad2pos(element[0], element[1], element[2])
                if point not in self.point_cloud:
                    self.point_cloud.append(point)

    def show_sensor_data(self):
        """
        Draws data on a new copy of map.
        """
        #self.infomap=self.map.copy()
        for point in self.point_cloud:
            self.infomap.set_at((int(point[0]), int(point[1])), Colors.RED.value)


        
