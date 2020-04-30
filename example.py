from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import random
import telegram
from datetime import datetime
from settings import INSTA_LOGIN, INSTA_PASS, BOT_TOKEN


today = datetime.utcnow().strftime("%Y-%m-%d%H:%M:%S")

bot = telegram.Bot(token=BOT_TOKEN,
                   base_url='https://telegg.ru/orig/bot')

block1 = ['3/3', '4/4', '5/5']
block2 = ['лайки', 'комментарии', 'комменты', 'ВЗ лайки', 'лайки или комментарии']
block3 = ['сразу', 'все взаимно', 'сразу сейчас']
#block4 = ['❤']

# for i in range(100):
#     print(f'{random.choice(block1)} {random.choice(block2)} {random.choice(block3)} {random.choice(block4)}')

browser = webdriver.Chrome()
#логинимся
browser.get("https://www.instagram.com")
sleep(2)
browser.find_element_by_xpath('//section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input').send_keys(INSTA_LOGIN)
browser.find_element_by_xpath('//section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input').send_keys(INSTA_PASS)
browser.find_element_by_xpath('//section/main/article/div[2]/div[1]/div/form/div[4]').click()
sleep(3)

f = open('subs.txt', 'r')
subc = [line.strip() for line in f]
f.close()


def set_urls(persons):
    urls = set()
    for pers in persons[:30]:
        time = pers.find_element_by_tag_name('time').get_attribute('datetime')
        time = time.split('T')[0] + time.split('T')[1].split('.')[0]
        if time > today:
            url = pers.find_element_by_tag_name('a').get_attribute('href')
            urls.add(url)
            #проверяем есть ли коммент
            if 'прокомментировал' in pers.text:
                f = open('comment.txt', 'r')
                comment = [line.strip() for line in f]
                f.close()
                if url not in comment:
                    print(pers.text)
                    bot.send_message(
                        chat_id=775257189,
                        text=f'{pers.text}'
                    )
                    f = open('comment.txt', 'a')
                    f.write(url + '\n')
                    f.close()
    return urls


#ставим лайки
def like():
    browser.get("https://www.instagram.com/grigoriy_kuzin")
    sleep(3)
    browser.find_element_by_xpath('//section/nav/div[2]/div/div/div[3]/div/div[4]/a').click()
    sleep(3)
    persons = browser.find_elements_by_xpath('//section/nav/div[2]/div/div/div[3]/div/div[4]/div/div/div[2]/div[2]/div/div/div/div/div/div[2]')
    urls = set_urls(persons)
    # проверяем есть ли в списке подписок
    # проверяем подписки
    f = open('temp.txt', 'r')
    temp = [line.strip() for line in f]
    f.close()
    for url in urls:
        print(url)
        if url not in subc:
            if url not in temp:
                f = open('temp.txt', 'a')
                f.write(url + '\n')
                f.close()
                browser.get(url)
                sleep(3)
                try:
                    browser.find_element_by_xpath(
                        '//section/main/div/div/article/div/div/div[1]/div[1]').click()
                except NoSuchElementException:
                    continue
                sleep(2)
                browser.find_element_by_xpath(
                    '//html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button').click()
                sleep(1)
                try:
                    browser.find_element_by_xpath('//html/body/div[4]/div[1]/div/div/a').click()
                except NoSuchElementException:
                    continue
                sleep(1)
                for i in range(5):
                    browser.find_element_by_xpath(
                        '//html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button').click()
                    sleep(1)
                    try:
                        browser.find_element_by_xpath('//html/body/div[4]/div[1]/div/div/a[2]').click()
                    except NoSuchElementException:
                        break
                    sleep(1)
#оставляем комментарии
while True:
    #оставляем комментарии
    browser.get('https://www.instagram.com/p/BLasj3qh8AP/')
    sleep(2)
    browser.find_element_by_xpath('//section/main/div/div/article/div[2]/section[3]/div/form/textarea').click()
    sleep(2)
    browser.find_element_by_xpath('//section/main/div/div/article/div[2]/section[3]/div/form/textarea')\
        .send_keys(f'{random.choice(block1)} {random.choice(block2)} {random.choice(block3)}')
    sleep(2)
    browser.find_element_by_xpath('//section/main/div/div/article/div[2]/section[3]/div/form/button').click()
    sleep(60)
    like()
    sleep(60)
    like()
    sleep(180)
    print('спим')
# while True:
#     like()
#     print('спим')
#     sleep(10)

#проверяем последние действия и записываем в список




# browser.find_element_by_xpath('//html/body/div[4]/div/div/div[3]/button[2]').click()
# sleep(2)
#
# browser.get('https://www.instagram.com/khnychenkovladislav/')
# sleep(2)


