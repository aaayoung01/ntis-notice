from datetime import datetime
import json
import os


def update_crawler():
  # NTIS 실제 공고 구조에 맞춘 샘플 및 확장 데이터 세트
  # (실제 구동 시 정상적으로 표와 링크가 뜨는지 확인용 데이터입니다)
  sample_data = [
      {
          'department': '국방부',
          'title': (
              '26년 국방연구개발 전력지원체계사업 주관연구개발기관 선정을 위한'
              ' 공고문'
          ),
          'link': 'https://www.ntis.go.kr/rndgate/eg/un/ra/view.do?roRndUid=1277668',
          'agency': '국방기술진흥연구소',
          'date': '2026.09.14',
          'amount': '6,742백만원',
      },
      {
          'department': '보건복지부',
          'title': (
              '「2026년 핵심인재 글로벌 브릿지 연수 프로그램 수행기관 모집」 2차'
              ' 공고 안내'
          ),
          'link': 'https://www.ntis.go.kr/rndgate/eg/un/ra/view.do?roRndUid=1277667',
          'agency': '한국보건산업진흥원',
          'date': '2026.09.10',
          'amount': '150백만원',
      },
      {
          'department': '과학기술정보통신부',
          'title': '2027년 상반기 <대한민국 과학기술인상> 선정계획 공고',
          'link': 'https://www.ntis.go.kr/rndgate/eg/un/ra/view.do?roRndUid=1277666',
          'agency': '한국연구재단',
          'date': '2026.09.09',
          'amount': '365백만원',
      },
      {
          'department': '행정안전부',
          'title': '2028년도 과학수사감정기법연구개발사업 과제발굴을 위한 연구수요조사 안내',
          'link': 'https://www.ntis.go.kr/mdgate/eg/un/ra/view.do?rorNdUid=1277668',
          'agency': '국립과학수사연구원',
          'date': '2026.09.09',
          'amount': '0원',
      },
      {
          'department': '우주항공청',
          'title': (
              '2026년도 우주기술혁신인재양성(R&D)사업[우주항공 글로벌 인력양성 및'
              ' 활용] 2차 추가공고'
          ),
          'link': 'https://www.ntis.go.kr/rndgate/eg/un/ra/view.do?roRndUid=1277665',
          'agency': '우주항공청',
          'date': '2026.09.07',
          'amount': '5,000백만원',
      },
  ]

  # 기존 data.json이 있다면 불러오고, 없으면 생성
  file_path = 'data.json'
  if os.path.exists(file_path):
    try:
      with open(file_path, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    except:
      existing_data = []
  else:
    existing_data = []

  # 데이터가 비어있거나 부족할 경우 샘플 데이터 자동 채우기
  if not existing_data:
    existing_data = sample_data

  with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=4)
  print('데이터 업데이트 완료.')


if __name__ == '__main__':
  update_crawler()
