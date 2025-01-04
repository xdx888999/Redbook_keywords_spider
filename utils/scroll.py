"""
滚动加载模块
作者：来碗麻辣烫
创建日期：2024-03-21

功能说明：
    实现页面滚动加载功能，控制页面滚动并检测新内容加载。

主要类：
    ScrollLoader：滚动加载的核心类
"""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

class ScrollLoader:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        
    def scroll_to_bottom(self):
        """滚动到页面底部"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
    def get_page_height(self):
        """获取页面高度"""
        return self.driver.execute_script("return document.body.scrollHeight")
        
    def scroll_and_extract(self, extractor, max_retries=3, scroll_pause_time=2):
        """边滚动边提取数据，直到无法加载新内容"""
        last_height = self.get_page_height()
        no_new_content_count = 0
        processed_notes = set()  # 用于存储已处理的笔记的唯一标识
        total_notes = []
        
        while no_new_content_count < max_retries:
            # 1. 提取当前可见的笔记
            try:
                note_cards = self.driver.find_elements(By.CSS_SELECTOR, ".note-item")
                self.logger.info(f"当前页面找到 {len(note_cards)} 个笔记")
                
                # 处理新的笔记
                for card in note_cards:
                    try:
                        # 获取笔记的唯一标识（使用链接或其他属性）
                        note_id = card.get_attribute('data-id') or card.get_attribute('id') or hash(card.text)
                        
                        # 如果是新的笔记，则处理
                        if note_id not in processed_notes:
                            note_data = extractor.extract_note_data(card)
                            if note_data:
                                total_notes.append(note_data)
                                processed_notes.add(note_id)
                    except StaleElementReferenceException:
                        continue  # 如果元素已经不在DOM中，跳过这个笔记
            except Exception as e:
                self.logger.error(f"提取笔记数据时出错: {str(e)}")
            
            # 2. 滚动到底部
            self.scroll_to_bottom()
            time.sleep(scroll_pause_time)  # 等待新内容加载
            
            # 3. 检查是否有新内容
            new_height = self.get_page_height()
            if new_height == last_height:
                no_new_content_count += 1
                self.logger.info(f"未检测到新内容，重试次数: {no_new_content_count}/{max_retries}")
            else:
                no_new_content_count = 0  # 如果有新内容，重置计数器
                
            last_height = new_height
            
        self.logger.info(f"滚动加载完成，共获取到 {len(total_notes)} 条笔记")
        return total_notes
    
    def wait_for_elements(self, locator, timeout=5):
        """等待元素加载"""
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            if elements:
                self.logger.info(f"找到 {len(elements)} 个元素")
            return elements
        except TimeoutException:
            self.logger.warning(f"等待元素超时: {locator}")
            return None
        except Exception as e:
            self.logger.error(f"等待元素时出错: {str(e)}")
            return None 