import time
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def is_exist_z(web):
    try:
        txt = web.find_element(By.XPATH, './div/div[1]/div[2]/p[1]/a').text
        if '展开' in txt:
            return True
        else:
            return False
    except:
        return False

if __name__ == "__main__":
    url = 'https://s.weibo.com/'
    web = Chrome('E:\FangLin\Taobao\chromedriver.exe')
    web.get(url)
    time.sleep(10)

    topic = input('请输入话题：') #话题的形式必须是#上海疫情#，必须用双#号括起来
    time.sleep(3)
    search_input = web.find_element(By.XPATH, '//*[@id="pl_homepage_search"]/div/div[2]/div/input')
    search_input.send_keys(topic)
    search_button = web.find_element(By.XPATH, '//*[@id="pl_homepage_search"]/div/div[2]/button')
    search_button.click()
    time.sleep(5)
    #hot_topic_link = web.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/ul/li[1]/a')
    #hot_topic_link.click()

    page_count = 1
    data = []
    while page_count <= 2:  # 自定义爬取的页码，这里定义为2
        print(f"开始爬取第 {page_count} 页数据")
        count = 0
        while count < 5:
            web.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(3)
            count += 1

        div_list = web.find_elements(By.XPATH, '//*[@id="pl_feedlist_index"]/div[4]/div')
        for div in div_list:
            user_name = div.find_element(By.XPATH,'./div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/div[@class="info"]/div[2]/a').text
            tran = div.find_element(By.XPATH, './div[@class="card"]/div[@class="card-act"]/ul/li[1]').text
            comment = div.find_element(By.XPATH, './div[@class="card"]/div[@class="card-act"]/ul/li[2]').text
            praise = div.find_element(By.XPATH, './div[@class="card"]/div[@class="card-act"]/ul/li[3]').text
            date = div.find_element(By.XPATH,'./div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/div[@class="from"]/a').text
            user_url = div.find_element(By.XPATH,'./div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/div[@class="info"]/div[2]/a').get_attribute('href')
            tag = user_name + '的微博视频'

            detail = ""
            if is_exist_z(div):
                detail_page_content_url = div.find_element(By.XPATH, './div/div[1]/div[2]/p[1]/a').get_attribute('href')
                js = "window.open('" + detail_page_content_url + "');"
                web.execute_script(js)
                time.sleep(5)
                web.switch_to.window(web.window_handles[1])
                time.sleep(5)
                detail = web.find_element(By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/article/div[2]/div/div/div').text
                with open('ciyun.txt', 'a', encoding='utf-8') as file:
                    file.write(detail + '\n')
                web.close()
                web.switch_to.window(web.window_handles[0])
            else:
                detail = div.find_element(By.XPATH,'./div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/p').text

            try:
                video_length_element = div.find_element(By.XPATH,'./div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/div[3]/div[@class="thumbnail"]/a/div/div/button')
                video_length_element.click()
                time.sleep(2)  # Let the video load and display the duration
                video_text_list = div.find_elements(By.XPATH,'./div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/div[3]/div[@class="thumbnail"]')

                for infor in video_text_list:
                    video_text = infor.text
                    lines = video_text.split("\n")
                    video_length = lines[5]
            except:
                video_length = 'no video'

            us = "window.open('" + user_url + "');"
            web.execute_script(us)
            time.sleep(5)
            web.switch_to.window(web.window_handles[1])
            time.sleep(5)
            try:
                ip = web.find_element(By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[3]/div/div/div[1]/div[3]').text
            except:
                ip = 'no ip'

            try:
                fans = web.find_element(By.XPATH,
                                        '//*[@id="app"]/div[2]/div[2]/div[2]/main/div[1]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/a[1]/span/span').text
            except:
                fans = 'no fans'

            try:
                element = web.find_element(By.CSS_SELECTOR,'#app > div.woo-box-flex.woo-box-column.Frame_wrap_3g67Q > div.woo-box-flex.Frame_content_3XrxZ.Frame_noside1_3M1rh > div.Frame_main_3Z_V0 > main > div > div > div:nth-child(2) > div:nth-child(1) > div.woo-panel-main.woo-panel-top.woo-panel-right.woo-panel-bottom.woo-panel-left.Card_wrap_2ibWe.Card_bottomGap_2Xjqi > div.woo-box-flex.woo-box-alignStart.ProfileHeader_box1_1qC-g > div.woo-box-item-flex > div.woo-box-flex.woo-box-alignCenter.ProfileHeader_h3_2nhjc > span:nth-child(2) > svg')
                attribute_value = element.get_attribute('class')
                start_index = attribute_value.find('--') + 2
                end_index = attribute_value.find('"', start_index)
                gender = attribute_value[start_index:end_index] + 'e'
            except:
                gender = 'no gender'
            web.close()
            web.switch_to.window(web.window_handles[0])

            data.append([user_name, tran, comment, praise, date, user_url, ip, fans, gender, detail, video_length, tag])

        next_page_button = web.find_element(By.XPATH, '//a[@class="next"]')
        next_page_button.click()
        time.sleep(5)

        page_count += 1

    web.quit()

    # Save the data to an Excel file
    df = pd.DataFrame(data, columns=['用户名', '转发', '评论', '点赞', '发博时间', '个人微博链接', 'IP地址', '粉丝数量', '性别', '内容', '视频时长', '视频标签'])
    df.to_excel('weibo.xlsx', index=False)
