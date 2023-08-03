# utils
python实现的小工具，dy下载用户视频
python版本使用3.10

### 安装依赖

```
python -m pip install -r requirements.txt
```

### 运行

```
python ./main.py
```



### 打包

```
pyinstaller -F .\main.py
#添加额外依赖
pyinstaller --add-data 'ca.crt;seleniumwire' --add-data 'ca.key;seleniumwire' --onefile main.py
```