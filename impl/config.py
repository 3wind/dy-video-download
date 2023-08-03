import yaml
import os

# 定义每次读取的行数
yaml_path = os.path.join(os.getcwd(), "config.yaml")
with open(yaml_path, "r", encoding="utf-8") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    print('---config---')
    print(data)
    G_LOAD_TYPE = data['load-type']
    G_URL = data['url']
    G_ID = data['id']
    G_SAVE_PATH = data['save-path']