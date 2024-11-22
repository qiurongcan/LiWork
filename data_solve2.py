import pandas as pd 
import ast
from collections import defaultdict


df = pd.read_excel(r'12类数据.xlsx', index_col=None)

# print(len(df.index))
# 合并标签

result_dict = defaultdict(list)

for i in range(len(df.index)):
    
    print(df.iloc[36, 1])
    # if df.iloc[i,1] == None:
    #     continue
    # print((df.iloc[i,1]))
    if type(df.iloc[i,1]) == type(df.iloc[36, 1]):
        continue
    skills_list = ast.literal_eval(df.iloc[i,1])
    # print(df.iloc[i,1])
    if i < 40 :
        result_dict['设备操作使用类'].extend(skills_list)

    
    elif i >=40 and i <= 61:
        result_dict['组织人员管理类'].extend(skills_list)
        
        
    elif i >= 62 and i <= 80:
        result_dict['专业知识技能类'].extend(skills_list)


    elif i >= 81 and i <= 109:
        result_dict['设备维护处理类'].extend(skills_list)
    # skills_list = list(df.iloc[i, 1])
    # print((skills_list))

    elif i > 109 and i <= 130:
        result_dict['生产加工处理类'].extend(skills_list)

    
    elif i > 130 and i <= 150:
        result_dict['社交沟通协调类'].extend(skills_list)

    
    elif i > 150 and i <= 178:
        result_dict['工程材料设计类'].extend(skills_list)


    elif i > 178 and i <= 195:
        result_dict['健康护理康复类'].extend(skills_list)


    elif i > 195 and i <= 212:
        result_dict['数据分析处理类'].extend(skills_list)

    elif i > 212 and i <= 235:
        result_dict['市场销售服务类'].extend(skills_list)

    elif i > 235 and i <= 253:
        result_dict['安全管理质控类'].extend(skills_list)

    elif i > 253 and i <= 280:
        result_dict['工程项目管理类'].extend(skills_list)



result_df = pd.DataFrame.from_dict(result_dict, orient='index').T
result_df.to_excel("Merge12.xlsx", index=False)
