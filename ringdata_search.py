# coding: utf-8
import requests
import pandas as pd
from tqdm import tqdm
import time


def scrapy_main(url, post_data):
    res = requests.post(url, headers=headers, json=post_data)
    return res.json()


def replace_text(text):
    return text.replace("<font color='red'>", "").replace("</font>", "").strip()


def parse_json(data):
    esHitList = data["data"]["esSearchResult"]["esHitList"]
    lst = []
    for item in esHitList:
        lst.append(
            [
                item["entity"]["title"],
                item["entity"]["media_name"],
                replace_text(item["entity"]["ctHighLight"]),
                item["entity"]["pub_time"],
            ]
        )
    return lst


if __name__ == "__main__":
    s_page, e_page = 1, 183
    keyword_all = "贪污 元"  # 包含以下全部关键词
    keyword_any = ""  # 包含以下任一关键词
    keyword_not = ""  # 不包含以下关键词
    page_size = 20  # 默认是20，可以适当调大，以减少翻页次数，但不确定是否会触发反爬

    start_date = "2006-01-01"  # 开始时间，如2020-10-01
    end_date = "2006-12-31"  # 结束时间，如2021-11-03
    location = "1"  # 在新闻全文中，若为"2"，则表示仅在新闻标题中

    media = ""  # 限定要搜索的新闻源，如"广东省湛江市人民政府"，超过2k个，就不一一列举了
    sort_type = 2 # 按相关度排序，若为1，则表示按时间排序

    url = "https://www.ringdata.com/ringdataApi/news/v1/ESQuery"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    }

    post_data = {
        "newsType": 1,
        "keywords": "",
        "from": "",
        "pageSize": page_size,
        "media": media,
        "sortType": sort_type,
        "startDate": start_date,
        "endDate": end_date,
        "category": "",
        "dataBaseType": "",
        "keywordsAllList": keyword_all,
        "keywordsAnyList": keyword_any,
        "keywordsNotList": keyword_not,
        "location": location,
    }

    res_lst = []
    for page in tqdm(range(s_page, e_page + 1)):
        post_data["from"] = page
        try:
            res_data = scrapy_main(url, post_data)
        except Exception as e:
            print(e, page)
            break
        res_lst += parse_json(res_data)
        time.sleep(0)

    columns = ["标题", "媒体名称", "内容", "发布时间"]
    df = pd.DataFrame(res_lst, columns=columns)
    keyword_fname = "-".join((keyword_all, keyword_any, keyword_not))
    df.to_excel("{}_{}_{}.xlsx".format(keyword_fname, s_page, e_page), index=False)