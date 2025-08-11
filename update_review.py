from sqlalchemy import create_engine, text
from app.core.config import settings

def update_review_content():
    """데이터베이스에서 직접 리뷰 내용 수정"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== 리뷰 내용 수정 도구 ===")
            
            # 1. 현재 리뷰 상태 확인
            result = conn.execute(text("""
                SELECT r.id, r.reviewer, r.content, p.name as platform_name
                FROM tb_reviews r
                LEFT JOIN tb_platforms p ON r.platform_id = p.id
                ORDER BY r.id
            """))
            reviews = result.fetchall()
            
            print(f"현재 리뷰 개수: {len(reviews)}")
            for review in reviews:
                print(f"  - ID: {review[0]}, 리뷰어: {review[1]}, 플랫폼: {review[3]}")
                print(f"    내용: {review[2][:100]}...")
                print()
            
            # 2. 수정할 리뷰 ID 입력
            review_id = input("수정할 리뷰 ID를 입력하세요: ")
            
            if not review_id:
                print("❌ 리뷰 ID를 입력해주세요.")
                return
            
            # 3. 새로운 리뷰 내용 입력
            print("\n새로운 리뷰 내용을 입력하세요 (여러 줄 입력 가능, 빈 줄로 종료):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            
            new_content = "\n".join(lines)
            
            if not new_content:
                print("❌ 리뷰 내용을 입력해주세요.")
                return
            
            # 4. 리뷰 내용 수정
            conn.execute(text("UPDATE tb_reviews SET content = :content WHERE id = :id"), 
                        {"content": new_content, "id": int(review_id)})
            conn.commit()
            
            print(f"✅ 리뷰 내용 수정 완료: ID {review_id}")
            
            # 5. 수정 결과 확인
            result = conn.execute(text("""
                SELECT r.id, r.reviewer, r.content, p.name as platform_name
                FROM tb_reviews r
                LEFT JOIN tb_platforms p ON r.platform_id = p.id
                WHERE r.id = :id
            """), {"id": int(review_id)})
            
            updated_review = result.fetchone()
            if updated_review:
                print(f"\n수정된 리뷰:")
                print(f"  - ID: {updated_review[0]}")
                print(f"  - 리뷰어: {updated_review[1]}")
                print(f"  - 플랫폼: {updated_review[3]}")
                print(f"  - 내용: {updated_review[2]}")
            
    except Exception as e:
        print(f"❌ 데이터베이스 수정 실패: {e}")
        raise
    finally:
        engine.dispose()

def update_reviewer_name():
    """리뷰어 이름 수정"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== 리뷰어 이름 수정 ===")
            
            # 1. 현재 리뷰 상태 확인
            result = conn.execute(text("""
                SELECT r.id, r.reviewer, r.content, p.name as platform_name
                FROM tb_reviews r
                LEFT JOIN tb_platforms p ON r.platform_id = p.id
                ORDER BY r.id
            """))
            reviews = result.fetchall()
            
            print(f"현재 리뷰 개수: {len(reviews)}")
            for review in reviews:
                print(f"  - ID: {review[0]}, 리뷰어: {review[1]}, 플랫폼: {review[3]}")
                print(f"    내용: {review[2][:50]}...")
            
            # 2. 수정할 리뷰 ID 입력
            review_id = input("\n수정할 리뷰 ID를 입력하세요: ")
            new_reviewer = input("새로운 리뷰어 이름을 입력하세요: ")
            
            if not review_id or not new_reviewer:
                print("❌ 리뷰 ID와 새로운 리뷰어 이름을 모두 입력해주세요.")
                return
            
            # 3. 리뷰어 수정
            conn.execute(text("UPDATE tb_reviews SET reviewer = :reviewer WHERE id = :id"), 
                        {"reviewer": new_reviewer, "id": int(review_id)})
            conn.commit()
            
            print(f"✅ 리뷰어 수정 완료: ID {review_id} → {new_reviewer}")
            
            # 4. 수정 결과 확인
            result = conn.execute(text("""
                SELECT r.id, r.reviewer, p.name as platform_name
                FROM tb_reviews r
                LEFT JOIN tb_platforms p ON r.platform_id = p.id
                WHERE r.id = :id
            """), {"id": int(review_id)})
            
            updated_review = result.fetchone()
            if updated_review:
                print(f"  - 수정된 리뷰: ID {updated_review[0]}, 리뷰어: {updated_review[1]}, 플랫폼: {updated_review[2]}")
            
    except Exception as e:
        print(f"❌ 데이터베이스 수정 실패: {e}")
        raise
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("=== 리뷰 수정 도구 ===")
    print("1. 리뷰 내용 수정")
    print("2. 리뷰어 이름 수정")
    
    choice = input("\n선택하세요 (1 또는 2): ")
    
    if choice == "1":
        update_review_content()
    elif choice == "2":
        update_reviewer_name()
    else:
        print("❌ 잘못된 선택입니다.")
