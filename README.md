# 小红书笔记采集工具

## 项目说明
本项目是一个基于Selenium的小红书笔记采集工具，可以根据关键词搜索并采集笔记数据。

## 功能特点
- 支持Cookie登录和手动登录
- 自动滚动加载更多内容
- 实时采集笔记数据
- 自动去重和数据保存
- 详细的日志记录

## 系统要求
- Python 3.7+
- Chrome浏览器
- ChromeDriver (与Chrome版本匹配)

## 安装依赖
```bash
pip install -r requirements.txt
```

## 目录结构
```
├── main.py              # 主程序入口
├── utils/              # 工具模块目录
│   ├── extractor.py    # 数据提取模块
│   ├── login.py        # 登录处理模块
│   ├── scroll.py       # 滚动加载模块
│   ├── search.py       # 搜索处理模块
│   └── logger.py       # 日志处理模块
├── config/             # 配置文件目录
│   └── cookies.json    # Cookies配置文件
├── data/              # 数据存储目录
├── logs/              # 日志存储目录
└── drivers/           # 驱动程序目录
```

## 使用说明

### 1. 配置ChromeDriver
1. 下载与Chrome浏览器版本匹配的ChromeDriver
2. 将ChromeDriver放置在项目的drivers目录下
3. 修改ChromeDriver路径配置：
   - 打开 `config/config.py` 文件
   - 找到以下代码行：
     ```python
     CHROME_DRIVER_PATH = '/Users/tx/Documents/python_project/chromedriver-mac-arm64/chromedriver'
     ```
   - 将路径修改为你的ChromeDriver实际位置
   - 例如：
     - Windows: `CHROME_DRIVER_PATH = 'drivers/chromedriver.exe'`
     - Mac/Linux: `CHROME_DRIVER_PATH = 'drivers/chromedriver'`

### 2. 运行程序
```bash
python main.py
```

### 3. 登录方式
- 首次使用需要手动登录，程序会保存登录状态
- 后续运行会优先使用已保存的Cookies登录
- 如果Cookies失效，需要重新手动登录

### 4. 数据格式
采集的数据以JSON格式保存，包含以下字段：
```json
{
    "title": "笔记标题",
    "note_url": "笔记链接",
    "author": "作者名称",
    "likes": "点赞数"
}
```

### 5. 配置说明
- 日志文件：logs/spider_{日期}.log
- 数据文件：data/notes_data.json
- Cookies文件：config/cookies.json

## 注意事项
1. 确保Chrome浏览器已安装
2. ChromeDriver版本必须与Chrome浏览器版本匹配
3. 首次运行需要手动登录
4. 采集过程中请勿关闭浏览器窗口
5. 遵守小红书的使用规范和速率限制

## 网页结构变化处理
当小红书更新网页结构后，程序可能无法正常获取数据。此时需要：

1. 打开小红书网页，找到要采集的元素
2. 获取新的选择器：
   - 右键点击元素，选择"检查"
   - 在开发者工具中右键点击对应的HTML元素
   - 选择 "Copy" -> "Copy selector"
   - 这样获取到的就是元素的CSS选择器
   
   注意：
   - 不要使用 "Copy JS path" 或 "Copy XPath"等
   - 如果复制到的选择器过于复杂（包含很多:nth-child之类的），建议手动简化
   - 确保选择器是稳定的，不要包含可能变化的id或class

3. 修改 `utils/extractor.py` 文件中的选择器：
   ```python
   # 标题选择器
   title_elem = card.find_element(By.CSS_SELECTOR, "div > div > a > span")
   
   # 链接选择器
   link = card.find_element(By.CSS_SELECTOR, "div > a.cover.ld.mask")
   
   # 作者选择器
   author_elem = card.find_element(By.CSS_SELECTOR, "div > div > div > a > span")
   
   # 点赞数选择器
   likes_elem = card.find_element(By.CSS_SELECTOR, "div > div > div > span > span.count")
   ```

4. 将获取到的新选择器替换对应的旧选择器
5. 保存文件并重新运行程序

提示：如果不确定选择器是否正确，可以在浏览器的Console中测试：
```javascript
// 例如测试标题选择器
document.querySelector("你的选择器").innerText
```
如果能正确返回目标内容，说明选择器有效。

## 常见问题
1. ChromeDriver相关错误
   - 检查Chrome版本是否匹配
   - 确认驱动路径是否正确
   - 验证驱动文件是否有执行权限

2. 登录相关问题
   - Cookies失效需要重新登录
   - 手动登录时要在提示后输入y确认

3. 数据采集问题
   - 确保网络连接稳定
   - 检查CSS选择器是否更新
   - 查看日志文件了解详细错误信息 