# from selenium import webdriver
import undetected_chromedriver as UC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import sys
import os

# Chrome 옵션 설정 (필요하면)
options = Options()
driver = UC.Chrome(options=options)

wait = WebDriverWait(driver, 10)

driver.get("https://www.google.com/travel/flights")
#driver.get("https://www.skyscanner.co.kr/")

# 편도 버튼 클릭
# (1) 왕복/편도 선택 탭 열기
# 1. 드롭다운 버튼 클릭 (VfPpkd-aPP78e)
dropdown_opener = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.VfPpkd-aPP78e"))
)
dropdown_opener.click()

# (2) "편도" 클릭
one_way = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//li[contains(., '편도')]")
))
one_way.click()

# 1. 목적지 입력 필드 찾기
destination_input = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[role='combobox'][placeholder*='목적지']"))
)

# 2. 클릭
destination_input.click()

# 기존 값 제거 후 텍스트 입력
destination_input.send_keys(Keys.CONTROL, 'a')
destination_input.send_keys("프랑스 파리")
# time.sleep(3)
# 추천 dropdown 목록 중 "파리" 선택
paris_option = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//li[contains(., '프랑스 파리')]")
    )
)
paris_option.click()
time.sleep(2)

# 3. 날짜 클릭
departure_input = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='출발']"))
)
driver.execute_script("arguments[0].click();", departure_input)

# 4. 날짜 입력
cell = driver.find_element(
    By.CSS_SELECTOR,
    'div[aria-label="2025년 12월 31일 수요일"]'
)
driver.execute_script("arguments[0].click();", cell)


# 5. 확인 버튼 클릭
btn = driver.find_element(By.XPATH, '//button[.//span[text()="확인"]]')
driver.execute_script("arguments[0].click();", btn)

# 6. 살펴보기 클릭
btn = driver.find_element(
    By.XPATH,
    '//button[.//span[text()="검색"]]'
)
driver.execute_script("arguments[0].click();", btn)

time.sleep(5) # time needed for the page to load

# page deux
# 2.1 살펴보기 펼친다
xpaths = [
    "//*[contains(text(),'더보기')]",
    "//span[contains(@class,'bEfgkb')]",
    "//span[contains(normalize-space(),'항공편 더보기')]"
]

for xp in xpaths:
    try:
        btn = driver.find_element(By.XPATH, xp)
        break
    except NoSuchElementException:
        pass

if btn:
    driver.execute_script("arguments[0].click();", btn)
    print("clicked")
else:
    print("button not found")

time.sleep(10)

# 2.1 aria-label 데이터 수집
flights = []
label_text = ""
'''
elements = driver.find_elements(
    By.XPATH,
    '//div[contains(@aria-label, "최저가")]'
)'''




elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located(
        (By.XPATH, '//div[contains(@aria-label,"최저가")]')
    )
)
# label_text = element.get_attribute("aria-label")

for el in elements:
    label_text = el.get_attribute("aria-label")
    print(label_text)
    flights.append(label_text)
    # if label_text:
    #     pass

print("\n\n\n\n\n")
for i in flights:
    print(i)
# print(flights)


# termination
driver.quit()
driver.service.process.kill()
os._exit(0)
