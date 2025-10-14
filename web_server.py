#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web服务器模块 - 提供游戏控制接口
@author: @Suroy
@site: https://suroy.cn/
@email: suroy@qq.com
@time: 2025/10/14
"""
import socket
import re


class WebServer:
    def __init__(self, game_instance, port=80):
        self.game = game_instance
        self.port = port
        self.addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
        self.server = socket.socket()
        self.server.bind(self.addr)
        self.server.listen(1)
        self.running = False
        
        # Web控制命令队列
        self.web_commands = []
        
    def start(self):
        """启动Web服务器"""
        self.running = True
        print(f"Web服务器已启动，端口: {self.port}")
        
    def stop(self):
        """停止Web服务器"""
        self.running = False
        self.server.close()
        
    def handle_request(self, client):
        """处理HTTP请求"""
        try:
            request = client.recv(1024).decode('utf-8')
            request = request.split('\n')[0]
            
            # 解析请求路径
            match = re.match(r'GET /(\w*)', request)
            if match:
                path = match.group(1)
                
                if path == 'left':
                    self.web_commands.append('left')
                    response = self.create_json_response({"status": "success", "action": "left"})
                elif path == 'right':
                    self.web_commands.append('right')
                    response = self.create_json_response({"status": "success", "action": "right"})
                elif path == 'restart':
                    self.game.reset_game()
                    response = self.create_json_response({"status": "success", "action": "restart"})
                elif path == 'status':
                    status = {
                        "score": self.game.score,
                        "game_over": self.game.game_over,
                        "player_x": self.game.PLAYER_X,
                        "temp": self.game.dht.temp,
                        "humi": self.game.dht.humi
                    }
                    response = self.create_json_response(status)
                else:
                    response = self.create_html_page()
            else:
                response = self.create_html_page()
                
            client.send('HTTP/1.1 200 OK\n')
            client.send('Content-Type: text/html\n')
            client.send('Connection: close\n\n')
            client.sendall(response)
            
        except Exception as e:
            print(f"处理请求错误: {e}")
        finally:
            client.close()
            
    def create_json_response(self, data):
        """创建JSON响应"""
        if isinstance(data, dict):
            result = "{"
            for i, (key, value) in enumerate(data.items()):
                if i > 0:
                    result += ","
                result += f'"{key}":"{value}"'
            result += "}"
            return result
        else:
            return f'"{data}"'
        
    def create_html_page(self):
        """创建HTML控制页面"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>ESP32方块躲避游戏</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 10px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .container {
            max-width: 800px;
            width: 95%;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        h1 { color: #fff; }
        .controls {
            margin: 20px 0;
        }
        button {
            width: 100px;
            height: 100px;
            margin: 15px;
            font-size: 28px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        button:hover {
            background: #45a049;
            transform: scale(1.1);
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        }
        button:active {
            transform: scale(0.95);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        @media (max-width: 768px) {
            button {
                width: 80px;
                height: 80px;
                margin: 10px;
                font-size: 24px;
            }
        }

        @media (max-width: 480px) {
            button {
                width: 70px;
                height: 70px;
                margin: 8px;
                font-size: 20px;
            }
        }
        .status {
            margin: 20px 0;
            padding: 10px;
            background: rgba(255,255,255,0.2);
            border-radius: 5px;
        }
        .restart-btn {
            background: #f44336;
            width: 120px;
            height: 40px;
            border-radius: 20px;
            align-self: center;
        }
        .restart-btn:hover {
            background: #da190b;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 方块躲避游戏</h1>

        <div class="status" id="status">
            <p>分数: <span id="score">0</span></p>
            <p>温度: <span id="temp">--</span>°C</p>
            <p>湿度: <span id="humi">--</span>%</p>
        </div>

        <div class="controls">
            <button onclick="move('left')">⬅️</button>
            <button onclick="move('right')">➡️</button>
        </div>

        <button class="restart-btn" onclick="restart()">🔄 重玩</button>
    </div>

    <footer style="margin-top: 5px; padding: 10px; font-size: 12px; color: rgba(255,255,255,0.7); text-align: center;">
        <p>© 2025 <a href="https://suroy.cn" style="color: rgba(255,255,255,0.9); text-decoration: none;">SUROY</a> | Powered by ESP32 & MicroPython</p>
    </footer>

    <script>
        function move(direction) {
            fetch('/' + direction)
                .then(response => response.json())
                .then(data => console.log('移动:', data));
        }

        function restart() {
            fetch('/restart')
                .then(response => response.json())
                .then(data => {
                    console.log('重启:', data);
                    updateStatus();
                });
        }

        function updateStatus() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('score').textContent = data.score;
                    document.getElementById('temp').textContent = data.temp;
                    document.getElementById('humi').textContent = data.humi;
                });
        }

        // 每秒更新状态
        setInterval(updateStatus, 1000);

        // 页面加载时更新状态
        updateStatus();
    </script>
</body>
</html>
        """
        return html
        
    def get_web_commands(self):
        """获取Web控制命令"""
        commands = self.web_commands.copy()
        self.web_commands.clear()
        return commands
        
    def process_requests(self):
        """处理Web请求（非阻塞）"""
        try:
            # 设置非阻塞模式
            self.server.setblocking(False)
            client, addr = self.server.accept()
            print(f"客户端连接: {addr}")
            self.handle_request(client)
        except:
            # 没有连接请求，继续执行
            pass