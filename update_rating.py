from sqlalchemy import create_engine, text
from app.core.config import settings

def update_rating():
    """데이터베이스에서 직접 리뷰 평점 수정"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
                         print("=== 리뷰 평점 수정 도구 ===")
             
             # 1. 현재 리뷰 상태 확인
             result = conn.execute(text("""
                 SELECT r.id, r.reviewer, r.rating, SUBSTR(r.content, 1, 50), p.name as platform_name
                 FROM tb_reviews r
                 LEFT JOIN tb_platforms p ON r.platform_id = p.id
                 ORDER BY r.id
             """))
            reviews = result.fetchall()
            
            print(f"현재 리뷰 개수: {len(reviews)}")
            for review in reviews:
                print(f"  - ID: {review[0]}, 리뷰어: {review[1]}, 평점: {review[2]}점, 플랫폼: {review[4]}")
                print(f"    내용: {review[3]}...")
                print()
            
            # 2. 수정할 리뷰 ID 입력
            review_id = input("수정할 리뷰 ID를 입력하세요: ")
            
            if not review_id:
                print("❌ 리뷰 ID를 입력해주세요.")
                return
            
            # 3. 새로운 평점 입력
            new_rating = input("새로운 평점을 입력하세요 (1-5): ")
            
            if not new_rating:
                print("❌ 평점을 입력해주세요.")
                return
            
            try:
                new_rating = int(new_rating)
                if new_rating < 1 or new_rating > 5:
                    print("❌ 평점은 1-5 사이의 숫자여야 합니다.")
                    return
            except ValueError:
                print("❌ 평점은 숫자여야 합니다.")
                return
            
            # 4. 해당 리뷰가 존재하는지 확인
            result = conn.execute(text("""
                SELECT r.id, r.reviewer, r.rating, p.name as platform_name
                FROM tb_reviews r
                LEFT JOIN tb_platforms p ON r.platform_id = p.id
                WHERE r.id = :id
            """), {"id": int(review_id)})
            review = result.fetchone()
            
            if not review:
                print(f"❌ ID {review_id}인 리뷰가 존재하지 않습니다.")
                return
            
            print(f"수정할 리뷰:")
            print(f"  - ID: {review[0]}")
            print(f"  - 리뷰어: {review[1]}")
            print(f"  - 현재 평점: {review[2]}점")
            print(f"  - 플랫폼: {review[3]}")
            print(f"  - 새 평점: {new_rating}점")
            
            # 5. 수정 확인
            confirm = input(f"\n정말로 평점을 {review[2]}점에서 {new_rating}점으로 수정하시겠습니까? (y/N): ")
            if confirm.lower() != 'y':
                print("❌ 수정이 취소되었습니다.")
                return
            
            # 6. 평점 수정
            conn.execute(text("UPDATE tb_reviews SET rating = :rating WHERE id = :id"), 
                        {"rating": new_rating, "id": int(review_id)})
            conn.commit()
            
            print(f"✅ 평점 수정 완료: ID {review_id} → {new_rating}점")
            
            # 7. 수정 결과 확인
            result = conn.execute(text("""
                SELECT r.id, r.reviewer, r.rating, p.name as platform_name
                FROM tb_reviews r
                LEFT JOIN tb_platforms p ON r.platform_id = p.id
                WHERE r.id = :id
            """), {"id": int(review_id)})
            
            updated_review = result.fetchone()
            if updated_review:
                print(f"\n수정된 리뷰:")
                print(f"  - ID: {updated_review[0]}")
                print(f"  - 리뷰어: {updated_review[1]}")
                print(f"  - 평점: {updated_review[2]}점")
                print(f"  - 플랫폼: {updated_review[3]}")
            
    except Exception as e:
        print(f"❌ 데이터베이스 수정 실패: {e}")
        raise
    finally:
        engine.dispose()

def batch_update_ratings():
    """플랫폼별로 일괄 평점 수정"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== 플랫폼별 일괄 평점 수정 ===")
            
            # 플랫폼별 평점 매핑
            platform_ratings = {
                "야놀자": [5, 4, 5, 4, 5],
                "여기어때": [3, 4, 3, 4, 3],
                "booking.com": [4, 5, 4, 5, 4]
            }
            
            for platform_name, ratings in platform_ratings.items():
                print(f"\n=== {platform_name} 플랫폼 처리 중 ===")
                
                # 해당 플랫폼의 리뷰 조회
                result = conn.execute(text("""
                    SELECT r.id, r.reviewer, r.rating
                    FROM tb_reviews r
                    LEFT JOIN tb_platforms p ON r.platform_id = p.id
                    WHERE p.name = :platform_name
                    ORDER BY r.id
                """), {"platform_name": platform_name})
                
                platform_reviews = result.fetchall()
                print(f"  {platform_name} 리뷰 {len(platform_reviews)}개 발견")
                
                # 평점 수정
                for i, review in enumerate(platform_reviews):
                    if i < len(ratings):
                        new_rating = ratings[i]
                        old_rating = review[2]
                        
                        conn.execute(text("UPDATE tb_reviews SET rating = :rating WHERE id = :id"), 
                                   {"rating": new_rating, "id": review[0]})
                        print(f"    ✅ ID {review[0]}: {old_rating}점 → {new_rating}점")
                    else:
                        print(f"    ⚠️ ID {review[0]}: 평점 매핑 없음")
                
                conn.commit()
                print(f"  {platform_name} 플랫폼 수정 완료")
            
            print("\n=== 모든 플랫폼 수정 완료 ===")
            
    except Exception as e:
        print(f"❌ 일괄 수정 실패: {e}")
        raise
    finally:
        engine.dispose()

def show_rating_statistics():
    """평점 통계 보기"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== 평점 통계 ===")
            
            # 전체 평점 통계
            result = conn.execute(text("""
                SELECT 
                    AVG(rating) as avg_rating,
                    COUNT(*) as total_reviews,
                    MIN(rating) as min_rating,
                    MAX(rating) as max_rating
                FROM tb_reviews
            """))
            stats = result.fetchone()
            
            print(f"전체 통계:")
            print(f"  - 평균 평점: {stats[0]:.1f}점")
            print(f"  - 총 리뷰 수: {stats[1]}개")
            print(f"  - 최저 평점: {stats[2]}점")
            print(f"  - 최고 평점: {stats[3]}점")
            
            # 플랫폼별 평점 통계
            result = conn.execute(text("""
                SELECT 
                    p.name as platform_name,
                    AVG(r.rating) as avg_rating,
                    COUNT(*) as review_count,
                    MIN(r.rating) as min_rating,
                    MAX(r.rating) as max_rating
                FROM tb_reviews r
                LEFT JOIN tb_platforms p ON r.platform_id = p.id
                GROUP BY p.name
                ORDER BY p.name
            """))
            platform_stats = result.fetchall()
            
            print(f"\n플랫폼별 통계:")
            for stat in platform_stats:
                print(f"  - {stat[0]}:")
                print(f"    평균 평점: {stat[1]:.1f}점")
                print(f"    리뷰 수: {stat[2]}개")
                print(f"    평점 범위: {stat[3]}점 ~ {stat[4]}점")
            
            # 평점별 개수
            result = conn.execute(text("""
                SELECT rating, COUNT(*) as count
                FROM tb_reviews
                GROUP BY rating
                ORDER BY rating
            """))
            rating_counts = result.fetchall()
            
            print(f"\n평점별 개수:")
            for rating_count in rating_counts:
                print(f"  - {rating_count[0]}점: {rating_count[1]}개")
            
    except Exception as e:
        print(f"❌ 통계 조회 실패: {e}")
        raise
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("=== 리뷰 평점 수정 도구 ===")
    print("1. 개별 리뷰 평점 수정")
    print("2. 플랫폼별 일괄 평점 수정")
    print("3. 평점 통계 보기")
    
    choice = input("\n선택하세요 (1-3): ")
    
    if choice == "1":
        update_rating()
    elif choice == "2":
        batch_update_ratings()
    elif choice == "3":
        show_rating_statistics()
    else:
        print("❌ 잘못된 선택입니다.")
