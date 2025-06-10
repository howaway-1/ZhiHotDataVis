# 🔥 ZhiHotDataVis · 基于知乎平台的热门问题与回答数据分析与可视化系统
> 🎓 本项目为我的毕业设计作品，作者：[howaway-1](https://github.com/howaway-1)  
> 📍 项目地址：[https://github.com/howaway-1/ZhiHotDataVis](https://github.com/howaway-1/ZhiHotDataVis)

## 🧠 项目简介

**ZhiHotDataVis** 是一个基于 Flask 框架开发的知乎数据分析与可视化系统。它通过爬取知乎热榜内容与回答数据，结合中文自然语言处理技术，对关键词、情感倾向、用户行为等进行分析，并以丰富的图表和词云形式进行可视化呈现，帮助用户全面理解知乎热点趋势。

本项目涵盖完整的数据采集、分析处理、后端 API、前端交互与图表展示流程，适合作为数据分析类项目参考。

## ✨ 项目亮点

- 🔍 **知乎热榜实时爬取**：采集知乎每日热榜问题与热门回答
- ☁️ **热词统计与词云图**：基于 jieba 提取关键词并生成词频图
- 😊 **情感倾向分析**：使用 SnowNLP 进行文本情感分类
- 📊 **可视化仪表盘**：集成 ECharts 展示多维度统计图表
- 👤 **用户行为分析**：分析用户活跃度、回答数、点赞数等
- 💻 **前后端协作架构**：Flask 提供 RESTful API 接口 + 前端页面展示

## 🧰 技术栈

| 类型       | 技术/工具              |
|------------|------------------------|
| 后端       | Flask, Flask-Bootstrap, Flask-CORS |
| 数据处理   | Pandas, jieba, SnowNLP |
| 数据可视化 | ECharts, pyecharts, wordcloud |
| 爬虫       | Requests, BeautifulSoup |
| 数据库     | SQLite                 |
| 前端模板   | HTML5, CSS3, JavaScript, Jinja2 |
| 配置管理   | configparser           |

## 📁 项目结构
ZhiHotDataVis/
├── app/
│ ├── controllers/ # 控制器层，处理页面路由与请求
│ ├── models/ # 数据模型封装
│ ├── services/ # 业务逻辑与数据处理
│ ├── utils/ # 工具类（爬虫、情感分析、分词等）
│ ├── templates/ # Jinja2 模板页面
│ └── static/ # 静态资源：CSS / JS / 图表
├── config/
│ └── config.ini # 项目配置文件
├── data/ # 存储采集后的知乎数据
├── main.py # Flask 应用入口
├── requirements.txt # Python 依赖列表
└── README.md # 项目说明文档

 使用说明
所有数据均由知乎公开页面获取，仅供学习用途
可在 app/utils/ 目录中添加更多分析算法或自定义模块
图表交互基于 ECharts，可自行拓展样式或联动

📄 开源协议
本项目开源仅供学习研究使用。数据采集涉及第三方知乎平台内容，请勿用于商业用途。若项目中涉及侵权内容请及时联系删除。

