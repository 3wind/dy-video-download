from seleniumwire import webdriver
from io import BytesIO
import gzip
import time
import brotli
import json
from bs4 import BeautifulSoup
from impl.config import *
from impl.download import make_dir, download_video

def load():
    if G_LOAD_TYPE == 'id':
        load_id_video(G_ID)
    elif G_LOAD_TYPE == 'url':
        load_user_videos(G_URL)

def load_id_video(id): 
    make_dir(G_SAVE_PATH)
    download_video(get_url_by_id(id), id, G_SAVE_PATH)

def get_url_by_id(id):
  return 'https://aweme.snssdk.com/aweme/v1/play/?video_id={id}&line=0&ratio=1080p&media_type=4&vr_type=0&improve_bitrate=0&is_play_url=1&is_support_h265=0&source=PackSourceEnum_PUBLISH'.format(id=id)

def load_user_videos(user_url):
    print('---load start---')
    
    # 页面访问配置
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')

    # 停止DevTools在ws：//127.0.0.1上侦听
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # 初始化Chrome浏览器驱动
    driver = webdriver.Chrome(options=options)

    # 拦截response处理函数
    def interceptor_response(request, response):
        if response and request.url.find("/aweme/v1/web/aweme/post/?device_platform=webapp") != -1:
            if response.status_code != 200:
                return
            else:
                res_body = get_rsp_body(response)
                device_platform_data_download(res_body)
            return

        # if  response and request.url.find("https://www.douyin.com/user/") != -1:
        #     if response.status_code != 200:
        #         return
        #     else:
        #         res_body = get_rsp_body(response)
        #         user_data_download(res_body)
        #     return

    # 设置拦截
    driver.response_interceptor  = interceptor_response

    # 打开网页
    driver.get(user_url)

    # 建立等待策略 
    # driver.implicitly_wait(2)

    print('===访问===')
    print(driver.title)
    print('=========')

    # 打开30分钟，程序执行完成后避免直接关闭
    time.sleep(30 * 60)
    # 关闭浏览器驱动
    driver.quit()

# 返回数据解码
def get_rsp_body(response):
        # print("Content-Type:", response.headers['Content-Type'])
        # print("Content-Encoding:", response.headers['Content-Encoding'])
        data = None
        contentEncoding = response.headers['Content-Encoding']
        
        if contentEncoding and any(t in contentEncoding for t in ['br']):
            data = brotli.decompress(response.body).decode('utf-8')
        elif contentEncoding and any(t in contentEncoding for t in ['gzip']):
            buff = BytesIO(response.body)
            data = gzip.GzipFile(fileobj=buff).read().decode('utf-8')
        else:
            data = response.body.decode('utf-8')

        return data
        

def device_platform_data_download(data_list):
    make_dir(G_SAVE_PATH)
    # 获取下载地址
    if data_list:
        try:
            aweme_list = json.loads(data_list)['aweme_list']
            for item in aweme_list:
                url = item['video']['play_addr']['url_list'][-1]
                name = item['desc']
                if len(name) > 16: name = name[:16]
                # url = play_addr['url_list'][-1]
                # name = play_addr['uri'].split('/')[-1]

                download_video(url, name, G_SAVE_PATH)
        except (IndexError, IndentationError, AttributeError):
            print("INFO：aweme_list处理失败", IndexError, IndentationError, AttributeError)
    return

def user_data_download(data):
    # 使用BeautifulSoup解析HTML页面
    soup = BeautifulSoup(data, 'html.parser')
    # 查找id为RENDER_DATA的script标签，并获取其内容
    render_data_script = soup.find('script', {'id': 'RENDER_DATA'})
    print('=============')
    print(render_data_script.string)
    print('=============')