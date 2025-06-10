import requests
import pandas as pd
from datetime import datetime
from app import db
from app.models.hot_article import HotArticle


class CrawlerService:
    @staticmethod
    def crawl_zhihu_hot():
        """
        爬取知乎热榜数据并返回
        """
        # 接口地址和参数
        url = "https://api.zhihu.com/topstory/hot-lists/total"
        params = {
            "limit": "50",
            "is_browse_model": "0"
        }

        # 构造请求头和cookies
        headers = {
            "User-Agent": "com.zhihu.android/Futureve/10.38.0 Mozilla/5.0 (Linux; Android 12; 24031PN0DC Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.1000.10 Mobile Safari/537.36",
            "Connection": "Keep-Alive",
            "x-api-version": "3.1.8",
            "isPreload": "false",
            "x-app-version": "10.38.0",
            "x-app-za": "OS=Android&Release=12&Model=24031PN0DC&VersionName=10.38.0&VersionCode=23810&Product=com.zhihu.android&Width=1080&Height=1920&Installer=VIVO%E8%BD%AF%E4%BB%B6%E5%95%86%E5%BA%97&DeviceType=AndroidPhone&Brand=Xiaomi",
            "x-app-bundleid": "com.zhihu.android",
            "x-app-flavor": "vivo",
            "x-app-build": "release",
            "x-network-type": "WiFi",
            "X-ZST-82": "2.00YeT2yjbghoMAAAASwUAADIuMHr_M2gAAAAAm0XhLGZ4O8K7NxVkEFXq1CRNjNk=",
            "x-udid": "pxAUqCjbghpLBUbHH9vLRpX2WW9Qr-K1esA=",
            "Authorization": "Bearer gt2.0AAAAAGGJAm0agtsoqBQQpwAAAAxNVQJgAgBv5qJ7dHwOAtkZRzoutLONFE3TWQ==",
            "X-Zse-96": "1.0_eV5XBY+WHERSCxqSZUvmZHrcqLT/naAwNMu0hMyGuxYCXYIhIB/0FqQ5jHF7Q1D1",
            "X-Zse-93": "101_1_1.0"
        }

        cookies = {
            "BEC": "e9bdbc10d489caddf435785a710b7029",
            "_xsrf": "3yK5vvt4XTT44ZFNm5JIBmsggrz9cNs0",
            "z_c0": "2|1:0|10:1748238203|4:z_c0|92:Z3QyLjBBQUFBQUdHSkFtMGFndHNvcUJRUXB3QUFBQXhOVlFKZ0FnQnY1cUo3ZEh3T0F0a1pSem91dExPTkZFM1RXUT09|ebc18ed5ed27606cd88520a015a01d53412f7389a55c013ab028e18fcf70ff19"
        }

        try:
            # 发送请求
            response = requests.get(url, headers=headers, cookies=cookies, params=params)

            # 检查响应状态
            if response.status_code != 200:
                return {"status": "error", "message": f"API请求失败，状态码: {response.status_code}"}

            # 解析JSON数据
            json_data = response.json()
            data_list = json_data['data']

            # 收集数据
            hot_articles = []
            for idx, data in enumerate(data_list, 1):
                # 提取所需字段
                title = data['target']['title_area']['text']
                description = data['target']['excerpt_area']['text'] if 'text' in data['target']['excerpt_area'] else ""
                article_url = data['target']['link']['url']
                hot_value = data['target']['metrics_area']['text']
                answer_count = data['feed_specific'].get('answer_count', 0)

                # 创建热榜文章对象
                article = HotArticle(
                    rank=idx,
                    title=title,
                    url=article_url,
                    hot_value=hot_value,
                    answer_count=answer_count,
                    description=description
                )
                hot_articles.append(article)

            return {"status": "success", "data": hot_articles}

        except Exception as e:
            return {"status": "error", "message": f"爬取过程中出错: {str(e)}"}

    @staticmethod
    def refresh_hot_data():
        """
        刷新知乎热榜数据，并存入数据库
        """
        result = CrawlerService.crawl_zhihu_hot()

        if result["status"] != "success":
            return result

        try:
            # 首先清空sentiment_analysis表中的数据，因为它引用了hot_articles表
            from app.models.sentiment_analysis import SentimentAnalysis
            db.session.query(SentimentAnalysis).delete()

            # 然后清空hot_articles表中的数据
            from app.models.hot_article import HotArticle
            db.session.query(HotArticle).delete()

            # 添加新数据
            db.session.add_all(result["data"])
            db.session.commit()

            return {"status": "success", "message": "数据刷新成功", "data": result["data"]}

        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": f"保存数据时出错: {str(e)}"}

    @staticmethod
    def get_latest_data():
        """
        从数据库获取最新的热榜数据
        """
        try:
            articles = HotArticle.query.order_by(HotArticle.rank).all()
            if not articles:
                # 如果数据库中没有数据，则爬取新数据
                refresh_result = CrawlerService.refresh_hot_data()
                if refresh_result["status"] == "success":
                    return {"status": "success", "data": refresh_result["data"], "is_fresh": True}
                else:
                    return refresh_result

            return {"status": "success", "data": articles, "is_fresh": False}

        except Exception as e:
            return {"status": "error", "message": f"获取数据时出错: {str(e)}"} 