import requests, json
from lxml import etree


class TieBaSpider:

    def __init__(self, tieba_name):

        self.tieba_name = tieba_name
        self.start_url = "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---1/m?kw="+ tieba_name +"&lp=0"
        self.base_url = "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---1/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36"}

    def parse_url(self, url):
        """发送请求，获取响应"""
        print(url)
        response = requests.get(url, headers=self.headers)
        # return response.content.decode()
        return response.content

    def get_content_list(self, html_str):
        """提取数据"""
        html = etree.HTML(html_str)
        div_list = html.xpath("//div[contains(@class, 'i')]")
        content_list = []
        for div in div_list:
            item = {}
            item["href"] = self.base_url + div.xpath("./a/@href")[0] if len(div.xpath("./a/@href"))>0 else None
            item["title"] = div.xpath("./a/text()")[0] if len(div.xpath("./a/text()"))>0 else None
            item["image_list"] = self.get_image_list(item["href"], [])
            content_list.append(item)

        # 获取下一页地址
        next_url = self.base_url + html.xpath("//a/text() = '下一页'/@href")[0] if len(html.xpath("//a/text() = '下一页'/@href")) else None
        return content_list, next_url

    def get_image_list(self, detail_url, total_image_list):
        """获取详情页图片"""
        # 发起请求获取数据
        detail_html_str = self.parse_url(detail_url)
        # 提取数据
        detail_html = etree.HTML(detail_html_str)
        image_list = detail_html.xpath("//img[@class='BDE_Image']/@src")
        total_image_list.append(image_list)
        next_detail_url = detail_html.xpath("//a/[text()='下一页']/@href")
        if len(next_detail_url) > 0:
            # 获取下一页url
            next_detail_url = self.base_url + detail_html.xpath("//a/[text()='下一页']/@href")[0]

            return self.get_image_list(next_detail_url, total_image_list)

        return total_image_list

    def save_data(self, content_list):
        """保存数据"""
        with open("{}.txt".format(self.tieba_name), "a") as f:
            for content in content_list:
                f.write(json.dumps(content))
                f.write("/n")
            print("保存成功")


    def run(self):
        # 构建url列表
        next_url = self.start_url
        while next_url is not None:
            # 发送请求获取响应
            html_str = self.parse_url(self.start_url)
            # 发送请求，提取数据
            content_list, next_url = self.get_content_list(html_str)
            # 保存数据
            self.save_data(content_list)


if __name__ == '__main__':
    tieba_spider = TieBaSpider("猫")
    tieba_spider.run()