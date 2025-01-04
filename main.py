"""
主程序模块
作者：来碗麻辣烫
创建日期：2024-03-21

功能说明：
    小红书笔记采集程序的入口，负责初始化系统、处理登录和执行数据采集。

主要流程：
    1. 初始化系统和登录
    2. 执行笔记搜索和数据采集
    3. 保存采集结果
"""

import os
from utils.logger import Logger
from utils.login import XHSLogin
from utils.search import XHSSearch
from config.config import CHROME_DRIVER_PATH

def main():
    # 初始化日志
    logger = Logger()
    logger.info('程序启动')
    
    # 配置文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cookies_path = os.path.join(current_dir, 'config', 'cookies.json')
    
    try:
        # 初始化登录模块
        login_handler = XHSLogin(CHROME_DRIVER_PATH, cookies_path, logger)
        login_handler.init_driver()
        
        # 尝试使用cookies登录
        if login_handler.load_cookies():
            logger.info('使用已保存的Cookies登录')
            login_handler.driver.get('https://www.xiaohongshu.com')
            logger.info('登录成功！')
        else:
            # 如果cookies无效，则进行手动登录
            logger.info('需要手动登录')
            if not login_handler.manual_login():
                logger.error('登录失败')
                return
        
        # 初始化搜索模块
        search_handler = XHSSearch(login_handler.driver, logger)
        
        # 获取用户输入的关键词
        keyword = input('请输入要搜索的关键词: ')
        
        # 搜索并获取笔记数据
        notes_data = search_handler.search_notes(keyword)
        
        # 保存数据
        if notes_data:
            logger.info(f"共获取到 {len(notes_data)} 条笔记")
            search_handler.save_notes_data(notes_data=notes_data, keyword=keyword)
        else:
            logger.warning("未找到任何笔记")
            
    except Exception as e:
        logger.error(f'程序运行出错: {str(e)}')
    finally:
        # 关闭浏览器
        if 'login_handler' in locals() and login_handler.driver:
            logger.info('关闭浏览器')
            login_handler.driver.quit()

if __name__ == '__main__':
    main() 