#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: @Suroy
@site: https://suroy.cn/
@email: suroy@qq.com
@time: 2025/5/13 11:23 PM
"""
import dht
import time
import random
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from network_config import NetworkConfig
from web_server import WebServer


class DHTSensor:

    def __init__(self):
        self.dht_sensor = dht.DHT11(Pin(26))  # DHT11
        self.temp = 0
        self.humi = 0
        self.last_spawn_time = time.ticks_ms()
        self.SPAWN_RATE = 30
        self._read()

    def read_dht11(self):
        """读取DHT11温湿度数据"""
        if time.ticks_diff(time.ticks_ms(), self.last_spawn_time) >= self.SPAWN_RATE * 1000:
            self._read()
        return self.temp, self.humi

    def _read(self):
        self.dht_sensor.measure()
        self.temp = self.dht_sensor.temperature()
        self.humi = self.dht_sensor.humidity()
        self.last_spawn_time = time.ticks_ms()


class Game:
    
    def __init__(self):
        # OLED
        self.WIDTH = 128
        self.HEIGHT = 64
        self.i2c = I2C(0, scl=Pin(10), sda=Pin(9))
        self.oled = SSD1306_I2C(self.WIDTH, self.HEIGHT, self.i2c)
        self.dht = DHTSensor()

        # 按键配置
        self.BUTTON_RIGHT_PIN = 28
        self.BUTTON_LEFT_PIN = 27
        self.button_right = Pin(self.BUTTON_RIGHT_PIN, Pin.IN, Pin.PULL_UP)
        self.button_left = Pin(self.BUTTON_LEFT_PIN, Pin.IN, Pin.PULL_UP)

        # 游戏参数
        self.PLAYER_SIZE = 8
        self.PLAYER_X = 0
        self.PLAYER_Y = self.HEIGHT - self.PLAYER_SIZE - 1
        self.BLOCK_SIZE = 8
        self.BLOCK_SPEED = 1
        self.SPAWN_RATE = 1.5  # 每隔多少秒生成一个新方块

        self.blocks = []
        self.score = 0
        self.game_over = False
        self.gen_block = True
        self.last_spawn_time = 0
        
        self.ENABLE_DEBUG = False
        
        # Web控制相关
        self.web_server = None
        self.last_web_check = 0
        self.WEB_CHECK_INTERVAL = 100  # 每100ms检查一次Web请求

        self.reset_game()
        
        # 初始化网络和Web服务器
        self.setup_network()
    
    def debug_log(self, log):
        if self.ENABLE_DEBUG:
            print(log)

    def setup_network(self):
        """设置网络和Web服务器"""
        try:
            # 设置AP模式
            network = NetworkConfig()
            ip = network.setup_ap()
            
            # 启动Web服务器
            self.web_server = WebServer(self)
            self.web_server.start()
            
            # 在OLED上显示IP地址
            self.oled.fill(0)
            self.oled.text("WiFi Started!", 0, 0, 1)
            self.oled.text("IP:", 0, 16, 1)
            self.oled.text(ip[:], 0, 24, 1)
            self.oled.text("Ready!", 0, 48, 1)
            self.oled.show()
            time.sleep(3)
            
            self.debug_log(f"网络设置完成，IP: {ip}")
        except Exception as e:
            self.debug_log(f"网络设置失败: {e}")
            
    def reset_game(self):
        self.PLAYER_X = self.WIDTH // 2 - self.PLAYER_SIZE // 2
        self.blocks = []
        self.score = 0
        self.game_over = False
        self.gen_block = True
        self.last_spawn_time = time.ticks_ms()
        self.debug_log("游戏重置！")

    def draw_player(self):
        self.oled.framebuf.fill_rect(self.PLAYER_X, self.PLAYER_Y, self.PLAYER_SIZE, self.PLAYER_SIZE, 1)

    def draw_block(self, x, y):
        # 尝试将 y 限制在屏幕范围内进行绘制，观察是否能看到
        draw_y = min(y, self.HEIGHT - self.BLOCK_SIZE)
        self.oled.framebuf.fill_rect(x, draw_y, self.BLOCK_SIZE, self.BLOCK_SIZE, 1)

    def check_collision(self, block_x, block_y):
        return (self.PLAYER_X < block_x + self.BLOCK_SIZE and
                self.PLAYER_X + self.PLAYER_SIZE > block_x and
                self.PLAYER_Y < block_y + self.BLOCK_SIZE and
                self.PLAYER_Y + self.PLAYER_SIZE > block_y)

    def display_score(self):
        self.oled.text("[{}]".format(self.score), 0, 0, 1)

        temp, humi = self.dht.read_dht11()
        self.oled.text("T:{} H:{}".format(temp, humi), 50, 0, 1)

    def display_game_over(self):
        self.oled.fill(0)
        self.oled.text("SUROY PROJECT", 10, 0, 1)
        self.oled.text("Game Over!", self.WIDTH // 2 - 40, self.HEIGHT // 2 - 10, 1)
        self.oled.text("Score: {}".format(self.score), self.WIDTH // 2 - 35, self.HEIGHT // 2 + 5, 1)
        self.oled.show()

    def handle_input(self):
        # 处理Web控制命令
        self.handle_web_input()
        
        # 读取按键状态 - 向右移动
        if self.button_right.value() == 0:  # 按键按下 (低电平)
            self.PLAYER_X = min(self.WIDTH - self.PLAYER_SIZE, self.PLAYER_X + self.PLAYER_SIZE // 2)
            while self.button_right.value() == 0:  # 等待按键释放
                time.sleep_ms(10)

        # 读取按键状态 - 向左移动
        if self.button_left.value() == 0:  # 按键按下 (低电平)
            self.PLAYER_X = max(0, self.PLAYER_X - self.PLAYER_SIZE // 2)
            while self.button_left.value() == 0:  # 等待按键释放
                time.sleep_ms(10)
                
    def handle_web_input(self):
        """处理Web控制输入"""
        if self.web_server and time.ticks_diff(time.ticks_ms(), self.last_web_check) >= self.WEB_CHECK_INTERVAL:
            # 处理Web请求
            self.web_server.process_requests()
            
            # 获取Web控制命令
            commands = self.web_server.get_web_commands()
            for command in commands:
                if command == 'left':
                    self.PLAYER_X = max(0, self.PLAYER_X - self.PLAYER_SIZE // 2)
                    self.debug_log("Web控制: 左移")
                elif command == 'right':
                    self.PLAYER_X = min(self.WIDTH - self.PLAYER_SIZE, self.PLAYER_X + self.PLAYER_SIZE // 2)
                    self.debug_log("Web控制: 右移")
                    
            self.last_web_check = time.ticks_ms()

    def spawn_blocks(self):
        if time.ticks_diff(time.ticks_ms(), self.last_spawn_time) >= self.SPAWN_RATE * 1000 and self.gen_block:
            block_x = random.randint(0, self.WIDTH - self.BLOCK_SIZE)
            self.blocks.append([block_x, 0])
            self.last_spawn_time = time.ticks_ms()
            self.gen_block = False
            self.debug_log(f"生成新方块：x={block_x}, y=0，当前方块数量：{len(self.blocks)}")

    def update_blocks(self):
        updated_blocks = []
        for block in self.blocks:
            block_x, block_y = block
            block_y += self.BLOCK_SPEED
            self.debug_log(f"更新方块：x={block_x}, y={block_y}")
            if block_y < self.HEIGHT:
                updated_blocks.append([block_x, block_y])
            elif block_y >= self.HEIGHT:
                self.gen_block = True
                self.score += 1
                self.debug_log(f"方块已到底部，得分增加：{self.score}")
        self.blocks = updated_blocks
        self.debug_log(f"更新后方块数量：{len(self.blocks)}")

    def check_collisions(self):
        for block in self.blocks:
            block_x, block_y = block
            if self.check_collision(block_x, block_y):
                self.debug_log("发生碰撞！游戏结束")
                self.game_over = True
                break

    def draw_screen(self):
        self.oled.fill(0)
        self.draw_player()
        for block in self.blocks:
            block_x, block_y = block
            self.draw_block(block_x, block_y)
        self.display_score()
        self.oled.show()

    def run(self):
        while True:
            if not self.game_over:
                self.handle_input()
                self.spawn_blocks()
                self.update_blocks()
                self.check_collisions()
                self.draw_screen()
                time.sleep_ms(50)
            else:
                self.display_game_over()
                time.sleep(2)
                self.reset_game()


if __name__ == "__main__":
    game = Game()
    game.run()
