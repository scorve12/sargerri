# rss/management/commands/add_tags.py
from django.core.management.base import BaseCommand
from rss.models import Tag

class Command(BaseCommand):
    help = '기본 태그들을 데이터베이스에 추가합니다'

    def handle(self, *args, **options):
        # 추가할 태그 리스트
        tags_to_add = [
            # 공연/엔터테인먼트
            '공연', '연극', '뮤지컬', '콘서트', '음악회', '댄스', '발레', '오페라',
            '코미디', '버스킹', '페스티벌', '축제',
            
            # 음식/요리
            '삼겹살', '맛집', '요리', '카페', '디저트', '술집', '한식', '양식',
            '중식', '일식', '베이킹', '와인', '커피', '맥주',
            
            # 문화/예술
            '전시회', '미술', '사진', '조각', '설치미술', '갤러리', '박물관',
            '영화', '독서', '문학', '시', '소설',
            
            # 스포츠/활동
            '축구', '야구', '농구', '배구', '테니스', '골프', '수영', '헬스',
            '요가', '필라테스', '등산', '캠핑', '낚시', '자전거', '마라톤',
            
            # 교육/학습
            '교육', '세미나', '워크샵', '강의', '스터디', '언어', '자격증',
            '컴퓨터', '프로그래밍', '디자인', '마케팅',
            
            # 취미/여가
            '여행', '사진촬영', '게임', '보드게임', '독서', '영화감상', '드라마',
            '애니메이션', '만화', '수집', '원예', '반려동물',
            
            # 건강/웰빙
            '건강', '운동', '다이어트', '명상', '힐링', '스파', '마사지',
            
            # 기술/IT
            '기술', 'IT', '개발', '앱', '웹', 'AI', '빅데이터', '블록체인',
            
            # 비즈니스/네트워킹
            '비즈니스', '창업', '투자', '부동산', '금융', '네트워킹', '미팅',
            
            # 봉사/사회활동
            '봉사', '기부', '환경', '사회공헌', '자원봉사',
            
            # 기타
            '모임', '파티', '데이트', '가족', '친구', '동호회', '클럽'
        ]
        
        created_count = 0
        existing_count = 0
        
        for tag_name in tags_to_add:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                created_count += 1
                self.stdout.write(f'✅ 새 태그 생성: {tag_name}')
            else:
                existing_count += 1
                self.stdout.write(f'⚠️  이미 존재: {tag_name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n완료! 새로 생성된 태그: {created_count}개, 기존 태그: {existing_count}개'
            )
        )