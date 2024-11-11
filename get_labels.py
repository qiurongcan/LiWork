# 通过GPT获取标签

# 获取技能和技能影响程度
# 根据职业匹配相应的13个技能有哪些
from openai import OpenAI
import os
import json
import csv
import pandas as pd

# 读取原始数据
origin_data = pd.read_csv(r'output.csv', index_col=None)
# origin_data = origin_data.to_string()
# print(origin_data)
# answer_style = """

# """

# 创建OpenAI的api链接
key = r'sk-t5Pc7liZ64RMDv9ogj7L7uB2sGyliaHSEYeS42ZoJrtiAkJI'
client = OpenAI(
    base_url='https://api.openai-proxy.org/v1',
    api_key=key
)

ability = """
"""

# 预热提问，告诉GPT它的任务是什么
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "一个善于提取各种文本信息的能手，根据我提供的信息，提取我需要的内容。"},
        {"role": "user", "content": f"现在会给你提供很多职业信息的相关内容，你需要从这些信息中获取提供的所有职业最需要的50种技能，并且按照技能重要程度，从重要到不太重要排序。"},
        {"role": "assistant", "content":f"好的，我明白了，我会在收到相关内容后进行分析，并json格式数据回答”，请你给出相关信息"},
        ],
    stream=True,
)
# print(stream)
# 输出结果
for chunk in stream:
    # print(chunk.choices[0])
    if len(chunk.choices) != 0:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="") 


def get_label():
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content":f"现在根据提供的信息：{origin_data},根据这些信息，综合进行考虑，结合每一个职业的特性，获取提供的所有职业最需要的50种技能，并且按照技能重要程度，从重要到不太重要排序,以json格式数据回答”，严格遵照这一个格式执行。"},
        ],
        stream=True,
    )
    with open(f'skills_label.txt',mode='w',encoding='utf-8') as f:
    
        for chunk in stream:
            if len(chunk.choices) != 0:
                if chunk.choices[0].delta.content is not None:
                    
                    result = chunk.choices[0].delta.content
                    result = result.replace("json",'')
                    result = result.replace("```","")
                    f.write(result)


# def getSkill():
 
#     for i in range(len(origin_data.index)):
#         # 读取每一行的数据
#         # data = origin_data[i]
#         if i < 1852:
#             continue
#         code = origin_data.iloc[i, 0]
#         name = origin_data.iloc[i, 1]
#         explain = origin_data.iloc[i, 2]
#         task = origin_data.iloc[i, 3]


#         stream = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "user", "content":f"现在根据提供的信息：职业代码：{code},职业名称:{name},职业说明:{explain},职业任务:{task}，根据这些信息，匹配这类职业需要哪些技能,根据给你提供的职业信息的内容，现在有对应15种能力，每一种能力使用数字表示需要这项能力的程度。这15项能力分别是{ability}，现在需要根据我提供的信息，判断这个职业需要哪些能力，且能力需要达到哪一个程度。以{answer_style}的json格式数据回答”，严格遵照这一个格式执行，只保存列表。"},
#             ],
#             stream=True,
#         )
#         with open(f'AbilityData/{i}.txt',mode='w',encoding='utf-8') as f:
        
#             for chunk in stream:
#                 if len(chunk.choices) != 0:
#                     if chunk.choices[0].delta.content is not None:
#                         # 写入表头
#                         # writer.writeheader()
#                         result = chunk.choices[0].delta.content
#                         result = result.replace("json",'')
#                         result = result.replace("```","")

#                         f.write(result)
#             print(f"完成第{i}次")
#         # if i == 20:
#         #     break
#         # break


if __name__ == "__main__":
    # getSkill()

    get_label()









