import json
import requests
import xml.etree.ElementTree as ET

def update_rss_data():
    # 안내받은 공식 RSS 주소 (최대 100개 호출)
    url = 'http://www.ntis.go.kr/rndgate/unRndRss.xml?prt=100'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # XML(RSS) 데이터 파싱
        root = ET.fromstring(response.content)
        
        items = []
        # RSS 규격에 따라 item 태그 안의 정보를 반복해서 찾음
        for item in root.findall('.//item'):
            title = item.findtext('title', default='제목 없음')
            link = item.findtext('link', default='#')
            department = item.findtext('author', default='')
            agency = item.findtext('category', default='')
            date = item.findtext('pubDate', default='')
            amount = item.findtext('budget', default='')
            
            # 기존 화면 코드(index.html)와 완벽히 호환되도록 영어 키값 맞춤
            items.append({
                'department': department,
                'title': title,
                'link': link,
                'agency': agency,
                'date': date,
                'amount': amount
            })
            
        # 가져온 데이터를 data.json 파일로 저장
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
            
        print(f"총 {len(items)}개의 공고 데이터를 성공적으로 가져왔습니다.")
            
    except Exception as e:
        print(f"데이터 수집 중 오류 발생: {e}")

if __name__ == '__main__':
    update_rss_data()
