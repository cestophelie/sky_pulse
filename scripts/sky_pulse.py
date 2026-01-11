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
    'div[aria-label="2026년 1월 31일 토요일"]'
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

print("------starting here-------")

'''buttons = wait.until(
    EC.presence_of_all_elements_located((
        By.XPATH,
        "//button[contains(@aria-label, '항공편 세부정보')]"
    ))
)'''
cards = driver.find_elements(
    By.XPATH,
    "//li[contains(@class, 'pIav2d')]"
)

results = []
elem_count = 0
cards_len = len(cards)

wait = WebDriverWait(driver, 15)
xpath = "//button[contains(@aria-label,'항공편 세부정보')]"

for i in range(cards_len):
    buttons = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, xpath))
    )
    # 아직 안 열린 버튼만
    unopened = [
        b for b in buttons
        if b.get_attribute("aria-expanded") == "false"
    ]

    if not unopened:
        break

    btn = unopened[0]

    # 클릭 (JS)
    driver.execute_script("arguments[0].click();", btn)

    wait.until(
        lambda d: btn.get_attribute("aria-expanded") == "true"
    )

print("exited")

# DOM has changed -> initiate the variable
cards = driver.find_elements(
    By.XPATH,
    "//li[contains(@class, 'pIav2d')]" # 출발 날짜부터 모두 포함된 최상위 항공 정보 단위
)
print(len(cards))

for card in cards:
    try:
        price_span = card.find_element(
            By.XPATH,
            ".//span[@aria-label and contains(@aria-label,'원')]"
        )
        # price = price_div.text # aria-label의 443400 대한민국 원이 \443,400원으로 js 렌더링 되는데 시차가 있음
        price = int(price_span.get_attribute("aria-label").split()[0])

        airport_spans = card.find_elements(By.XPATH, ".//span[@dir='ltr']")
        trips = card.find_elements(
            By.CSS_SELECTOR,
            "div.MX5RWe.sSHqwe.y52p7d"
        )

        results2 = []

        for i, trip in enumerate(trips):
            # 공항 2개씩 매칭
            dep = airport_spans[i * 2].text.strip("()")
            arr = airport_spans[i * 2 + 1].text.strip("()")

            spans = trip.find_elements(By.XPATH, ".//span")
            texts = [s.text.strip() for s in spans if s.text.strip()]

            # texts 예: [항공사, 기종, 편명]
            results.append({
                "from": dep,
                "to": arr,
                "price": price,
                "airline": texts[0],
                "airplane": texts[1],
                "flight_no": texts[2]
            })

        print("now in try")

    except Exception:
        # print("------cards parsing exception------")
        print("now in except")
        continue

# print(results)
for i, item in enumerate(results, start=1):
    print(f"{i}.{item}")

'''
# price extraction first
spans = wait.until(
    EC.presence_of_all_elements_located((
        By.XPATH,
        "//span[@role='text' and contains(@aria-label, '원')]"
    ))
)

prices = []
for span in spans:
    label = span.get_attribute("aria-label")  # 예: "443400 대한민국 원"
    price = int(label.split()[0])
    prices.append(price)

print(prices)

# button 상세정보 안의 데이터 추출
button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//button[contains(@aria-label, '항공편 세부정보')]"
    ))
)
button.click()

# plane info collection
wait = WebDriverWait(driver, 10)

divs = driver.find_elements(
    By.CSS_SELECTOR,
    "div.MX5RWe.sSHqwe.y52p7d"
)

results = []

for div in divs:
    spans = div.find_elements(By.XPATH, ".//span")
    texts = [s.text.strip() for s in spans if s.text.strip()]
    results.append(texts)

print(results)

button.click()
'''
print("------ending here-------")
time.sleep(5)

# button.click()

# page deux
# 2.1 항공편 더보기 펼친다
'''
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
'''

# termination
driver.quit()
driver.service.process.kill()
os._exit(0)
