# 获取技能和技能影响程度
# 根据职业匹配相应的13个技能有哪些
from openai import OpenAI
import os
import json
import csv
import pandas as pd

# 读取原始数据
origin_data = pd.read_csv(r'output.csv', index_col=None)

answer_style = """
{
    "职业代码": X,
    "职业名称": X,
    "职业说明": X,
    "职业任务": X,
    '掌握工作技能时间': X,
    '能力和技能使用状况': X,
    '专业技术资格数量': X,
    '专业技术资格等级': X,
    '使用新技术能力': X,
    '阅读能力': X,
    '与人打交道频率': X,
    '合作能力': X,
    '社交机会': X,
    '外语能力': X,
    '普通话能力': X,
    '管理能力': X,
    '快速反应思考或脑力劳动频率': X,
    '繁重体力劳动频率': X,
    '频繁移动身体位置频率': X,
}
"""

# 创建OpenAI的api链接
key = r'sk-t5Pc7liZ64RMDv9ogj7L7uB2sGyliaHSEYeS42ZoJrtiAkJI'
client = OpenAI(
    base_url='https://api.openai-proxy.org/v1',
    api_key=key
)

ability = """
能力1-掌握工作技能时间：根据提供的这份职业信息，判断这个职业掌握这项能力的时间，其中，0:不需要；1:一周左右；2:不到一个月；3:一个月到三个月; 4:三个月以上
能力2-专业技能使用状况：根据提供的这份职业信息，判断这个职业需要使用高级专业技能的程度：0:不需要；1:不太需要；2:一般需要；3:比较需要；4:非常需要
能力3-专业技术资格数量：根据提供的这份职业信息，判断这个职业需要的专业技术资格数量，其中，0:不需要；1:1个；2:2个；3:3个；4:4个或更多
能力4-专业技术资格等级：根据提供的这份职业信息，判断这份职业需要的专业技术资格等级，其中，0:不需要；1:初级(国家职业资格五级)，2：中级(国家 职业资格四级)，3：高级(国家职业资格三级)，4：技师(国家职业资格二级)
能力5-使用新技术能力：根据提供的这份职业信息，判断这份职业需要使用当前最新技术的要求，其中，0:不需要；1:不太需要；2:一般需要；3:比较需要；4:非常需要
能力6-阅读能力：根据提供的这份职业信息，判断这份职业需要阅读能力的要求，其中，0:不需要；1:不太需要；2:一般需要；3:比较需要；4:非常需要
能力7-与人打交道频率：根据提供的这份职业信息，判断这份职业需要与人打交道的频率，其中，0:不需要；1:不太需要；2:一般需要；3:比较需要；4:非常需要
能力8-合作能力：根据提供的这份职业信息，判断这份职业需要与人合作的能力，其中，0:不需要；1:不太需要；2:一般需要；3:比较需要；4:非常需要
能力9-社交机会：根据提供的这份职业信息，判断这份职业可能参与的社交程度，其中，0:不需要；1:不太需要；2:一般需要；3:比较需要；4:非常需要
能力10-外语能力：根据提供的这份职业信息，判断这份职业需要外语的能力程度，其中，0:不需要；1:不太需要；2:一般需要；3:比较需要；4:非常需要
能力11-普通话能力：根据提供的这份职业信息，判断这份职业需要流利普通话进行频繁交流的程度，其中，0:不需要；1:不太需要；2:一般需要；3:比较需要；4:非常需要
能力12-管理能力：根据提供的这份职业信息，判断这份职业需要管理能力的程度，其中，0:不需要；1:不太需要；2:一般需要；3:比较需要；4:非常需要
能力13-快速反应思考或脑力劳动频率：根据提供的这份职业信息，判断这份职业需要快速反应思考或脑力劳动频率，其中，0:不需要；1:很少；2:有时；3:经常；4:非常频繁
能力14-繁重体力劳动频率：根据提供的这份职业信息，判断这份职业需要繁重体力劳动频率，其中，0:不需要；1:很少；2:有时；3:经常；4:非常频繁
能力15-频繁移动身体位置频率：根据提供的这份职业信息，判断这份职业需要频繁移动身体位置频率，其中，0:不需要；1:很少；2:有时；3:经常；4:非常频繁
"""

# 预热提问，告诉GPT它的任务是什么
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "一个善于提取各种文本信息的能手，将帮助我根据我提供的信息和对应的技能进行匹配"},
        {"role": "user", "content": f"现在会给你提供某一职业信息的内容，现在有对应15种能力，每一种能力使用数字表示需要这项能力的程度。这15项能力分别是{ability}，现在需要根据我提供的信息，判断这个职业需要哪些能力，且能力需要达到哪一个程度。"},
        {"role": "assistant", "content":f"好的，我明白了，我会在收到相关内容后进行分析，以{answer_style}的json格式数据回答”，请你给出相关信息"},
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



def getSkill():
 
    for i in range(len(origin_data.index)):
        # 读取每一行的数据
        # data = origin_data[i]
        if i < 1852:
            continue
        code = origin_data.iloc[i, 0]
        name = origin_data.iloc[i, 1]
        explain = origin_data.iloc[i, 2]
        task = origin_data.iloc[i, 3]


        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content":f"现在根据提供的信息：职业代码：{code},职业名称:{name},职业说明:{explain},职业任务:{task}，根据这些信息，匹配这类职业需要哪些技能,根据给你提供的职业信息的内容，现在有对应15种能力，每一种能力使用数字表示需要这项能力的程度。这15项能力分别是{ability}，现在需要根据我提供的信息，判断这个职业需要哪些能力，且能力需要达到哪一个程度。以{answer_style}的json格式数据回答”，严格遵照这一个格式执行，只保存列表。"},
            ],
            stream=True,
        )
        with open(f'AbilityData/{i}.txt',mode='w',encoding='utf-8') as f:
        
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
        # if i == 20:
        #     break
        # break


if __name__ == "__main__":
    getSkill()






