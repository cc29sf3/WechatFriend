# -*- coding: utf-8 -*-
import os
import selenium
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

from db import db
from util import Processor



FrameLayout='android.widget.FrameLayout'
LinearLayout='android.widget.LinearLayout'
View='android.view.View'
ListView='android.widget.ListView'
#微信图片保存路径
virtualPath='/storage/sdcard0/tencent/MicroMsg/WeiXin/'
#从手机pull到本地的图片保存路径
localPath='G:\\photo\\'
command='adb pull '+virtualPath+' '+localPath
rmCommand='adb shell rm '+virtualPath+'*'

class Moments():
    def __init__(self):
        """
        初始化
        """
        # 驱动配
        self.desired_caps = {
            'platformName': 'Android',
            'deviceName': '127.0.0.1:62001',
            'appPackage': 'com.tencent.mm',
            'appActivity': '.ui.LauncherUI',
            # 'udid': '8FS7N16715002301',
            'noReset': True
        }

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        self.wait = WebDriverWait(self.driver, 20)
        # self.client = MongoClient(MONGO_URL)
        # self.db = self.client[MONGO_DB]
        # self.collection = self.db[MONGO_COLLECTION]
        # 处理器
        self.processor = Processor()
        
        

    # def login(self):
    #     """
    #     登录微信
    #     :return:
    #     """
    #     # 登录按钮
    #     login = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/d75')))
    #     login.click()
    #     # 手机输入
    #     phone = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/hz')))
    #     phone.set_text('18621059247')
    #     sleep(1)
    #     # 下一步
    #     next = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/alr')))
    #     next.click()
    #     # 密码
    #     password = self.wait.until(
    #         EC.presence_of_element_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/hz"][1]')))
    #     password.set_text('gm@hubu.com')
    #     sleep(3)
    #     # 提交
    #     submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/alr')))
    #     submit.click()
    #     # 是否查看通讯录
    #     yesORnot = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/an2')))
    #     yesORnot.click()

    def enter(self):
        
        """
        进入朋友圈
        :return:
        """
        # 选项卡
        tab = self.wait.until(
            EC.presence_of_element_located((By.XPATH,
                                            '//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[3]')))

        # tab = self.driver.find_element(By.NAME('发现'))
        tab.click()
        # 朋友圈
        moments = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                  '//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.LinearLayout/com.tencent.mm.ui.mogic.WxViewPager/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ListView/android.widget.LinearLayout[1]')))
        moments.click()

        
    def getWechatNo(self,item):
        friendInfo = item.find_element_by_id('com.tencent.mm:id/dfg')
        friendInfo.click()
        sleep(0.5)
        tab = self.wait.until(
            EC.presence_of_element_located((By.XPATH,'//'+FrameLayout+'/'+FrameLayout+'/'+FrameLayout+'/'+FrameLayout+'/'+LinearLayout+'/'+FrameLayout+'/'+View+'/'+FrameLayout+'[2]/'+FrameLayout+'/'+LinearLayout+'/'+ListView+'/'+LinearLayout+'[1]')))
        print('进入朋友信息页面')
        wechatNo=tab.find_element_by_id('com.tencent.mm:id/ap7').get_attribute('text')[4:]
        self.driver.keyevent(4)
        return wechatNo

    def getFriendInfo(self,item):
        """
        获取每个朋友昵称，备注和头像
        /storage/sdcard0/tencent/MicroMsg/WeiXin/
        return (微信号，昵称，备注)
        """
        friendInfo = item.find_element_by_id('com.tencent.mm:id/dfg')
        friendInfo.click()
        tab = self.wait.until(
            EC.presence_of_element_located((By.XPATH,'//'+FrameLayout+'/'+FrameLayout+'/'+FrameLayout+'/'+FrameLayout+'/'+LinearLayout+'/'+FrameLayout+'/'+View+'/'+FrameLayout+'[2]/'+FrameLayout+'/'+LinearLayout+'/'+ListView+'/'+LinearLayout+'[1]')))
        print('进入朋友信息页面')
        #获取昵称备注
        wechatNo=tab.find_element_by_id('com.tencent.mm:id/ap7').get_attribute('text')[4:]
        nickname=''
        beizhu=''
        try:
            nickname=tab.find_element_by_id('com.tencent.mm:id/apt').get_attribute('text')[3:]
            beizhu=tab.find_element_by_id('com.tencent.mm:id/qj').get_attribute('text')
        except:
            nickname=tab.find_element_by_id('com.tencent.mm:id/qj').get_attribute('text')    
        print('获取昵称')
        #获取签名
        more = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/ge')))
        more.click()
        
        items=self.wait.until(
                EC.presence_of_all_elements_located(
                   (By.XPATH, '//*[@resource-id="com.tencent.mm:id/css"]')))
  
        autograph=''
        autographPath='//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[{x}]/android.widget.LinearLayout/android.widget.TextView[{y}]'
        for i in range(len(items)):
            print("xxxxxx")
            print(autographPath.format(x=i+1,y=1))
            textview1=self.wait.until(EC.presence_of_element_located((By.XPATH,autographPath.format(x=i+1,y=1))))
            if textview1.get_attribute('text')=='个性签名':
                textview2=self.wait.until(EC.presence_of_element_located((By.XPATH,autographPath.format(x=i+1,y=2))))
                autograph=textview2.get_attribute('text')
                break
        self.driver.keyevent(4)
        print('获取签名:'+autograph)
        #获取头像图片
        head=tab.find_element_by_id('com.tencent.mm:id/qi')
        head.click()
        img= self.wait.until(
            EC.presence_of_element_located((By.XPATH,'//'+FrameLayout+'/'+LinearLayout+'/android.widget.Gallery/android.widget.ImageView')))
        TouchAction(self.driver).long_press(img).perform()
        sleep(2)
        saveBtn=self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,'//'+FrameLayout+'/'+FrameLayout+'/'+FrameLayout+'/'+LinearLayout+'/'+LinearLayout+'/'+ListView+'/'+LinearLayout)))
        saveBtn.click()
        print('保存图片')
        
        os.system(command)
        
        files = os.listdir(localPath)
        print(len(files))
        if len(files)!=1:
            raise Exception('本地文件夹里头像数不唯一')
        filepath=localPath+files[0]
        f=open(filepath,"rb")
        b=f.read()
        f.close()

        conn = db()
        sql="INSERT INTO friendinfo (wechatNo,remark,nickname,handwrite,headimg) values (%s,%s,%s,%s,%s)"
        conn.cursor.execute(sql,(wechatNo,beizhu,nickname,autograph,b))
        conn.db.commit()
        conn.close()
        
        print('写头像')
        os.remove(filepath)
        os.system(rmCommand)
        print('删除文件')
        self.driver.keyevent(4)
        self.driver.keyevent(4)
        return wechatNo
        
    def getComment(self,item):
        result=''
        try:
            comments = item.find_elements_by_xpath('//android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.view.View')
            for comment in comments:
                result=result+' '+comment.get_attribute('name')
            return result
        except NoSuchElementException:
            try:
                comments = item.find_elements_by_xpath('//android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.LinearLayout/android.view.View')
                for comment in comments:
                    result=result+' '+comment.get_attribute('name')
                return result
            except NoSuchElementException:
                return ''

        
    def crawl(self):
        """
        爬取
        :return:
        """
        item = self.wait.until(
                EC.presence_of_all_elements_located(
                   (By.XPATH, '//*[@resource-id="com.tencent.mm:id/dkb"]')))[0]
        wechatNo = self.getFriendInfo(item)
        print('获取朋友信息完毕')
        # 记录重复的次数
        count = 0
        pageContent = ''
        while True:

            # 记录这一次的页面
            if pageContent == self.driver.page_source:
                count += 1
                if count % 3 == 0:
                    break
            else:
                pageContent = self.driver.page_source

            # 当前页面显示的所有状态
            items = self.wait.until(
                EC.presence_of_all_elements_located(
                   (By.XPATH, '//*[@resource-id="com.tencent.mm:id/dkb"]')))
            
            # 遍历每条状态
            for i,item in enumerate(items):
                try:
                    print(i)
                    # 昵称
                    name = item.find_element_by_id('com.tencent.mm:id/as6').get_attribute('text')
                    #wechatNo=self.getWechatNo(item)
                    # 正文
                    try:
                        contents = item.find_element_by_id('com.tencent.mm:id/dkf').get_attribute('text')
                        contents = self.processor.clean(contents)
                    except NoSuchElementException:
                        contents = ''
                    # 日期
                    try:
                        date = item.find_element_by_id('com.tencent.mm:id/dfw').get_attribute('text')
                        # 处理日期
                        date = self.processor.date(date)
                    except NoSuchElementException:
                        date = ''
                    # 点赞
                    try:
                        zan = item.find_element_by_id('com.tencent.mm:id/djz').get_attribute('text')
                        zan = self.processor.clean(zan)
                    except NoSuchElementException:
                        zan = ''
                    # 评论
                    comments=self.getComment(item)
                    if date != '':
                        conn = db()
                        sql="insert into wechat(wechatNo,name,contents,date,zan,comments) VALUES (%s,%s,%s,%s,%s,%s)"
                        conn.cursor.execute(sql,(wechatNo,name,contents,date,zan,comments))
                        conn.db.commit()
                        conn.close()
                    
                except NoSuchElementException as e:
                    pass
                except TimeoutException:
                    pass
            self.swipeUp(1000)
            sleep(1)

    # 获得机器屏幕大小x,y
    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x, y)

    # 屏幕向上滑动
    def swipeUp(self, t):
        l = self.getSize()
        x1 = int(l[0] * 0.5)  # x坐标
        y1 = int(l[1] * 0.65)  # 起始y坐标
        y2 = int(l[1] * 0.25)  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)

    def main(self):
        """
        入口
        :return:
        """
        os.system(rmCommand)
        self.del_file(localPath)
        # 登录
        # self.login()
        # 进入朋友圈
        self.enter()
        # 爬取
        self.crawl()
        
    def del_file(self,path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                del_file(c_path)
            else:
                os.remove(c_path)

if __name__ == '__main__':
    
    moments = Moments()
    moments.main()
