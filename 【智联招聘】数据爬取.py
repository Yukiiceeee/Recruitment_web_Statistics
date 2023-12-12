# 导入selenium自动测试模块
# selenium较为简单，相比js逆向简单，但是效率较低，爬取较慢
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
# 导入csv模块
import csv

# 创建文件对象
f = open('data.csv', mode='w', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
        '职位',
        '公司',
        '薪资',
        '年薪',
        '城市',
        '区域',
        '经验',
        '学历',
        '公司性质',
        '公司规模',
        '标签',
])
csv_writer.writeheader()

# 导入本地谷歌浏览器的用户文件，使得爬取数据时可以用现有用户登录招聘网站
options = Options()
options.add_argument("--user-data-dir=C:\\Users\\86133\\AppData\\Local\\Google\\Chrome\\User Data")

# # 也可以创建一个 Service 对象，指向 chromedriver 的路径，但是这样就无法登录
# service = Service(executable_path=r'D:\Microsoft Visual Studio\shared\Python39_64\chromedriver.exe')

# 使用创建的 service 对象来初始化 Chrome WebDriver
driver = webdriver.Chrome(options = options)

# 访问目标网站
driver.get('https://sou.zhaopin.com/?jl=538&kw=python&p=1')
print(driver)

# 下滑操作（避免无法自动点击下一页按钮）
def drop_down():
    for x in range(1, 12, 2):
        time.sleep(1)
        j = x / 9
        # document.documentElement.scrollTop 指定滚动条位置
        # document.documentElement.scrollHeight 指定浏览器获取页面的最大高度
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        driver.execute_script(js)

# 定义爬取数据函数，实现爬取一页数据功能
def get_content():
    # 延时等待，等待元素内容加载完成再获取
    # 这里设置等待10s，加载完成元素立刻获取
    driver.implicitly_wait(10)
    drop_down()

    # 定位元素 <元素面板>
    divs = driver.find_elements(By.CSS_SELECTOR, '.joblist-box__item')

    for div in divs:
        # 提取具体数据
        # 标题
        title = div.find_element(By.CSS_SELECTOR, '.iteminfo__line1__jobname__name').get_attribute('title')
        # 公司
        company = div.find_element(By.CSS_SELECTOR, '.iteminfo__line1__compname__name').get_attribute('title')
        # 薪资
        salary = div.find_element(By.CSS_SELECTOR, '.iteminfo__line2__jobdesc__salary').text
        salary_info = salary.split('·')
        if len(salary_info) >= 2:
            year_salary = salary_info[-1].replace('薪', '')
            money = salary_info[0]
        else:
            year_salary = '12'
            money = salary_info[0]

        # 详细信息
        info = [i.text for i in div.find_elements(By.CSS_SELECTOR, '.iteminfo__line2__jobdesc__demand__item')]
        area_info = info[0].split('-')  # 城市与区域
        if len(area_info) >= 2:
            city = area_info[0]
            area = area_info[1]
        else:
            city = area_info[0]
            area = "未知"  # 或者使用其他默认值
        exp = info[1]   # 经验
        edu = info[2]   # 教育
        tags = '.'.join([j.text for j in div.find_elements(By.CSS_SELECTOR, '.iteminfo__line3__welfare__item')])
        cop_info = [x.text for x in div.find_elements(By.CSS_SELECTOR, '.iteminfo__line2__compdesc__item')]
        cop_type = cop_info[0]
        cop_num = cop_info[1]
        dit = {
            '职位': title,
            '公司': company,
            '薪资': salary,
            '年薪': year_salary,
            '城市': city,
            '区域': area,
            '经验': exp,
            '学历': edu,
            '公司性质': cop_type,
            '公司规模': cop_num,
            '标签': tags,
        }
        # 写入数据
        csv_writer.writerow(dit)
        print(dit)

for page in range(10):
    get_content()
    # 这里可以写个等待按钮加载完成，但是一般足够加载了，所以不需要
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, '.soupager button:btn soupager__btn'))
    # )
    # 实现翻页，自动点击下一页按钮，读取下一页信息
    target = driver.find_element(By.CSS_SELECTOR, 'button.btn.soupager__btn')
    driver.execute_script("arguments[0].click();", target)

time.sleep(10)  # 等待 10 秒再退出程序















