import pygame
import math
import numpy as np

class Utils:
    def distance(a_pos, b_pos):
        """
        Formula for Euclidean distance:
        distance = sqrt((xb -xa)^2 + (yb-ya)^2)
        """
        px = (b_pos[0]-a_pos[0])**2
        py = (b_pos[1]-a_pos[1])**2
        return math.sqrt(px+py)

    def uncertainty_add(distance, angle, sigma):
        """
        Used to add noise to sensor.
        """
        # Arrange data in numpy array
        mean = np.array([distance, angle])
        # Use sigma to create covariance matrix
        covariance = np.diag(sigma ** 2)
        distance, angle = np.random.multivariate_normal(mean, covariance)
        distance = max(distance, 0)
        angle = max(angle, 0)

        # Returns distance from robot and angle with which it was formed.
        return [distance, angle]

class LaserSensor:
    def __init__(self, s_range, s_speed, s_map, s_uncertainty):
        self.s_range = s_range
        self.s_speed = s_speed # rounds per sec
        self.s_sigma = np.array([s_uncertainty[0], s_uncertainty[1]])
        self.s_pos=(0,0)
        self.s_map = s_map
        self.s_w, self.s_h = pygame.display.get_surface().get_size()
        self.sensed_obstacles=[]

    def sense_obstacles(self):
        data=[]
        x1, y1 = self.s_pos[0], self.s_pos[1]
        # Iterate over angles between 0, 2pi
        for angle in np.linspace(0, 2*math.pi, 60, False):
            x2, y2 = (x1 + self.s_range * math.cos(angle), y1 + self.s_range * math.sin(angle))
            # Sampling loop
            for i in range(0, 100):
                u = i / 100
                x3 = int(x2 * u + x1 * (1 - u))
                y3 = int(y2 * u + y1 * (1 - u))
                if 0<x3<self.s_w and 0<y3<self.s_h:
                    color=self.s_map.get_at((x3, y3))
                    if (color[0], color[1], color[2]) == (0, 0, 0):
                        distance = Utils.distance((x1,y1), (x3,y3))
                        output = Utils.uncertainty_add(distance, angle, self.s_sigma)
                        output.append(self.s_pos)
                        data.append(output)
                        break
        if len(data)>0:
            return data
        else:
            return ((False,))

