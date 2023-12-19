from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import Select
import time
import json


def add_nested_item(dictionary, keys, value):
    """
    在嵌套字典中新增项。

    Parameters:
    - dictionary: 要更新的字典
    - keys: 以列表形式提供的键，用于指定嵌套层级
    - value: 要设置的值
    """
    current_level = dictionary
    for key in keys[:-1]:
        if key not in current_level or not isinstance(current_level[key], dict):
            # 如果当前层级不存在或者不是字典类型，创建一个字典
            current_level[key] = {}
        current_level = current_level[key]
    current_level[keys[-1]] = value

url = 'https://university-tw.ldkrsi.men/caac/'

university_dict = {}
stay_dict = {}
department_dict = {}
# 配置Selenium以使用Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')  # 无头模式，不打开浏览器窗口
driver = webdriver.Chrome(options=chrome_options)

# 打开网页
driver.get(url)

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 使用CSS选择器找到指定的<select>元素
select_element = soup.select_one('.select #school')

# 提取所有<option>元素的文本内容
options = select_element.find_all('option')


# 迭代并打印每个大学的名称，跳过第一个"請選擇學校"的选项
for option in options[1:]:
    match = re.search(r'\((\d+)\)', option.text)  
    # 如果匹配成功，提取编号并构建字典
    if match:
        university_code = match.group(1)
        school = re.search(r'\)\s*([^)]+)', option.text)   
        university_dict[university_code] = school.group(1)
    else:
        print("No match found.")


select_school = Select(driver.find_element(By.ID, 'school'))

n = 1
i=1

for _ in range(len(university_dict)):      
    select_school.select_by_index(n)
    # 等待一段时间，确保相关事件触发
    time.sleep(2)

    # 再次使用BeautifulSoup解析HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # 选择另一select #dep
    select_dep = Select(driver.find_element(By.ID, 'dep'))

    # 提取所有<option>元素的文本内容
    options_dep = select_dep.options

    # 打印每个系所的选项
    print("系所選項:")
    for option2 in options_dep:
        match2 = re.search(r'\((\d+)\)', option2.text)
        if match2:
            dep_code = match2.group(1)
            dep = re.search(r'\)\s*([^)]+)', option2.text)
            stay_dict[dep_code] = dep.group(1)
        else:
            print("No match found.")
            
    department_dict[str(i)] = stay_dict
    stay_dict = {}
    i+=1
    n+=1
    print(i)
   
with open('department.json', 'w') as file:
    json.dump(department_dict, file, indent=4)

with open('university.json', 'w') as file:
    json.dump(university_dict, file, indent=4)

# 关闭浏览器
driver.quit()
