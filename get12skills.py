# 根据职业大典所有技能，提取出来12类技能，然后再对每一个职业进行贴标签

from openai import OpenAI
import os
import json
import csv
import pandas as pd

from tqdm import tqdm

# 读取原始数据
origin_data = pd.read_csv(r'output.csv', index_col=None)

answer_style = """
{
    "职业代码": X,
    "职业名称": X,
    "职业说明": X,
    "职业任务": X,
    '设备操作使用类': X,
    '组织人员管理类': X,
    '专业知识技能类': X,
    '设备维护处理类': X,
    '生产加工处理类': X,
    '社交沟通协调类': X,
    '工程材料设计类': X,
    '健康护理康复类': X,
    '数据分析处理类': X,
    '市场销售服务类': X,
    '安全管理质控类': X,
    '工程项目管理类': X,
}
"""

# 创建OpenAI的api链接
# key = r'0000sk-t5Pc7liZ64RMDv9ogj7L7uB2sGyliaHSEYeS42ZoJrtiAkJI'
client = OpenAI(
    base_url='https://api.openai-proxy.org/v1',
    api_key=key
)

classes = """
    1设备操作使用类,
    2组织人员管理类,
    3专业知识技能类,
    4设备维护处理类,
    5生产加工处理类,
    6社交沟通协调类,
    7工程材料设计类,
    8健康护理康复类,
    9数据分析处理类,
    10市场销售服务类,
    11安全管理质控类,
    12工程项目管理类,
"""

# # 预热提问，告诉GPT它的任务是什么
# stream = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "一个善于提取各种文本信息的能手，将帮助我根据我提供的信息和对应的技能进行匹配"},
#         {"role": "user", "content": f"现在会给你提供某一职业信息的内容，现在有对应15种能力，每一种能力使用数字表示需要这项能力的程度。这15项能力分别是{ability}，现在需要根据我提供的信息，判断这个职业需要哪些能力，且能力需要达到哪一个程度。"},
#         {"role": "assistant", "content":f"好的，我明白了，我会在收到相关内容后进行分析，以{answer_style}的json格式数据回答”，请你给出相关信息"},
#         ],
#     stream=True,
# )
# # print(stream)
# # 输出结果
# for chunk in stream:
#     # print(chunk.choices[0])
#     if len(chunk.choices) != 0:
#         if chunk.choices[0].delta.content is not None:
            # print(chunk.choices[0].delta.content, end="") 



def getSkill():

    with tqdm(total=len(origin_data.index)) as pbar:
        for i in range(len(origin_data.index)):
            # 读取每一行的数据
            # data = origin_data[i]
            # if i < 1384:
            #     continue
            code = origin_data.iloc[i, 0]
            name = origin_data.iloc[i, 1]
            explain = origin_data.iloc[i, 2]
            task = origin_data.iloc[i, 3]


            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "一个善于提取各种文本信息的能手，将帮助我根据我提供的职业信息和对应的职业类别进行匹配"},
                    {"role": "user", "content":f"现在根据提供的信息：职业代码：{code},职业名称:{name},职业说明:{explain},职业任务:{task}，根据这些信息，匹配这个职业属于哪些类职业,现在有13类职业类型，分别是{classes}，现在需要根据我提供的信息，判断这个职业属于哪些类，如果属于则用1表示，不属于则用0表示，以{answer_style}的json格式数据回答”，严格遵照这一个格式执行。"},
                ],
                stream=True,
            )
            with open(f'ClassData/{i}.txt',mode='w',encoding='utf-8') as f:
            
                for chunk in stream:
                    if len(chunk.choices) != 0:
                        if chunk.choices[0].delta.content is not None:
                            # 写入表头
                            # writer.writeheader()
                            result = chunk.choices[0].delta.content
                            result = result.replace("json",'')
                            result = result.replace("```","")

                            f.write(result)
            # print(f"完成第{i}次")

            pbar.set_postfix({
                "Finish": i+1
            })
            pbar.update(1)
            # if i == 20:
            #     break
            # break


if __name__ == "__main__":
    getSkill()











