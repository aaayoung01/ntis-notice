import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def crawl_real_ntis():
    # 깃허브 서버용 가상 크롬 브라우저 설정
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    url = 'https://www.ntis.go.kr/rndgate/eg/un/ra/initList.do'
    
    try:
        driver.get(url)
        # 자바스크립트로 표가 화면에 그려질 때까지 최대 10초 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
        )
        time.sleep(2) # 데이터 로딩 안정화 대기
        
        data = []
        rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if len(cols) < 5:
                continue
                
            a_tag = row.find_element(By.TAG_NAME, 'a')
            title = a_tag.text.strip()
            
            # 실제 링크가 숨겨진 onclick 속성이나 href 속성 추출
            raw_href = a_tag.get_attribute('href')
            raw_onclick = a_tag.get_attribute('onclick')
            
            link = "#"
            if raw_href and "javascript" not in raw_href:
                link = raw_href
            elif raw_onclick:
                # onclick="fnView('실제번호')" 형태에서 숫자만 빼내어 진짜 주소 조립
                import re
                match = re.search(r"\'(\d+)\'", raw_onclick)
                if match:
                    real_id = match.group(1)
                    link = f"https://www.ntis.go.kr/rndgate/eg/un/ra/view.do?roRndUid={real_id}"

            data.append({
                'department': cols[1].text.strip(),
                'title': title,
                'link': link,
                'agency': cols[3].text.strip(),
                'date': cols[4].text.strip(),
                'amount': cols[5].text.strip() if len(cols) > 5 else '0'
            })
            
        # 추출한 진짜 데이터를 json 파일에 저장
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        print(f"크롤링 에러 발생: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    crawl_real_ntis()
