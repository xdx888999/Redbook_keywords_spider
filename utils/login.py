"""
登录处理模块
作者：来碗麻辣烫
创建日期：2024-03-21

功能说明：
    处理小红书的登录功能，支持Cookie登录和手动登录。

主要类：
    LoginHandler：登录处理的核心类
"""

import json
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class XHSLogin:
    def __init__(self, driver_path, cookies_path, logger):
        self.driver_path = driver_path
        self.cookies_path = cookies_path
        self.driver = None
        self.logger = logger

    def random_sleep(self, min_seconds=2, max_seconds=5):
        """随机延时函数"""
        sleep_time = random.uniform(min_seconds, max_seconds)
        self.logger.info(f'随机延时 {sleep_time:.2f} 秒')
        time.sleep(sleep_time)

    def init_driver(self):
        """初始化Chrome浏览器"""
        self.logger.info('初始化Chrome浏览器')
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        # 添加其他必要的选项
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 使用指定的 ChromeDriver
        service = Service(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 修改 window.navigator.webdriver 标记
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })

    def manual_login(self):
        """手动登录流程"""
        self.logger.info('开始手动登录流程')
        self.driver.get('https://www.xiaohongshu.com')
        self.random_sleep()
        
        while True:
            user_input = input('请完成手动登录后输入 y 继续，输入 n 退出程序: ')
            if user_input.lower() == 'y':
                self.random_sleep()
                self.save_cookies()
                self.logger.info('手动登录成功')
                return True
            elif user_input.lower() == 'n':
                self.logger.info('用户选择退出程序')
                self.quit()
                return False
            else:
                self.logger.warning('输入无效，请重新输入')

    def save_cookies(self):
        """保存登录cookies"""
        self.logger.info('开始保存Cookies')
        self.random_sleep()
        cookies = self.driver.get_cookies()
        with open(self.cookies_path, 'w', encoding='utf-8') as f:
            json.dump(cookies, f)
        self.logger.info('Cookies保存成功')

    def load_cookies(self):
        """加载已保存的cookies"""
        if os.path.exists(self.cookies_path):
            self.logger.info('开始加载Cookies')
            self.driver.get('https://www.xiaohongshu.com')
            self.random_sleep()  # 访问网站后的随机延时
            
            with open(self.cookies_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            try:
                for cookie in cookies:
                    if 'expiry' in cookie:
                        del cookie['expiry']
                    self.driver.add_cookie(cookie)
                
                self.random_sleep()  # 所有cookies加载完成后只延时一次
                self.logger.info('Cookies加载成功')
                return True
            except Exception as e:
                self.logger.error(f'加载Cookies时出错: {str(e)}')
                return False
        self.logger.warning('未找到已保存的Cookies文件')
        return False

    def quit(self):
        """关闭浏览器"""
        if self.driver:
            self.logger.info('关闭浏览器')
            self.driver.quit() 