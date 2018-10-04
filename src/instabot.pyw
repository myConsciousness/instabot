from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.parse
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Webdriver
browser = webdriver.Chrome()

#URL

loginURL = "https://www.instagram.com/" #ログインする際のページ
tagSearchURL = "https://www.instagram.com/explore/tags/{}/?hl=ja" #.format()で{}の中の値を入れられるようになっている

tagName = "partying" #タグの名前 #よみうりランド

#ここには書くページのSelectorを選ぶ。x-pathもしくはcss selector
loginPath = '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a' #xpath @https://www.instagram.com/
usernamePath = '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[1]/div/div[1]/input' #xpath @https://www.instagram.com/
passwordPath = '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/div[1]/input' #xpath @https://www.instagram.com/

notNowPath = '//*[@id="react-root"]/div/div[2]/a[2]'

mediaSelector = '#react-root > section > main > article > div.EZdmt' #表示されているメディアのwebelement @https://www.instagram.com/explore/tags/%E3%82%88%E3%81%BF%E3%81%86%E3%82%8A%E3%83%A9%E3%83%B3%E3%83%89/?hl=ja
likeXpath = '/html/body/div[3]/div/div[2]/div/article/div[2]/section[1]/span[1]/button/span'
nextPagerSelector = 'a.coreSpriteRightPaginationArrow' #次へボタン

username = ""
password = ""

mediaList = []

likedCounter = 0

if __name__ == '__main__':

    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    #Login
    browser.get(loginURL)
    time.sleep(3)
    browser.find_element_by_xpath(loginPath).click()
    time.sleep(3)
    #usernameField = browser.find_element_by_xpath(usernamePath)

    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))).send_keys(username)
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']"))).send_keys(password)

    browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]').click()

    #Finished logging in. now at
    time.sleep(3)
    encodedTag = urllib.parse.quote(tagName) #普通にURLに日本語は入れられないので、エンコードする
    encodedURL = tagSearchURL.format(encodedTag)
    print("encodedURL:{}".format(encodedURL))
    browser.get(encodedURL)

    #Finished tag search. now at https://www.instagram.com/explore/tags/%E8%AA%AD%E5%A3%B2%E3%83%A9%E3%83%B3%E3%83%89/?hl=ja
    time.sleep(3)
    browser.implicitly_wait(10)

    #写真を取得してクリックする
    mediaList = browser.find_elements_by_css_selector(mediaSelector)
    mediaCounter = len(mediaList)
    print("Found {} media".format(mediaCounter))

    for media in mediaList:
        media.click()

        while True:
            try:
                time.sleep(3)
                browser.find_element_by_xpath(likeXpath).click()
                browser.implicitly_wait(10)
                likedCounter += 1
                print("liked {} of {}".format(likedCounter,mediaCounter))
                browser.find_element_by_css_selector(nextPagerSelector).click()
            except:
                break #もう次へボタンが存在しない場合、エラーをはくのでそこで終了
        break #for文自体も終了させる

    print("You liked {} media".format(likedCounter))
