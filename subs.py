#Собираем подписчиков в файл

from time import sleep
from selenium import webdriver
from settings import INSTA_LOGIN, INSTA_PASS

browser = webdriver.Chrome()
#логинимся
browser.get("https://www.instagram.com")
sleep(2)
browser.find_element_by_xpath('//section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input').send_keys(INSTA_LOGIN)
browser.find_element_by_xpath('//section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input').send_keys(INSTA_PASS)
browser.find_element_by_xpath('//section/main/article/div[2]/div[1]/div/form/div[4]').click()
sleep(3)
browser.get("https://www.instagram.com/grigoriy_kuzin")
sleep(3)

#прокручиваем список подписок

browser.find_element_by_xpath('//section/main/div/header/section/ul/li[2]/a').click()
sleep(2)

element = browser.find_element_by_xpath('/html/body/div[4]/div/div[2]')

browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %6, element)
sleep(2)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %4, element)
sleep(2)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %3, element)
sleep(2)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %2, element)
sleep(2)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %1.4, element)

pers = []
t = 1
num_scroll = 0
#прокручиваем список подписчиков и добавляем в список
while True:
    num_scroll += 1
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
    sleep(t)
    if num_scroll == 27:
        print('!')
        #сохраняем в массив
        persons = browser.find_elements_by_xpath('//div/div[2]/ul/div/li/div/div/div/div/a[@title]')
        for i in persons:
            pers.append(str(i.get_attribute('href')))
        print(pers)
        print(len(pers))
        break

f = open('subs.txt', 'w')
for person in pers:
    f.write(person + '\n')
f.close()

browser.close()
