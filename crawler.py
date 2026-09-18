import json
import requests
import xml.etree.ElementTree as ET
import re

def format_date(date_str):
    if not date_str:
        return ""
    # 날짜 데이터에서 숫자만 추출한 뒤 YYYY.MM.DD 형태로 변환
    digits = re.sub(r'\D', '', date_str)
    if len(digits) >= 8:
        return f"{digits[:4]}.{digits[4:6]}.{digits[6:8]}"
    return date_str

def update_rss_data():
    url = 'http://www.ntis.go.kr/rndgate/unRndRss.xml?prt=100'
    try:
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        items = []
        for item in root.findall('.//item'):
            title = item.findtext('title', default='제목 없음')
            link = item.findtext('link', default='#')
            department = item.findtext('author', default='')
            agency = item.findtext('category', default='')
            date = format_date(item.findtext('pubDate', default=''))
            amount = item.findtext('budget', default='-')
            
            # 접수시작일과 마감일을 가져와 YYYY.MM.DD ~ YYYY.MM.DD 형태로 결합
            appbegin = format_date(item.findtext('appbegin', default=''))
            appdue = format_date(item.findtext('appdue', default=''))
            app_period = f"{appbegin} ~ {appdue}" if appbegin and appdue else "-"
            
            items.append({
                'department': department,
                'title': title,
                'link': link,
                'agency': agency,
                'date': date,
                'appPeriod': app_period,
                'amount': amount
            })
            
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        print(f"데이터 수집 중 오류 발생: {e}")

if __name__ == '__main__':
    update_rss_data()
