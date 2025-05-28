import json
import jsonlines
from tqdm import tqdm


# 需要转化的数据路径
data_path = "./data/DF/DF_step04.json"
# 转化后数据的保存路径
written_path = "./ft_data/DF/DF_instruction.json"


# 将指令转化为指令微调的形式
def instruction_reform(data_path, written_path):
    train_data = []
    
    with open(data_path, 'r', encoding='utf-8') as file:
        # 逐行读取
        for line in file:
            # 去掉行尾的换行符
            line = line.strip()
            # 解析 JSON 数据
            line = json.loads(line)
            for idx, i in enumerate(json.loads(line['instruction'])):
                # 构建新的数据格式
                new_data = {
                    "instruction": i['instruction'],
                    "input": line['rule'],
                    "output": i['output']
                }
                train_data.append(new_data)
    
    with open(written_path, 'w', encoding='utf-8') as f:
        json.dump(train_data, f, ensure_ascii=False, indent=4)


instruction_reform(data_path, written_path)

