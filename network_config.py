#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
网络配置模块 - ESP32 AP模式配置
@author: @Suroy
@site: https://suroy.cn/
@email: suroy@qq.com
@time: 2025/10/14
"""

import network
import time

class NetworkConfig:
    def __init__(self, ssid="SUROY_AP", password="88888888"):
        self.ssid = ssid
        self.password = password
        self.ap = network.WLAN(network.AP_IF)
        
    def setup_ap(self):
        """设置ESP32为AP模式"""
        self.ap.active(True)
        self.ap.config(essid=self.ssid, password=self.password)
        
        print(f"AP模式已启动")
        print(f"SSID: {self.ssid}")
        print(f"Password: {self.password}")
        print(f"IP地址: {self.ap.ifconfig()[0]}")
        
        return self.ap.ifconfig()[0]
    
    def get_status(self):
        """获取网络状态"""
        if self.ap.active():
            return {
                "active": True,
                "ssid": self.ssid,
                "ip": self.ap.ifconfig()[0],
                "connected_stations": self.ap.status()['stations']
            }
        else:
            return {"active": False}