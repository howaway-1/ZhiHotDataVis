from collections import Counter
import jieba
import jieba.analyse
from snownlp import SnowNLP
import re

def generate_word_cloud(text):
    """
    生成词云图数据

    Args:
        text: 要分析的文本内容

    Returns:
        词云图数据，格式为 [{'name': '词语1', 'value': 频率1}, ...]
    """
    try:
        # 扩展停用词列表
        stop_words = {'的', '了', '和', '是', '在', '有', '被', '？', '如何', '为什么', '吗', '为何', '多', '大', '小', '上', '下', '年', '月', '日', '等', '中', '个', '这', '那', '什么', '哪些', '怎么', '还', '都', '就', '你', '我', '他', '她', '啊', '吧', '呢', '哦', '哈', '哎', '呀', '嗯', '哪', '么'}

        # 使用jieba进行中文分词，确保分词结果有效
        if not text or len(text) < 5:
            # 如果文本太短，使用默认值
            return [
                {'name': '知乎', 'value': 100},
                {'name': '热榜', 'value': 80},
                {'name': '话题', 'value': 60},
                {'name': '数据', 'value': 50},
                {'name': '分析', 'value': 40}
            ]

        # 使用 jieba 的关键词提取更准确地获取重要词汇
        keywords = jieba.analyse.extract_tags(text, topK=50, withWeight=True)
        if keywords:
            # 直接使用关键词提取结果
            word_cloud_data = [{'name': word, 'value': int(weight * 100)} for word, weight in keywords]
            return word_cloud_data

        # 如果关键词提取失败，则回退到基本分词
        words = jieba.cut(text)
        filtered_words = [word for word in words if len(word) > 1 and word not in stop_words]

        # 统计词频
        word_count = Counter(filtered_words).most_common(100)

        # 生成词云图数据
        word_cloud_data = [{'name': word, 'value': count} for word, count in word_count]

        return word_cloud_data
    except Exception as e:
        # 出现异常时返回一些默认数据，确保前端能够正常显示
        print(f"生成词云数据时出错: {str(e)}")
        return [
            {'name': '知乎', 'value': 100},
            {'name': '热榜', 'value': 80},
            {'name': '话题', 'value': 60},
            {'name': '数据', 'value': 50},
            {'name': '分析', 'value': 40}
        ]

def perform_sentiment_analysis(text):
    """
    执行情感分析

    Args:
        text: 要分析的文本内容

    Returns:
        情感分析结果，包括情感分数、积极词数、消极词数、中性词数和关键词
    """
    try:
        # 使用SnowNLP进行情感分析
        s = SnowNLP(text)
        sentiment_score = s.sentiments # 获取整段话的情感度

        # 分词
        words = list(jieba.cut(text))

        # 过滤停用词
        stop_words = {'的', '了', '和', '是', '在', '有', '被', '？', '如何', '为什么', '吗', '为何', '多', '大', '小', '上', '下', '年', '月', '日', '等', '中', '个', '这', '那', '什么', '哪些', '怎么', '还', '都', '就', '你', '我', '他', '她', '啊', '吧', '呢', '哦', '哈', '哎', '呀', '嗯', '哪', '么'}
        filtered_words = [word for word in words if len(word) > 1 and word not in stop_words]

        # 计算积极词、消极词和中性词数量
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        for word in filtered_words:
            try:
                word_score = SnowNLP(word).sentiments # 获取这段话中每一个词的情感度，统计情感度词汇分布
                print(word, ':', word_score)
                if word_score > 0.7:
                    positive_count += 1
                elif word_score < 0.3:
                    negative_count += 1
                else:
                    neutral_count += 1
            except:
                # 如果单个词分析出错，将其归为中性
                neutral_count += 1

        # 提取关键词
        keywords = jieba.analyse.extract_tags(text, topK=10)
        # total_words = positive_count + negative_count + neutral_count
        #
        # if total_words == 0:  # 防止除以零
        #     sentiment_score = 0  # 如果没有词汇，情感得分设为0%
        # else:
        #     sentiment_score = (positive_count / total_words) * 100  # 转换为百分比

        return sentiment_score, positive_count, negative_count, neutral_count, keywords
    except Exception as e:
        print(f"情感分析出错: {str(e)}")
        # 出错时返回默认值
        return 0.5, 0, 0, 0, []

def extract_numbers_from_hot_value(hot_value):
    """
    从热度值中提取数字部分

    Args:
        hot_value: 热度值，如 "4307 万热度"

    Returns:
        提取出的数字，如 4307
    """
    if not hot_value:
        return 0

    # 使用正则表达式提取数字部分
    number_match = re.search(r'\d+', hot_value)
    if number_match:
        return int(number_match.group())
    return 0 