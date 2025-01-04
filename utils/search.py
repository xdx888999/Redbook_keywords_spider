"""
搜索处理模块
作者：来碗麻辣烫
创建日期：2024-03-21

功能说明：
    处理小红书笔记的搜索功能，包括执行搜索和保存结果。

主要类：
    SearchHandler：搜索处理的核心类
"""

import json
import time
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from utils.scroll import ScrollLoader
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.extractor import NoteExtractor

class XHSSearch:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.search_url = "https://www.xiaohongshu.com"
        self.scroll_loader = ScrollLoader(driver, logger)
        self.extractor = NoteExtractor(logger)
        
    def search_notes(self, keyword):
        """搜索笔记并提取数据"""
        self.logger.info(f'开始搜索关键词: {keyword}')
        
        try:
            # 构造搜索URL
            search_url = f"{self.search_url}/search_result?keyword={keyword}"
            self.driver.get(search_url)
            time.sleep(5)  # 等待页面加载
            
            # 等待笔记内容加载
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".note-item"))
                )
            except:
                self.logger.warning("等待笔记加载超时")
                return []
            
            # 使用新的滚动加载方法
            notes_data = self.scroll_loader.scroll_and_extract(self.extractor)
            
            if notes_data:
                # 数据去重
                unique_notes = self.remove_duplicates(notes_data)
                self.logger.info(f"共获取到 {len(notes_data)} 条笔记，去重后剩余 {len(unique_notes)} 条")
                return unique_notes
            else:
                self.logger.warning("未找到任何笔记")
                return []
            
        except Exception as e:
            self.logger.error(f"搜索笔记时出错: {str(e)}")
            return []

    def remove_duplicates(self, notes_data):
        """根据笔记链接去除重复数据"""
        unique_notes = {}
        for note in notes_data:
            # 使用笔记链接作为唯一标识
            if note.get('note_url'):
                unique_notes[note['note_url']] = note
            # 如果没有链接，使用标题作为备选标识
            elif note.get('title'):
                unique_notes[note['title']] = note
        
        # 转换回列表
        return list(unique_notes.values())

    def save_notes_data(self, notes_data, keyword):
        """保存笔记数据到文件"""
        if not notes_data:
            self.logger.warning('没有笔记数据可保存')
            return
            
        try:
            # 确保data目录存在
            data_dir = 'data'
            os.makedirs(data_dir, exist_ok=True)
            
            # 生成文件名（使用关键词）
            filename = os.path.join(data_dir, f'{keyword}_notes.json')
            
            # 如果文件已存在，先读取已有数据
            existing_notes = []
            if os.path.exists(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        existing_notes = json.load(f)
                    self.logger.info(f"从文件中读取到 {len(existing_notes)} 条已存在的笔记")
                except:
                    self.logger.warning("读取已存在的笔记数据失败")
            
            # 合并新旧数据并去重
            all_notes = existing_notes + notes_data
            unique_notes = self.remove_duplicates(all_notes)
            
            # 保存去重后的数据
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(unique_notes, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f'笔记数据已保存到文件: {filename}')
            if len(existing_notes) > 0:
                self.logger.info(f'合并后共有 {len(unique_notes)} 条唯一笔记')
            
        except Exception as e:
            self.logger.error(f'保存笔记数据时出错: {str(e)}') 