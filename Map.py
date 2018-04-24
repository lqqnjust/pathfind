# coding:utf-8
import pygame
from pygame import QUIT, KEYUP, K_ESCAPE, K_s, MOUSEBUTTONDOWN, K_e, K_o, K_r, K_LCTRL,K_l, K_F1, K_F2
import sys

XDIM = 800
YDIM = 600
WINSIZE = [XDIM, YDIM]

pygame.init()
fpsClock = pygame.time.Clock()


screen = pygame.display.set_mode(WINSIZE)
pygame.display.set_caption('Rapidly Exploring Random Tree')

#字体
font1 = pygame.font.SysFont('arial', 16)


class BaseAlg:
    """
    寻路算法基类
    """
    def __init__(self, map):
        """
        初始化地图数据
        """
        self.map = map

    def process(self):
        """
        算法处理
        """
        pass

class Map:
    '''
    用于绘制地图
    '''
    def __init__(self, screen, map_size, cell_size):
        self.screen =  screen
        self.map_size = map_size
        self.cell_size = cell_size
        self.position = (0, 0)

        #是否展示格子边框
        self.showcell = True

        self.line_color = (125, 125, 125)
        self.backgroundcolor = (255, 255, 255)
        self.start_color = (0, 255, 0)
        self.end_color = (0, 0, 255)
        self.obstacle_color = (0, 0, 0)

        self.path = []
        self.start = None
        self.end = None
        self.obstacles = []

        self.filename = "map.txt"
    
    def set_position(self, position):
        self.position = position

    def draw(self):
        self.screen.fill(self.backgroundcolor)

        if self.start:
            pos = self.grid_to_screen(self.start)
            pygame.draw.rect(self.screen, self.start_color, [pos[0],pos[1],self.cell_size[0],self.cell_size[1]],0)

        if self.end:
            pos = self.grid_to_screen(self.end)
            pygame.draw.rect(self.screen, self.end_color, [pos[0], pos[1], self.cell_size[0],self.cell_size[1]], 0)

        for ob in self.obstacles:
            pos = self.grid_to_screen(ob)
            pygame.draw.rect(self.screen, self.obstacle_color, [pos[0], pos[1], self.cell_size[0],self.cell_size[1]], 0)


        if self.showcell:
            cols, rows  = self.map_size
            cell_width, cell_height = self.cell_size
            for x in range(cols):
                for y in range(rows):
                    _x = self.position[0] + x * cell_width
                    _y = self.position[1] + y * cell_height
                    pygame.draw.rect(self.screen, self.line_color, [_x, _y, cell_width, cell_height], 1)
        else:
            top = self.position
            width = self.map_size[0] * self.cell_size
            height = self.map_size[1] * self.cell_size
            pygame.draw.rect(self.screen, self.line_color, [top[0], top[1], width, height], 1)
    def save(self):
        with open(self.filename,"w") as f:
            f.write("{},{}\n".format(self.start[0],self.start[1]))
            f.write("{},{}\n".format(self.end[0],self.end[1]))
            for ob in self.obstacles:
                f.write("{},{}\n".format(ob[0],ob[1]))

    def load(self):
        with open(self.filename,"r") as f:
            lines = f.readlines()
            start_line = lines[0]
            items = start_line.strip().split(",")
            self.start = int(items[0]),int(items[1])

            end_line = lines[1]
            items = end_line.strip().split(",")
            self.end = int(items[0]),int(items[1])

            self.obstacles=[]
            for line in lines[2:]:
                line = line.strip()
                if line!="":
                    items = line.split(",")
                    self.obstacles.append((int(items[0]),int(items[1])))

    def screen_to_grid(self, position):
        """
        将屏幕坐标转换成地图坐标
        :param position:
        :return:
        """

        _x = (position[0] - self.position[0])//self.cell_size[0]
        _y = (position[1] - self.position[1])//self.cell_size[1]
        return _x,_y

    def grid_to_screen(self, position):
        """
        将地图坐标系转成屏幕坐标系
        :param position:
        :return:
        """
        _x = position[0] * self.cell_size[0] +self.position[0]
        _y = position[1] * self.cell_size[1] + self.position[1]
        return _x, _y

def main():

    map = Map(screen,(40,30),(16,16))
    state = 0
    loop = True
    while loop:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                print("exit ")
                loop = False
            elif  e.type == KEYUP :
                if e.key == K_s:
                    print("设置起点")
                    # 设置开始
                    state = 1
                elif e.key == K_e:
                    print("设置终点")
                    state = 2
                elif e.key == K_o:
                    print("设置障碍物")
                    state = 3
                elif e.key == K_r:
                    print("key up r, 开始路径搜寻")
                    state = 4
                elif e.key == K_F1:
                    print("保存地图")
                    map.save()
                elif e.key == K_F2:
                    print("加载地图")
                    map.load()
            #鼠标事件
            if e.type == MOUSEBUTTONDOWN:
                if state == 1:
                    mx, my = pygame.mouse.get_pos()
                    gx,gy = map.screen_to_grid((mx,my))
                    map.start = (gx,gy)
                elif state == 2:
                    mx, my = pygame.mouse.get_pos()
                    gx, gy = map.screen_to_grid((mx, my))
                    map.end = (gx, gy)
                elif state == 3:
                    mx, my = pygame.mouse.get_pos()
                    gx, gy = map.screen_to_grid((mx, my))
                    map.obstacles.append((gx, gy))

        map.draw()

        pygame.display.flip()
        fpsClock.tick(60)


if __name__ == "__main__":
    main()

    