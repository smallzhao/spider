import requests
import json
from retrying import retry


class DoubanSpider:
    def __init__(self):

        self.url_temp_list = [
            {
                "url_temp":"https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?start={}&count=18&loc_id=108288",
                "country":"US"
            },
            {
                "url_temp":"https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_english_hot/items?start={}&count=18&loc_id=108288",
                "country":"UK"
            },
            {
                "url_temp":"https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_domestic_hot/items?start={}&count=18&loc_id=108288",
                "country":"CN"
            }
        ]
        self.headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36"}

    @retry(stop_max_attempt_number=3)
    def _send_request(self, url):
        response = requests.get(url, headers=self.headers, timeout=5)
        assert response.status_code == 200
        return response

    def send_request(self, url):
        """发送请求，获取响应"""
        try:
            response = self._send_request(url)
        except:
            response = None
        return response

    def save_data(self, response_data, country):
        """保存数据"""
        file_path = "{}电视.txt".format(country)
        with open(file_path, "w") as f:
            for content in response_data:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")

    def handle_data(self, response):
        """提取数据"""
        # 解码
        response = response.content.decode()
        response_data = json.loads(response)
        # 获取数据列表
        content_list = response_data["subject_collection_items"]

        return content_list

    def run(self):
        """运行爬虫"""
        for url_temp in self.url_temp_list:
            i = 0
            while True:
                # 构建url
                url = url_temp["url_temp"].format(i)
                print(url)
                # 发送请求
                response = self.send_request(url)
                # response = requests.get(url, headers=self.headers)
                # print(response)
                # 提取数据
                content_list = self.handle_data(response)
                # 判断本页电影数量
                count = len(content_list)
                if count < 18:
                    break
                # 保存数据
                self.save_data(content_list, url_temp["country"])
                i += 18


if __name__ == '__main__':

    china_tv = DoubanSpider()
    china_tv.run()