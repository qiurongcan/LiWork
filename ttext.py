import csv
import os
import json

# 指定CSV文件路径
csv_file_path = 'output.csv'





base_path = f'outdata'

file_names = os.listdir(base_path)
# 将JSON数据转换为CSV
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["职业代码", "职业名称", "职业说明", "职业任务"])
    i = 0 
    for file_n in file_names:
        try:
            path = os.path.join(base_path, file_n)
            with open(path, encoding='utf-8') as f:
                text = f.read()

            # 写入表头
            data = json.loads(text)
            if i == 0:
                writer.writeheader()
            
            # 写入数据行
            writer.writerows(data)
            i = i + 1
            print(f'{file_n} is finished')
        
        except:
            print(print(f'{file_n} is FALSE!!!'))
    
print(f"数据已成功转换为CSV并保存在 {csv_file_path}")
