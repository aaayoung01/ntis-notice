import json
import requests
import xml.etree.ElementTree as ET
import re
import os

def format_date(date_str):
    if not date_str: return ""
    digits = re.sub(r'\D', '', date_str)
    return f"{digits[:4]}.{digits[4:6]}.{digits[6:8]}" if len(digits) >= 8 else date_str

def format_budget(amount_str):
    if not amount_str: return "-"
    digits = re.sub(r'\D', '', amount_str)
    if not digits: return amount_str
    val = int(digits)
    if val == 0: return "0원"
    mil = val // 1000000
    return f"{val:,}원" if mil == 0 else f"{mil:,}백만원"

def update_rss_data():
    url = 'http://www.ntis.go.kr/rndgate/unRndRss.xml?prt=100'
    allowed_depts = ["과학기술정보통신부", "교육부", "보건복지부", "산업통상부", "식품의약품안전처", "질병관리청", "기타"]
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        new_items = []
        for item in root.findall('.//item'):
            raw_dept = item.findtext('author', default='-').strip()
            if raw_dept not in allowed_depts: continue
                
            appbegin = item.findtext('appbegin') or item.findtext('appBegin') or ''
            appdue = item.findtext('appdue') or item.findtext('appDue') or ''
            appbegin_f, appdue_f = format_date(appbegin), format_date(appdue)
                
            new_items.append({
                'department': raw_dept,
                'title': item.findtext('title', default='제목 없음'),
                'link': item.findtext('link', default='#'),
                'agency': item.findtext('category', default='-'),
                'date': format_date(item.findtext('pubDate', default='')),
                'appPeriod': f"{appbegin_f} ~ {appdue_f}" if appbegin_f and appdue_f else "-",
                'appBegin': appbegin_f,
                'appDue': appdue_f,
                'amount': format_budget(item.findtext('budget', default=''))
            })
            
        file_path = 'data.json'
        existing_data = json.load(open(file_path, 'r', encoding='utf-8')) if os.path.exists(file_path) else []
        existing_links = {d.get('link') for d in existing_data}
        
        for item in reversed(new_items):
            if item['link'] not in existing_links:
                existing_data.insert(0, item)
                
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == '__main__':
    update_rss_data()
