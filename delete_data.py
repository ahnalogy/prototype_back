from sqlalchemy import create_engine, text
from app.core.config import settings

def delete_individual_platform():
    """개별 플랫폼 데이터 삭제"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== 개별 플랫폼 데이터 삭제 ===")
            
            # 1. 현재 플랫폼 데이터 확인
            result = conn.execute(text("SELECT id, name FROM tb_platforms ORDER BY id"))
            platforms = result.fetchall()
            
            if not platforms:
                print("❌ tb_platforms 테이블에 데이터가 없습니다.")
                return
            
            print(f"현재 플랫폼 개수: {len(platforms)}")
            for platform in platforms:
                print(f"  - ID: {platform[0]}, 이름: {platform[1]}")
            
            # 2. 삭제할 플랫폼 ID 입력
            platform_id = input("\n삭제할 플랫폼 ID를 입력하세요: ")
            
            if not platform_id:
                print("❌ 플랫폼 ID를 입력해주세요.")
                return
            
            # 3. 해당 플랫폼이 존재하는지 확인
            result = conn.execute(text("SELECT id, name FROM tb_platforms WHERE id = :id"), 
                                {"id": int(platform_id)})
            platform = result.fetchone()
            
            if not platform:
                print(f"❌ ID {platform_id}인 플랫폼이 존재하지 않습니다.")
                return
            
            print(f"삭제할 플랫폼: ID {platform[0]}, 이름: {platform[1]}")
            
            # 4. 해당 플랫폼을 참조하는 리뷰가 있는지 확인
            result = conn.execute(text("SELECT COUNT(*) FROM tb_reviews WHERE platform_id = :id"), 
                                {"id": int(platform_id)})
            review_count = result.fetchone()[0]
            
            if review_count > 0:
                print(f"⚠️ 경고: 이 플랫폼을 참조하는 리뷰가 {review_count}개 있습니다.")
                confirm = input("계속 삭제하시겠습니까? (y/N): ")
                if confirm.lower() != 'y':
                    print("❌ 삭제가 취소되었습니다.")
                    return
            
            # 5. 삭제 확인
            confirm = input(f"\n정말로 플랫폼 '{platform[1]}' (ID: {platform[0]})을 삭제하시겠습니까? (y/N): ")
            if confirm.lower() != 'y':
                print("❌ 삭제가 취소되었습니다.")
                return
            
            # 6. 플랫폼 데이터 삭제
            conn.execute(text("DELETE FROM tb_platforms WHERE id = :id"), 
                        {"id": int(platform_id)})
            conn.commit()
            
            print(f"✅ 플랫폼 '{platform[1]}' (ID: {platform[0]})이 삭제되었습니다.")
            
    except Exception as e:
        print(f"❌ 데이터 삭제 실패: {e}")
        raise
    finally:
        engine.dispose()

def delete_individual_review():
    """개별 리뷰 데이터 삭제"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== 개별 리뷰 데이터 삭제 ===")
            
            # 1. 현재 리뷰 데이터 확인
            result = conn.execute(text("""
                SELECT r.id, r.reviewer, r.content[:50], p.name as platform_name
                FROM tb_reviews r
                LEFT JOIN tb_platforms p ON r.platform_id = p.id
                ORDER BY r.id
            """))
            reviews = result.fetchall()
            
            if not reviews:
                print("❌ tb_reviews 테이블에 데이터가 없습니다.")
                return
            
            print(f"현재 리뷰 개수: {len(reviews)}")
            for review in reviews:
                print(f"  - ID: {review[0]}, 리뷰어: {review[1]}, 플랫폼: {review[3]}")
                print(f"    내용: {review[2]}...")
            
            # 2. 삭제할 리뷰 ID 입력
            review_id = input("\n삭제할 리뷰 ID를 입력하세요: ")
            
            if not review_id:
                print("❌ 리뷰 ID를 입력해주세요.")
                return
            
            # 3. 해당 리뷰가 존재하는지 확인
            result = conn.execute(text("""
                SELECT r.id, r.reviewer, r.content, p.name as platform_name
                FROM tb_reviews r
                LEFT JOIN tb_platforms p ON r.platform_id = p.id
                WHERE r.id = :id
            """), {"id": int(review_id)})
            review = result.fetchone()
            
            if not review:
                print(f"❌ ID {review_id}인 리뷰가 존재하지 않습니다.")
                return
            
            print(f"삭제할 리뷰:")
            print(f"  - ID: {review[0]}")
            print(f"  - 리뷰어: {review[1]}")
            print(f"  - 플랫폼: {review[3]}")
            print(f"  - 내용: {review[2][:100]}...")
            
            # 4. 삭제 확인
            confirm = input(f"\n정말로 이 리뷰를 삭제하시겠습니까? (y/N): ")
            if confirm.lower() != 'y':
                print("❌ 삭제가 취소되었습니다.")
                return
            
            # 5. 리뷰 데이터 삭제
            conn.execute(text("DELETE FROM tb_reviews WHERE id = :id"), 
                        {"id": int(review_id)})
            conn.commit()
            
            print(f"✅ 리뷰 (ID: {review_id})이 삭제되었습니다.")
            
    except Exception as e:
        print(f"❌ 데이터 삭제 실패: {e}")
        raise
    finally:
        engine.dispose()

def delete_individual_store():
    """개별 스토어 데이터 삭제"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== 개별 스토어 데이터 삭제 ===")
            
            # 1. 현재 스토어 데이터 확인
            result = conn.execute(text("SELECT id, name FROM tb_stores ORDER BY id"))
            stores = result.fetchall()
            
            if not stores:
                print("❌ tb_stores 테이블에 데이터가 없습니다.")
                return
            
            print(f"현재 스토어 개수: {len(stores)}")
            for store in stores:
                print(f"  - ID: {store[0]}, 이름: {store[1]}")
            
            # 2. 삭제할 스토어 ID 입력
            store_id = input("\n삭제할 스토어 ID를 입력하세요: ")
            
            if not store_id:
                print("❌ 스토어 ID를 입력해주세요.")
                return
            
            # 3. 해당 스토어가 존재하는지 확인
            result = conn.execute(text("SELECT id, name FROM tb_stores WHERE id = :id"), 
                                {"id": int(store_id)})
            store = result.fetchone()
            
            if not store:
                print(f"❌ ID {store_id}인 스토어가 존재하지 않습니다.")
                return
            
            print(f"삭제할 스토어: ID {store[0]}, 이름: {store[1]}")
            
            # 4. 해당 스토어를 참조하는 리뷰가 있는지 확인
            result = conn.execute(text("SELECT COUNT(*) FROM tb_reviews WHERE store_id = :id"), 
                                {"id": int(store_id)})
            review_count = result.fetchone()[0]
            
            if review_count > 0:
                print(f"⚠️ 경고: 이 스토어를 참조하는 리뷰가 {review_count}개 있습니다.")
                confirm = input("계속 삭제하시겠습니까? (y/N): ")
                if confirm.lower() != 'y':
                    print("❌ 삭제가 취소되었습니다.")
                    return
            
            # 5. 삭제 확인
            confirm = input(f"\n정말로 스토어 '{store[1]}' (ID: {store[0]})을 삭제하시겠습니까? (y/N): ")
            if confirm.lower() != 'y':
                print("❌ 삭제가 취소되었습니다.")
                return
            
            # 6. 스토어 데이터 삭제
            conn.execute(text("DELETE FROM tb_stores WHERE id = :id"), 
                        {"id": int(store_id)})
            conn.commit()
            
            print(f"✅ 스토어 '{store[1]}' (ID: {store[0]})이 삭제되었습니다.")
            
    except Exception as e:
        print(f"❌ 데이터 삭제 실패: {e}")
        raise
    finally:
        engine.dispose()

def delete_platforms():
    """tb_platforms 테이블의 모든 데이터 삭제"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== tb_platforms 테이블 데이터 삭제 ===")
            
            # 1. 현재 플랫폼 데이터 확인
            result = conn.execute(text("SELECT id, name FROM tb_platforms ORDER BY id"))
            platforms = result.fetchall()
            
            if not platforms:
                print("❌ tb_platforms 테이블에 데이터가 없습니다.")
                return
            
            print(f"현재 플랫폼 개수: {len(platforms)}")
            for platform in platforms:
                print(f"  - ID: {platform[0]}, 이름: {platform[1]}")
            
            # 2. 삭제 확인
            confirm = input("\n정말로 모든 플랫폼 데이터를 삭제하시겠습니까? (y/N): ")
            if confirm.lower() != 'y':
                print("❌ 삭제가 취소되었습니다.")
                return
            
            # 3. 플랫폼 데이터 삭제
            conn.execute(text("DELETE FROM tb_platforms"))
            conn.commit()
            
            print("✅ tb_platforms 테이블의 모든 데이터가 삭제되었습니다.")
            
            # 4. 삭제 결과 확인
            result = conn.execute(text("SELECT COUNT(*) FROM tb_platforms"))
            count = result.fetchone()[0]
            print(f"현재 tb_platforms 테이블 데이터 개수: {count}")
            
    except Exception as e:
        print(f"❌ 데이터 삭제 실패: {e}")
        raise
    finally:
        engine.dispose()

def delete_reviews():
    """tb_reviews 테이블의 모든 데이터 삭제"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== tb_reviews 테이블 데이터 삭제 ===")
            
            # 1. 현재 리뷰 데이터 확인
            result = conn.execute(text("SELECT COUNT(*) FROM tb_reviews"))
            count = result.fetchone()[0]
            
            if count == 0:
                print("❌ tb_reviews 테이블에 데이터가 없습니다.")
                return
            
            print(f"현재 리뷰 개수: {count}")
            
            # 2. 삭제 확인
            confirm = input("\n정말로 모든 리뷰 데이터를 삭제하시겠습니까? (y/N): ")
            if confirm.lower() != 'y':
                print("❌ 삭제가 취소되었습니다.")
                return
            
            # 3. 리뷰 데이터 삭제
            conn.execute(text("DELETE FROM tb_reviews"))
            conn.commit()
            
            print("✅ tb_reviews 테이블의 모든 데이터가 삭제되었습니다.")
            
            # 4. 삭제 결과 확인
            result = conn.execute(text("SELECT COUNT(*) FROM tb_reviews"))
            count = result.fetchone()[0]
            print(f"현재 tb_reviews 테이블 데이터 개수: {count}")
            
    except Exception as e:
        print(f"❌ 데이터 삭제 실패: {e}")
        raise
    finally:
        engine.dispose()

def delete_stores():
    """tb_stores 테이블의 모든 데이터 삭제"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== tb_stores 테이블 데이터 삭제 ===")
            
            # 1. 현재 스토어 데이터 확인
            result = conn.execute(text("SELECT id, name FROM tb_stores ORDER BY id"))
            stores = result.fetchall()
            
            if not stores:
                print("❌ tb_stores 테이블에 데이터가 없습니다.")
                return
            
            print(f"현재 스토어 개수: {len(stores)}")
            for store in stores:
                print(f"  - ID: {store[0]}, 이름: {store[1]}")
            
            # 2. 삭제 확인
            confirm = input("\n정말로 모든 스토어 데이터를 삭제하시겠습니까? (y/N): ")
            if confirm.lower() != 'y':
                print("❌ 삭제가 취소되었습니다.")
                return
            
            # 3. 스토어 데이터 삭제
            conn.execute(text("DELETE FROM tb_stores"))
            conn.commit()
            
            print("✅ tb_stores 테이블의 모든 데이터가 삭제되었습니다.")
            
            # 4. 삭제 결과 확인
            result = conn.execute(text("SELECT COUNT(*) FROM tb_stores"))
            count = result.fetchone()[0]
            print(f"현재 tb_stores 테이블 데이터 개수: {count}")
            
    except Exception as e:
        print(f"❌ 데이터 삭제 실패: {e}")
        raise
    finally:
        engine.dispose()

def delete_all_data():
    """모든 테이블의 데이터 삭제"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== 모든 테이블 데이터 삭제 ===")
            
            # 1. 현재 데이터 상태 확인
            result = conn.execute(text("SELECT COUNT(*) FROM tb_reviews"))
            review_count = result.fetchone()[0]
            
            result = conn.execute(text("SELECT COUNT(*) FROM tb_platforms"))
            platform_count = result.fetchone()[0]
            
            result = conn.execute(text("SELECT COUNT(*) FROM tb_stores"))
            store_count = result.fetchone()[0]
            
            print(f"현재 데이터 상태:")
            print(f"  - 리뷰: {review_count}개")
            print(f"  - 플랫폼: {platform_count}개")
            print(f"  - 스토어: {store_count}개")
            
            # 2. 삭제 확인
            confirm = input("\n정말로 모든 데이터를 삭제하시겠습니까? (y/N): ")
            if confirm.lower() != 'y':
                print("❌ 삭제가 취소되었습니다.")
                return
            
            # 3. 모든 데이터 삭제 (순서 중요: 외래키 제약조건 때문)
            print("리뷰 데이터 삭제 중...")
            conn.execute(text("DELETE FROM tb_reviews"))
            
            print("플랫폼 데이터 삭제 중...")
            conn.execute(text("DELETE FROM tb_platforms"))
            
            print("스토어 데이터 삭제 중...")
            conn.execute(text("DELETE FROM tb_stores"))
            
            conn.commit()
            
            print("✅ 모든 테이블의 데이터가 삭제되었습니다.")
            
    except Exception as e:
        print(f"❌ 데이터 삭제 실패: {e}")
        raise
    finally:
        engine.dispose()

def show_current_data():
    """현재 데이터베이스 상태 확인"""
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    
    try:
        with engine.connect() as conn:
            print("=== 현재 데이터베이스 상태 ===")
            
            # 리뷰 데이터
            result = conn.execute(text("SELECT COUNT(*) FROM tb_reviews"))
            review_count = result.fetchone()[0]
            print(f"리뷰: {review_count}개")
            
            if review_count > 0:
                result = conn.execute(text("""
                    SELECT r.id, r.reviewer, r.content[:50], p.name as platform_name
                    FROM tb_reviews r
                    LEFT JOIN tb_platforms p ON r.platform_id = p.id
                    ORDER BY r.id
                    LIMIT 5
                """))
                reviews = result.fetchall()
                for review in reviews:
                    print(f"  - ID: {review[0]}, 리뷰어: {review[1]}, 플랫폼: {review[3]}")
                    print(f"    내용: {review[2]}...")
            
            # 플랫폼 데이터
            result = conn.execute(text("SELECT COUNT(*) FROM tb_platforms"))
            platform_count = result.fetchone()[0]
            print(f"\n플랫폼: {platform_count}개")
            
            if platform_count > 0:
                result = conn.execute(text("SELECT id, name FROM tb_platforms ORDER BY id"))
                platforms = result.fetchall()
                for platform in platforms:
                    print(f"  - ID: {platform[0]}, 이름: {platform[1]}")
            
            # 스토어 데이터
            result = conn.execute(text("SELECT COUNT(*) FROM tb_stores"))
            store_count = result.fetchone()[0]
            print(f"\n스토어: {store_count}개")
            
            if store_count > 0:
                result = conn.execute(text("SELECT id, name FROM tb_stores ORDER BY id"))
                stores = result.fetchall()
                for store in stores:
                    print(f"  - ID: {store[0]}, 이름: {store[1]}")
            
    except Exception as e:
        print(f"❌ 데이터 확인 실패: {e}")
        raise
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("=== 데이터베이스 삭제 도구 ===")
    print("=== 개별 삭제 ===")
    print("1. 개별 플랫폼 데이터 삭제")
    print("2. 개별 리뷰 데이터 삭제")
    print("3. 개별 스토어 데이터 삭제")
    print("=== 일괄 삭제 ===")
    print("4. tb_platforms 테이블 데이터 삭제")
    print("5. tb_reviews 테이블 데이터 삭제")
    print("6. tb_stores 테이블 데이터 삭제")
    print("7. 모든 테이블 데이터 삭제")
    print("=== 기타 ===")
    print("8. 현재 데이터베이스 상태 확인")
    
    choice = input("\n선택하세요 (1-8): ")
    
    if choice == "1":
        delete_individual_platform()
    elif choice == "2":
        delete_individual_review()
    elif choice == "3":
        delete_individual_store()
    elif choice == "4":
        delete_platforms()
    elif choice == "5":
        delete_reviews()
    elif choice == "6":
        delete_stores()
    elif choice == "7":
        delete_all_data()
    elif choice == "8":
        show_current_data()
    else:
        print("❌ 잘못된 선택입니다.")
