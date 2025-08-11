from sqlalchemy import create_engine, text
from app.core.config import settings

def migrate_database():
    """데이터베이스 마이그레이션"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== 데이터베이스 마이그레이션 시작 ===")
            
            # 1. platform_id 컬럼이 있는지 확인
            result = conn.execute(text("PRAGMA table_info(tb_reviews)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'platform_id' not in columns:
                print("platform_id 컬럼 추가 중...")
                conn.execute(text("ALTER TABLE tb_reviews ADD COLUMN platform_id INTEGER DEFAULT 1"))
                conn.commit()
                print("platform_id 컬럼 추가 완료")
            else:
                print("platform_id 컬럼이 이미 존재합니다.")
            
            # 2. 플랫폼 데이터 확인 및 생성
            result = conn.execute(text("SELECT COUNT(*) FROM tb_platforms"))
            platform_count = result.fetchone()[0]
            
            if platform_count == 0:
                print("기본 플랫폼 데이터 생성 중...")
                platforms = [
                    ("야놀자",),
                    ("여기어때",),
                    ("booking.com",)
                ]
                conn.execute(text("INSERT INTO tb_platforms (name) VALUES (?)"), platforms)
                conn.commit()
                print("기본 플랫폼 데이터 생성 완료")
            else:
                print(f"플랫폼 데이터가 {platform_count}개 존재합니다.")
            
            # 3. 기존 리뷰들의 platform_id 업데이트 (기본값 1로 설정)
            result = conn.execute(text("SELECT COUNT(*) FROM tb_reviews WHERE platform_id IS NULL"))
            null_platform_count = result.fetchone()[0]
            
            if null_platform_count > 0:
                print(f"{null_platform_count}개의 리뷰에 platform_id 설정 중...")
                conn.execute(text("UPDATE tb_reviews SET platform_id = 1 WHERE platform_id IS NULL"))
                conn.commit()
                print("platform_id 설정 완료")
            
            print("=== 마이그레이션 완료 ===")
            
    except Exception as e:
        print(f"마이그레이션 실패: {e}")
        raise
    finally:
        engine.dispose()

if __name__ == "__main__":
    migrate_database()
