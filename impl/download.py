import requests
import os
from impl.config import *
import re

# 创建输出目录
def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
        print('目录：【', dir, '】创建成功')


pattern = re.compile('["!@#$%^&*()_+[\]\{\};:,./<>?\|\`\~\-\=\n]')
# 下载并保存视频
def download_video(url, name, path):
    file_path = os.path.join(path,  re.sub(pattern, '', name) + '.mp4')
    print('---download---')
    if (os.path.exists(file_path)):
        print('{name}------已存在！'.format(name=file_path))
        return
    # 发送网络请求并获取响应
    response = requests.get(url, stream=True)
    # 检查响应状态码是否为200
    if response.status_code == 200:
        # 打开本地文件并写入响应内容
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

        print('{name}------下载完成！'.format(name=file_path))
    else:
        print('{name}------下载失败！'.format(name=name))