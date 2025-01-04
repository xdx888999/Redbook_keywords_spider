"""
数据提取模块
作者：来碗麻辣烫
创建日期：2024-03-21

功能说明：
    从小红书笔记卡片中提取标题、链接、作者和点赞数等数据。

主要类：
    NoteExtractor：提取笔记数据的核心类
"""

from selenium.webdriver.common.by import By

class NoteExtractor:
    def __init__(self, logger):
        self.logger = logger

    def extract_note_data(self, card):
        """
        从笔记卡片中提取数据
        :param card: 笔记卡片元素
        :return: dict 笔记数据
        """
        try:
            note_data = {
                'title': '',
                'note_url': '',
                'author': '',
                'likes': '0'
            }
            
            # 提取标题
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, "div > div > a > span")
                title = title_elem.text.strip()
                if title:
                    note_data['title'] = title
            except:
                self.logger.warning("未找到标题")
            
            # 提取笔记链接
            try:
                link = card.find_element(By.CSS_SELECTOR, "div > a.cover.ld.mask")
                href = link.get_attribute('href')
                if href:
                    note_data['note_url'] = href
            except:
                self.logger.warning("未找到笔记链接")
            
            # 提取作者
            try:
                author_elem = card.find_element(By.CSS_SELECTOR, "div > div > div > a > span")
                if author_elem:
                    note_data['author'] = author_elem.text.strip()
            except:
                self.logger.warning("未找到作者")
            
            # 提取点赞数
            try:
                likes_elem = card.find_element(By.CSS_SELECTOR, "div > div > div > span > span.count")
                likes = likes_elem.text.strip()
                # 如果点赞数为空或者显示"赞"，则设为"0"
                if not likes or likes == "赞":
                    note_data['likes'] = '0'
                else:
                    note_data['likes'] = likes
            except:
                self.logger.warning("未找到点赞数")
            
            # 如果至少有标题或链接，则返回数据
            if note_data['title'] or note_data['note_url']:
                self.logger.info(f"成功提取笔记: {note_data['title'][:20] if note_data['title'] else '无标题'}...")
                return note_data
            
            return None
            
        except Exception as e:
            self.logger.error(f"提取笔记数据时出错: {str(e)}")
            return None 