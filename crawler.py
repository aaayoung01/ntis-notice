import json
import requests
import xml.etree.ElementTree as ET
import re
import os

def format_date(date_str):
    if not date_str:
        return ""
    # 날짜 데이터에서 숫자만 추출한 뒤 YYYY.MM.DD 형태로 변환
    digits = re.sub(r'\D', '', date_str)
    if len(digits) >= 8:
        return f"{digits[:4]}.{digits[4:6]}.{digits[6:8]}"
    return date_str

def format_budget(amount_str):
    if not amount_str:
        return "-"
    
    # 숫자만 추출
    digits = re.sub(r'\D', '', amount_str)
    if not digits:
        return amount_str # 문자로만 된 경우 원본 반환
        
    val = int(digits)
    if val == 0:
        return "0원"
        
    # 1,000,000(백만) 단위로 나누고 콤마 삽입
    mil = val // 1000000
    if mil == 0:
        return f"{val:,}원"
    return f"{mil:,}백만원"

def update_rss_data():
    url = 'http://www.ntis.go.kr/rndgate/unRndRss.xml?prt=100'
    try:
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        new_items = []
        for item in root.findall('.//item'):
            title = item.findtext('title', default='제목 없음')
            link = item.findtext('link', default='#')
            department = item.findtext('author', default='-')
            agency = item.findtext('category', default='-')
            
            # 날짜 및 금액 포맷 적용
            date = format_date(item.findtext('pubDate', default=''))
            amount = format_budget(item.findtext('budget', default=''))
            
            # 접수시작일/마감일 (태그 대소문자 변형 모두 대응)
            appbegin = item.findtext('appbegin') or item.findtext('appBegin') or ''
            appdue = item.findtext('appdue') or item.findtext('appDue') or ''
            
            appbegin_f = format_date(appbegin)
            appdue_f = format_date(appdue)
            
            if appbegin_f and appdue_f:
                app_period = f"{appbegin_f} ~ {appdue_f}"
            else:
                app_period = "-" # 원본에 데이터가 없는 경우 하이픈 처리
                
            new_items.append({
                'department': department,
                'title': title,
                'link': link,
                'agency': agency,
                'date': date,
                'appPeriod': app_period,
                'amount': amount
            })
            
        # 기존 데이터 불러오기 (데이터 누적을 위함)
        file_path = 'data.json'
        existing_data = []
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except:
                pass
                
        existing_links = {d.get('link') for d in existing_data}
        added_count = 0
        
        # 새 공고를 최신순(맨 앞)으로 누적 삽입
        for item in reversed(new_items):
            if item['link'] not in existing_links:
                existing_data.insert(0, item)
                added_count += 1
                
        # 병합된 전체 데이터 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
            
        print(f"신규 공고 {added_count}개 추가 완료. (총 {len(existing_data)}개 누적)")
            
    except Exception as e:
        print(f"데이터 수집 중 오류 발생: {e}")

if __name__ == '__main__':
    update_rss_data()
