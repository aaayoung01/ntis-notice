import json
import requests
import xml.etree.ElementTree as ET
import re
import os

def format_date(date_str):
    if not date_str:
        return ""
    digits = re.sub(r'\D', '', date_str)
    if len(digits) >= 8:
        return f"{digits[:4]}.{digits[4:6]}.{digits[6:8]}"
    return date_str

def format_budget(amount_str):
    if not amount_str:
        return "-"
    digits = re.sub(r'\D', '', amount_str)
    if not digits:
        return amount_str
    val = int(digits)
    if val == 0:
        return "0원"
    mil = val // 1000000
    if mil == 0:
        return f"{val:,}원"
    return f"{mil:,}백만원"

def update_rss_data():
    allowed_depts = [
        "과학기술정보통신부", "교육부", "보건복지부", 
        "산업통상부", "식품의약품안전처", "질병관리청", "기타"
    ]
    
    new_items = []
    target_count = 100
    max_pages = 10 # 무한 루프 방지: 최대 1,000개의 과거 공고까지만 탐색
    
    start_idx = 1
    end_idx = 100
    
    for _ in range(max_pages):
        # NTIS 페이징 파라미터 적용 (Fi: 시작번호, prt: 끝번호)
        url = f'http://www.ntis.go.kr/rndgate/unRndRss.xml?Fi={start_idx}&prt={end_idx}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            
            items = root.findall('.//item')
            if not items:
                break # 더 이상 과거 데이터가 없으면 중단
                
            for item in items:
                raw_dept = item.findtext('author', default='-').strip()
                if raw_dept not in allowed_depts:
                    continue
                    
                title = item.findtext('title', default='제목 없음')
                link = item.findtext('link', default='#')
                agency = item.findtext('category', default='-')
                date = format_date(item.findtext('pubDate', default=''))
                amount = format_budget(item.findtext('budget', default=''))
                
                appbegin = item.findtext('appbegin') or item.findtext('appBegin') or ''
                appdue = item.findtext('appdue') or item.findtext('appDue') or ''
                appbegin_f = format_date(appbegin)
                appdue_f = format_date(appdue)
                
                app_period = f"{appbegin_f} ~ {appdue_f}" if appbegin_f and appdue_f else "-"
                    
                new_items.append({
                    'department': raw_dept,
                    'title': title,
                    'link': link,
                    'agency': agency,
                    'date': date,
                    'appPeriod': app_period,
                    'appBegin': appbegin_f,
                    'appDue': appdue_f,
                    'amount': amount
                })
                
                # 조건에 맞는 공고가 100개가 되면 즉시 탐색 중단
                if len(new_items) >= target_count:
                    break 
                    
            if len(new_items) >= target_count:
                break
                
            # 목표 수량을 못 채웠으면 다음 100개(과거 공고)를 탐색하기 위해 인덱스 증가
            start_idx += 100
            end_idx += 100
            
        except Exception as e:
            print(f"데이터 수집 중 오류 발생: {e}")
            break
            
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
    
    # 새 공고를 최신순으로 누적 삽입
    for item in reversed(new_items):
        if item['link'] not in existing_links:
            existing_data.insert(0, item)
            added_count += 1
            
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
        
    print(f"조건 부합 공고 {added_count}개 추가 완료. (총 {len(existing_data)}개 누적)")

if __name__ == '__main__':
    update_rss_data()
