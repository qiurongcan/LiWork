import pandas as pd
import os
import json

base_file = r'Merge_label5'
files = os.listdir(base_file)
result = pd.DataFrame()
for fil in files:
    print(fil)
    f_path = os.path.join(base_file, fil)
    with open(f_path, encoding='utf-8') as f:
        data = json.loads(f.read())


    # 准备数据列表
    data_list = []

    # 遍历JSON数据，整理成适合DataFrame的格式
    for category, details in data.items():
        data_list.append({
                '技能类别': category,
                '技能名称': details['技能名称'],
                '技能次数': details['技能次数']
            })

    # 创建DataFrame
    df = pd.DataFrame(data_list)

    result = pd.concat([result, df], axis=0)

    # 保存为Excel文件
result.to_excel('skills111.xlsx', index=False)
    # break