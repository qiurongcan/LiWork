# 从PDF中提取文本
import re
import fitz

from openai import OpenAI
import os
import json
import csv
from pprint import pprint

# csv_file_path = 'output1.csv'


key = r'sk-t5Pc7liZ64RMDv9ogj7L7uB2sGyliaHSEYeS42ZoJrtiAkJI'

# os.environ["OPENAI_API_BASE"] = "https://api.openai-proxy.org/v1"
# os.environ["OPENAI_API_KEY"] = key

career = """
1.党的机关、国家机关、群众团体和社会组织、企事业单位负责人
2.专业技术人员
3.办事人员和有关人员
4.社会生产服务和生活服务人员
5.农、林、牧、渔业生产及辅助人员
6.生产制造及有关人员
7.军队人员
8.不便分类的其他从业人员
"""

client = OpenAI(
    base_url='https://api.openai-proxy.org/v1',
    api_key=key
)

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "一个善于提取各种文本信息的能手，需要帮助我准确提取各类信息"},
        {"role": "user", "content": "现在会给你提供各类职业信息的内容，一共分为8个大类，分别是"+career+",其中每一个大类又分成各种中类，中类又分成各种小类，现在需要提取各个小类的信息，需要包括职业代码，职业名称、职业说明和职业任务"},
        {"role": "assistant", "content":"好的，我明白了，我会在收到相关内容后进行分析，以“ \职业代码:XX,职业名称：XX，职业说明：XX，职业任务：XX\ 的json格式数据回答”，请你给出相关信息"},
        ],
    stream=True,
)
# 输出结果
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="") 



def parsePDF(filePath):
    # 将JSON数据转换为CSV
    # with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    #     writer = csv.DictWriter(file, fieldnames=["职业代码", "职业名称", "职业说明", "职业任务"])
    with fitz.open(filePath) as doc:
        
        i = 0
        for page in doc.pages():
            # print("----")
            
            # 从第10页开始请求
            text1 = ""
            # text0 = ""
            if i > 8:
                text0 = page.get_text("text")
                if len(text0) != 0:
                    text = text0 + text1
                    stream = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "user", "content":f"现在根据提供的信息：{text}，从中提取各个小类的信息，需要包括职业代码，职业名称、职业说明和职业任务，按照之前约定的格式输出,如果之前有输出过的内容则不需要输出，如果有重复内容则只输出一次。只需要json格式数据,只保存列表。"},
                        ],
                        stream=True,
                    )
                    with open(f'outdata/{i}.txt',mode='w',encoding='utf-8') as f:
                    
                        for chunk in stream:
                            if chunk.choices[0].delta.content is not None:
                                # 写入表头
                                # writer.writeheader()
                                result = chunk.choices[0].delta.content
                                result = result.replace("json",'')
                                result = result.replace("```","")

                                f.write(result)
                        print(f"完成第{i}次")
                text1 = text0
            


            i = i + 1


        if text:
            return text

if __name__ == "__main__":
    file_path = r'《中华人民共和国职业分类大典（2022版）》.pdf'
    text = parsePDF(filePath=file_path)
    # text = text.replace(" ", '')
    # with open(r'page100.txt', mode='w', encoding='UTF-8') as f:
    #     f.write(text)
    # # print(len(text))

    # with open(r'page100.txt', encoding='UTF-8') as f:
    #     textlines = f.readlines()

    # allcontent = ''.join([line.strip() for line in textlines])
    # print(len(allcontent))
    # allcontent = allcontent.replace("　",'')
    # print(len(allcontent))
    # print(allcontent[:910])
    # with open("aa.txt",mode='w',encoding='utf-8') as f:
    #     f.write(allcontent)

    # obj = re.compile(textlines[0]+'(.*?)'+textlines[0])
    # result = obj.findall(text)
    # print(len(result))
