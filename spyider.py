import re
import time
from urllib import request


class Spider:
    # 根据不同的题库,URL要改一下
    url = "http://210.44.14.75/redir.php?catalog_id=6&cmd=learning&tikubh=30171&page="
    # url = "http://210.44.14.75/redir.php?catalog_id=6&cmd=learning&tikubh=17825&page="
    root_pattern = r'<div class="shiti-content">[\s\S]*?<div class="fy">'
    Q_A_pattern = r'<div class="shiti"><h3>[\s\S]*?）</span>'
    mod_pattern = r'xuanxiang_panduan'  # 用于判断题型
    question_pattern = r'<h3>([\s\S]*)?</h3>'  # 题干
    chosen_pattern = r'>([A-D].[\s\S]*?)[(\r)(</label>)]'  # 选项
    answer_pattern = r'标准答案：([\s\S]*)）</span>'  # 判断题
    answer_pattern_2 = r'(标准答案：[\s\S]*)\r\n'  # 选择题
    page_num = 223 # 信工的题库共223页,根据需要更改

    # 匹配所有字符的正则表达式,*表示匹配中间字符,?表示非贪婪模式,只匹配到第一个/div为止

    def __fetch_content(self, url):
        # 模仿HTTP请求
        r = request.urlopen(url)
        htmls = r.read()  # 此时html编码是字节码
        htmls = str(htmls, encoding='utf-8')  # 使用str-encoding将html转为GB2312编码的字符串
        return htmls

    # 分析文本
    def __analysis(self, htmls):
        root_html = re.findall(self.root_pattern, htmls)
        Q_A_list = []
        for text in root_html:
            # 提取出问题题干以及选项还有答案
            Q_A_text = re.findall(self.Q_A_pattern, text)
            # print(Q_A_text)
            for x in Q_A_text:
                question_text = re.findall(self.question_pattern, x)
                question_text = str(question_text)[8:-2]
                Q_A_list.append(question_text)
                if re.search(self.mod_pattern, x) != None:
                    # 如果是判断题,直接跳过选项保留答案
                    answer_text = re.findall(self.answer_pattern, x)
                    answer_text = str(answer_text).replace(' ', '')
                    Q_A_list.append(answer_text)
                    continue
                else:
                    # 如果是选择题,依次将选项和答案保留
                    chosen_text = re.findall(self.chosen_pattern, x)
                    Q_A_list.append(chosen_text)
                    answer_text = re.findall(self.answer_pattern_2, x)
                    answer_text = str(answer_text).replace(' ', '')
                    Q_A_list.append(answer_text)
        return Q_A_list

    # 输出
    def __OutPutToText(self, Q_A_text):
        f = open("Question.txt", 'a')
        for x in Q_A_text:
            text = str(x)
            f.write(text + '\n')
        f.close()

    # 入口以及总控方法
    def main(self):
        print('Please wait a minute')
        start = time.perf_counter()
        for i in range(1, self.page_num):
            page_num = str(i)
            url = self.url + page_num
            htmls = self.__fetch_content(url)
            Q_A_list = self.__analysis(htmls)
            self.__OutPutToText(Q_A_list)
        end = time.perf_counter()
        print('Success')
        print('Run time : ' + str(end - start) + "s")


if __name__ == '__main__':
    s = Spider()
    s.main()
