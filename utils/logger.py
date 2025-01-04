"""
日志模块
作者：来碗麻辣烫
创建日期：2024-03-21
"""

import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, log_dir='logs'):
        # 创建日志目录
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # 生成日志文件名（使用当前日期）
        log_file = os.path.join(log_dir, f'spider_{datetime.now().strftime("%Y%m%d")}.log')
        
        # 创建logger实例
        self.logger = logging.getLogger('RedBookSpider')
        self.logger.setLevel(logging.INFO)
        
        # 清除可能存在的之前的处理器
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建文件处理器，设置 mode='w' 来覆盖文件
        file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 设置日志格式
        log_format = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler.setFormatter(log_format)
        file_handler.setFormatter(log_format)
        
        # 添加处理器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def info(self, message):
        """记录信息级别的日志"""
        self.logger.info(message)
    
    def error(self, message):
        """记录错误级别的日志"""
        self.logger.error(message)
    
    def warning(self, message):
        """记录警告级别的日志"""
        self.logger.warning(message) 