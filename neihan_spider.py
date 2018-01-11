import requests, re, json


class NeiHanspider:
    def __init__(self):

        self.start_url = "http://neihanshequ.com/"
        self.next_url = "http://neihanshequ.com/joke/?is_json=1&app_name=neihanshequ_web&max_time={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
    def send_request(self, url):
        """发送请求获取数据"""
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_first_max_time(self, html_str):
        """处理第一次数据获得max_time"""
        content_list = re.findall(r"<h1 class=\"title\">.*?<p>(.*?)</p>", html_str, re.S)
        max_time = re.findall(r"max_time: '(.*)'", html_str)[0]
        return content_list, max_time

    def save_data(self, content_list):
        """保存数据"""
        with open("neihan.txt", "a", encoding="utf-8") as f:
            for content in content_list:
                f.write(content)
                f.write("\n")
            print("保存成功")

    def handel_next_data(self, json_str):
        """处理第一页之后的数据"""
        json_data = json.loads(json_str)
        # 获取max_time
        max_time = json_data["data"]["max_time"]
        # 获取是否有下一页
        has_more = json_data["data"]["has_more"]
        # 获取内容列表
        data = json_data["data"]["data"]
        content_list = [i["group"]["content"] for i in data]
        return content_list, max_time, has_more

    def run(self):
        # 第一次请求数据
        html_str = self.send_request(self.start_url)
        # 处理数据
        content_list, max_time = self.get_first_max_time(html_str)
        # 保存数据
        self.save_data(content_list)

        has_more = True
        while has_more:
            # 构造下一次url
            url = self.next_url.format(max_time)
            print(url)
            # 发请求
            json_str = self.send_request(url)
            # 处理数据
            content_list, max_time, has_more = self.handel_next_data(json_str)
            # 保存数据
            self.save_data(content_list)


if __name__ == '__main__':
    neihan = NeiHanspider()
    neihan.run()