import numpy as np
import math
import cv2
from collections import deque


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.queue = deque([])
        self.score = 0
        self.turn = 0
        self.end = False
        self.last_eat = 0
        self.matrix = np.zeros((self.x, self.y), dtype=int)
        rand_x = np.random.randint(low=0, high=x)
        rand_y = np.random.randint(low=0, high=y)
        self.food_x = rand_x
        self.food_y = rand_y
        # 1 = food = 127
        # 2 = snake = 255
        self.matrix[rand_x][rand_y] = 127
        stop = False

        while not stop:
            rand_x = np.random.randint(low=1, high=(x-1))
            rand_y = np.random.randint(low=1, high=(y-1))
            stop = True
            for i in range(0, 4):
                if rand_x + i >= self.x or self.matrix[rand_x + i][rand_y] != 0:
                    stop = False
                    break

        for i in range(0, 4):
            self.matrix[rand_x + i][rand_y] = 255
            self.queue.appendleft({"x": rand_x + i, "y": rand_y})

    def calculate_distance(self):
        front = self.queue[0]
        distance_y = front["y"] - self.food_y
        distance_x = front["x"] - self.food_x
        distance = math.sqrt(math.pow(distance_y, 2) + math.pow(distance_x, 2))
        return distance

    def next_move(self, keycode):
        old_distance = self.calculate_distance()
        move_x, move_y = None, None
        # Up
        if keycode == 40:
            move_x, move_y = 0, 1
        # Down
        if keycode == 38:
            move_x, move_y = 0, -1
        # Right
        if keycode == 39:
            move_x, move_y = 1, 0
        # Left
        if keycode == 37:
            move_x, move_y = -1, 0
        # If event.keycode is not a legal value
        if move_x is None:
            return self.generate_image(), -10, self.end
        if self.end:
            return self.generate_image(), -100, self.end
        if self.last_eat > 500:
            self.end = True
            return self.generate_image(), -100, self.end
        front = self.queue[0]
        self.turn += 1
        # snake beat on the wall
        if front["x"] + move_x < 0 or front["y"] + move_y < 0 or front["x"] + move_x >= self.x or front[
                "y"] + move_y >= self.y:
            self.end = True
            return self.generate_image(), -100, self.end

        if front["x"] + move_x == self.queue[1]["x"] and front["y"] + move_y == self.queue[1]["y"]:
            self.last_eat += 1
            return self.generate_image(), -100, self.end
        eat = (self.matrix[front["x"] + move_x]
               [front["y"] + move_y] == 127 if True else False)
        beat = (self.matrix[front["x"] + move_x]
                [front["y"] + move_y] == 255 if True else False)
        # Snake beat on himself
        if beat:
            self.end = True
            return self.generate_image(), -100, self.end
        # Snake eat
        self.matrix[front["x"] + move_x][front["y"] + move_y] = 255
        self.queue.appendleft(
            {"x": front["x"] + move_x, "y": front["y"] + move_y})
        tail = self.queue[-1]
        if not eat:
            self.queue.pop()
            self.matrix[tail["x"]][tail["y"]] = 0
            self.last_eat += 1
            new_distance = self.calculate_distance()
            if new_distance < old_distance:
                return self.generate_image(), 10, self.end
            else:
                return self.generate_image(), -10, self.end
        else:
            self.score += 1
            self.last_eat = 0
            while True:
                rand_x = np.random.randint(low=0, high=self.x)
                rand_y = np.random.randint(low=0, high=self.y)
                if self.matrix[rand_x][rand_y] == 0 or self.score > 98:
                    self.matrix[rand_x][rand_y] = 127
                    self.food_x = rand_x
                    self.food_y = rand_y
                    break
            return self.generate_image(), 100, self.end

    def generate_image(self, scale_percent=1):
        new_rgb = np.dstack(
            [self.matrix, self.matrix, self.matrix]).astype(np.uint8)
        img = cv2.cvtColor(new_rgb, cv2.COLOR_BGR2GRAY)
        width = int(img.shape[1] * scale_percent)
        height = int(img.shape[0] * scale_percent)
        dim = (width, height)

        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return resized
