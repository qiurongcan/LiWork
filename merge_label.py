# 用于合并文档中类似的标签

# 根据职业匹配相应的13个技能有哪些
from openai import OpenAI
import os
import json
import csv
import pandas as pd

# 读取原始数据
origin_data = pd.read_excel(r'准备文档_大语言识别全部技能 20241116.xlsx', index_col=None)

# 创建OpenAI的api链接
key = r'sk-t5Pc7liZ64RMDv9ogj7L7uB2sGyliaHSEYeS42ZoJrtiAkJI'
client = OpenAI(
    base_url='https://api.openai-proxy.org/v1',
    api_key=key
)

# 使用gpt-4o
ans_style = """
{
    "设备操作类": {
        "技能名称": [
            "设备操作",
            "操作设备",
            "操作设备的技能",
            "专用设备操作",
            "机械设备操作",
            "操作控制系统/设备",
            "设备操作技能"
        ],
        "技能次数": 261
    },
    "沟通能力类": {
        "技能名称": [
            "沟通协调能力",
            "沟通能力",
            "客户沟通",
            "沟通与协调能力",
            "沟通与协商能力"
        ],
        "技能次数": 87
    },

}
"""

def getSkill():
 
    ask_str = ""
    for i in range(len(origin_data.index)):
        # 读取每一行的数据
        
        skill = origin_data.iloc[i, 0]
        frequency = origin_data.iloc[i, 1]
        msg = f'技能名称：{skill}, 技能次数：{frequency} \n'
        ask_str += msg
        if i % 151 == 150:
            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content":f"现在根据提供的信息：{ask_str},判断在提供的这些技能中，哪些技能可以归为一类，如果这些技能可以归为一类，同时合并他们的频次。例如设备操作，操作设备、操作设备的技能可以认为是同一类的技能，如果提供的技能中不能和其他技能合并为一类的，则单独为一类技能，并以json格式数据回答,回答格式如{ans_style}所示”；只需要json格式数据。"},
                ],
                stream=True,
            )
            with open(f'Merge_label3/{i}.txt',mode='w',encoding='utf-8') as f:
            
                for chunk in stream:
                    if len(chunk.choices) != 0:
                        if chunk.choices[0].delta.content is not None:
                            # 写入表头
                            # writer.writeheader()
                            result = chunk.choices[0].delta.content
                            result = result.replace("json",'')
                            result = result.replace("```","")

                            f.write(result)
                print(f"完成第{i}次")
                ask_str = ''
        # break
    stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content":f"现在根据提供的信息：{ask_str},需要判断在提供的这些技能中，是否存在技能名称相同、技能名称类似的技能，对他们进行合并，同时合并频次。例如设备操作，操作设备、操作设备的技能可以认为是相同的技能，则可以合并，并以json格式数据回答”；只需要json格式数据。"},
                ],
                stream=True,
            )
    with open(f'Merge_label3/{i}.txt',mode='w',encoding='utf-8') as f:
    
        for chunk in stream:
            if len(chunk.choices) != 0:
                if chunk.choices[0].delta.content is not None:
                    # 写入表头
                    # writer.writeheader()
                    result = chunk.choices[0].delta.content
                    result = result.replace("json",'')
                    result = result.replace("```","")

                    f.write(result)
        print(f"完成第{i}次")


if __name__ == "__main__":
    getSkill()








