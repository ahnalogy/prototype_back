from sqlalchemy import create_engine, text
from app.core.config import settings

def update_reviewer_directly():
    """데이터베이스에서 직접 리뷰어 수정"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== 데이터베이스 직접 수정 ===")
            
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

def batch_update_reviewers_directly():
    """플랫폼별로 일괄 리뷰어 수정"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== 플랫폼별 일괄 리뷰어 수정 ===")
            
            # 플랫폼별 리뷰어 매핑
            platform_reviewers = {
                "야놀자": ["김야놀", "박야놀", "이야놀", "최야놀", "정야놀"],
                "여기어때": ["김여기", "박여기", "이여기", "최여기", "정여기"],
                "booking.com": ["김부킹", "박부킹", "이부킹", "최부킹", "정부킹"]
            }
            
            for platform_name, reviewers in platform_reviewers.items():
                print(f"\n=== {platform_name} 플랫폼 처리 중 ===")
                
                # 해당 플랫폼의 리뷰 조회
                result = conn.execute(text("""
                    SELECT r.id, r.reviewer
                    FROM tb_reviews r
                    LEFT JOIN tb_platforms p ON r.platform_id = p.id
                    WHERE p.name = :platform_name
                    ORDER BY r.id
                """), {"platform_name": platform_name})
                
                platform_reviews = result.fetchall()
                print(f"  {platform_name} 리뷰 {len(platform_reviews)}개 발견")
                
                # 리뷰어 수정
                for i, review in enumerate(platform_reviews):
                    if i < len(reviewers):
                        new_reviewer = reviewers[i]
                        old_reviewer = review[1]
                        
                        conn.execute(text("UPDATE tb_reviews SET reviewer = :reviewer WHERE id = :id"), 
                                   {"reviewer": new_reviewer, "id": review[0]})
                        print(f"    ✅ ID {review[0]}: {old_reviewer} → {new_reviewer}")
                    else:
                        print(f"    ⚠️ ID {review[0]}: 리뷰어 매핑 없음")
                
                conn.commit()
                print(f"  {platform_name} 플랫폼 수정 완료")
            
            print("\n=== 모든 플랫폼 수정 완료 ===")
            
    except Exception as e:
        print(f"❌ 일괄 수정 실패: {e}")
        raise
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("=== 데이터베이스 직접 수정 도구 ===")
    print("1. 개별 리뷰어 수정")
    print("2. 플랫폼별 일괄 리뷰어 수정")
    
    choice = input("\n선택하세요 (1 또는 2): ")
    
    if choice == "1":
        update_reviewer_directly()
    elif choice == "2":
        batch_update_reviewers_directly()
    else:
        print("❌ 잘못된 선택입니다.")
