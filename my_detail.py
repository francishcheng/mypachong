from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
from bs4 import BeautifulSoup as bs
import time

import io
import re
from my_imgpro import add_bgc

def get_detail(sql, n_code, s_time, rc_id):
    ############
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    path = '/usr/bin/chromedriver'

    options.add_argument('--no-sandbox') 
    # ###

    ###
    #browser = webdriver.Chrome(executable_path=path,chrome_options=options)
    while True:
        try:
            browser = webdriver.Chrome(executable_path=path,chrome_options=options)
        except:
            print("something went wrong, retrying...")
            time.sleep(2)
            continue
        break
    wait = WebDriverWait(browser, 10)

    url = 'https://www.helmenyun.cn/index.php/DataManage/data_detail?sql={sql}&SNcode={SNcode}&sTime={sTime}&RecordID={RecordID}'.format(sql=sql, SNcode=n_code, sTime=s_time, RecordID=rc_id)
    print(url)
    ##############


    ####
    #browser.get(url)
    while True:
        try:
            browser.get(url)
        except:
            print("network went wrong, retrying...")
            time.sleep(2)
            continue
        break

    ####
    time.sleep(2.5)
    #
    browser.add_cookie({'name':'PHPSESSID', 'value': '6q9o2jdlut9qsst35dmpfl6h40'})
    browser.add_cookie({'name':'username', 'value':'Yingtianwanwu'})
    browser.add_cookie({'name':'pwd', 'value':'yingtianwanwu0122'})
    while True:
        try:
            browser.get(url)
        except:
            print("network went wrong, retrying...")
            time.sleep(2)
            continue
        break

 
    #browser.get(url)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'data-bight')))
    time.sleep(1.5)
    JS = 'return  document.getElementsByTagName("canvas")[0].toDataURL("image/png");'
    im_info = browser.execute_script(JS)
    im_base64 = im_info.split(',')[1]

    im_bytes = base64.b64decode(im_base64)
    buf = io.BytesIO(im_bytes)
    im = add_bgc(buf)

    im.convert("RGB").save(r'/var/www/html/img/'+str(rc_id)+'.jpg')
    print('image saved')
    #with open('/var/www/html/img/'+rc_id+'.png','wb') as f:  #保存图片到本地
    #    f.write(im_bytes)

    js = "return document.documentElement.outerHTML"




    html = browser.execute_script(js)
    soup = bs(html, 'lxml')
    ##检测时间
    data_header = soup.find('div', {'class':'data-header'}) # 主数据区域


    test_time = data_header.find('span', text=re.compile('\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d')).text

    batch_name = data_header.find('span', {'class':'SNcode'}).text

    gender_pattern = re.compile('性别：(.*?)出生年月', re.S)
    gender = re.search(gender_pattern, data_header.text).group(1).strip()

    birth_pattern = re.compile('出生年月：(.*?)设备投放地', re.S)
    birth = re.search(birth_pattern, data_header.text).group(1).strip()

    facility_pattern = re.compile('设备投放地：(.*?)详细地址', re.S)
    facility = re.search(facility_pattern, data_header.text).group(1).strip()

    location_pattern = re.compile('详细地址：(.*?)检测结果', re.S)
    location = re.search(location_pattern, data_header.text).group(1).strip()

    test_result = data_header.find_all('div', {'class':'row'})[3:]
    test_result = [i.text.strip() for i in test_result]

    curve = soup.find('div', {'class':'data-bight'}).find_all('span')
    curve = [i.text for i in curve]
    curve = ' '.join(curve)

    browser.quit()
    return test_time, batch_name, gender, birth, facility, location, test_result, curve

if __name__ == '__main__':
    pass
