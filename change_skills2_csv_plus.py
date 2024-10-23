import csv
import os
import json

# 指定CSV文件路径
csv_file_path = '15ability_detect.csv'

base_path = f'AbilityData'

file_names = os.listdir(base_path)
# 将JSON数据转换为CSV
with open(csv_file_path, mode='w', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["职业代码", "职业名称", "职业说明", "职业任务", '掌握工作技能时间', '能力和技能使用状况','专业技术资格数量', '专业技术资格等级', '使用新技术能力', '阅读能力', '与人打交道频率', '合作能力', '社交机会', '外语能力', '普通话能力', '管理能力', '快速反应思考或脑力劳动频率', '繁重体力劳动频率', '频繁移动身体位置频率'])
    i = 0 
    for file_n in file_names:
    # for k in range(len(file_names)):
        try:
            # path = os.path.join(base_path, f'{k}.txt')
            path = os.path.join(base_path, file_n)
            with open(path, encoding='utf-8') as f:
                text = f.read()
                # print(text)

            # 写入表头
            data = json.loads(text)
            # print(type(data))
            # print(data)
            if i == 0:
                writer.writeheader()
            
            # 写入数据行
            # print(type(data))
            writer.writerow(data)
            # print("---")
            
            # print(f'{file_n} is finished')
            i = i + 1
            # break
        
        except:
            i = i + 1
            print(f'{file_n} is False')
            # print(f'{k}.txt is FALSE!!!')
        
        # break
    
print(f"数据已成功转换为CSV并保存在 {csv_file_path}")
