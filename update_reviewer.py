import requests
import json

# API 기본 URL
BASE_URL = "http://localhost:8000"

def update_reviewer():
    """리뷰어 수정 스크립트"""
    
    # 1. 로그인하여 토큰 얻기
    login_data = {
        "email": "kyeong00416@gmail.com",
        "password": "1234"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/user/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"✅ 로그인 성공, 토큰: {token[:20]}...")
        else:
            print(f"❌ 로그인 실패: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ 로그인 오류: {e}")
        return
    
    # 2. 전체 리뷰 조회하여 현재 상태 확인
    try:
        response = requests.get(f"{BASE_URL}/review/list/전체?offset=1&limit=10", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            reviews = response.json()
            print(f"✅ 현재 리뷰 개수: {len(reviews)}")
            for review in reviews:
                print(f"  - ID: {review['id']}, 리뷰어: {review['reviewer']}, 플랫폼: {review['platform']}")
        else:
            print(f"❌ 리뷰 조회 실패: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ 리뷰 조회 오류: {e}")
        return
    
    # 3. 특정 리뷰의 리뷰어 수정
    review_id = input("\n수정할 리뷰 ID를 입력하세요: ")
    new_reviewer = input("새로운 리뷰어 이름을 입력하세요: ")
    
    if not review_id or not new_reviewer:
        print("❌ 리뷰 ID와 새로운 리뷰어 이름을 모두 입력해주세요.")
        return
    
    try:
        update_data = {
            "reviewer": new_reviewer
        }
        
        response = requests.put(
            f"{BASE_URL}/review/update/{review_id}", 
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json=update_data
        )
        
        if response.status_code == 200:
            updated_review = response.json()
            print(f"✅ 리뷰어 수정 성공!")
            print(f"  - ID: {updated_review['id']}")
            print(f"  - 새로운 리뷰어: {updated_review['reviewer']}")
            print(f"  - 플랫폼: {updated_review['platform']}")
        else:
            print(f"❌ 리뷰어 수정 실패: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 리뷰어 수정 오류: {e}")

def batch_update_reviewers():
    """여러 리뷰의 리뷰어를 일괄 수정"""
    
    # 1. 로그인
    login_data = {
        "email": "kyeong00416@gmail.com",
        "password": "1234"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/user/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"✅ 로그인 성공")
        else:
            print(f"❌ 로그인 실패: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 로그인 오류: {e}")
        return
    
    # 2. 플랫폼별 리뷰어 매핑
    platform_reviewers = {
        "야놀자": ["김야놀", "박야놀", "이야놀", "최야놀", "정야놀"],
        "여기어때": ["김여기", "박여기", "이여기", "최여기", "정여기"],
        "booking.com": ["김부킹", "박부킹", "이부킹", "최부킹", "정부킹"]
    }
    
    # 3. 각 플랫폼별로 리뷰 수정
    for platform_name, reviewers in platform_reviewers.items():
        print(f"\n=== {platform_name} 플랫폼 리뷰 수정 중 ===")
        
        try:
            response = requests.get(
                f"{BASE_URL}/review/list/{platform_name}?offset=1&limit=10", 
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                reviews = response.json()
                print(f"  {platform_name} 리뷰 {len(reviews)}개 발견")
                
                for i, review in enumerate(reviews):
                    if i < len(reviewers):
                        new_reviewer = reviewers[i]
                        
                        update_data = {"reviewer": new_reviewer}
                        
                        update_response = requests.put(
                            f"{BASE_URL}/review/update/{review['id']}", 
                            headers={
                                "Authorization": f"Bearer {token}",
                                "Content-Type": "application/json"
                            },
                            json=update_data
                        )
                        
                        if update_response.status_code == 200:
                            print(f"    ✅ ID {review['id']}: {review['reviewer']} → {new_reviewer}")
                        else:
                            print(f"    ❌ ID {review['id']} 수정 실패")
                    else:
                        print(f"    ⚠️ ID {review['id']}: 리뷰어 매핑 없음")
            else:
                print(f"  ❌ {platform_name} 리뷰 조회 실패: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ {platform_name} 처리 오류: {e}")

if __name__ == "__main__":
    print("=== 리뷰어 수정 도구 ===")
    print("1. 개별 리뷰어 수정")
    print("2. 플랫폼별 일괄 리뷰어 수정")
    
    choice = input("\n선택하세요 (1 또는 2): ")
    
    if choice == "1":
        update_reviewer()
    elif choice == "2":
        batch_update_reviewers()
    else:
        print("❌ 잘못된 선택입니다.")
