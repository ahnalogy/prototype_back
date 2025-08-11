import requests
import json

# API 기본 URL
BASE_URL = "http://localhost:8000"

def test_platform_filtering():
    """플랫폼별 리뷰 필터링 테스트"""
    
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
    
    # 2. 플랫폼 목록 조회
    try:
        response = requests.get(f"{BASE_URL}/platform/list", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            platforms = response.json()
            print(f"✅ 플랫폼 목록: {[p['name'] for p in platforms]}")
        else:
            print(f"❌ 플랫폼 목록 조회 실패: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 플랫폼 목록 조회 오류: {e}")
    
    # 3. 전체 리뷰 조회
    try:
        response = requests.get(f"{BASE_URL}/review/list/전체?offset=1&limit=10", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            reviews = response.json()
            print(f"✅ 전체 리뷰 개수: {len(reviews)}")
            for review in reviews:
                print(f"  - ID: {review['id']}, 플랫폼: {review['platform']}, 작성자: {review['reviewer']}")
        else:
            print(f"❌ 전체 리뷰 조회 실패: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 전체 리뷰 조회 오류: {e}")
    
    # 4. 야놀자 리뷰 조회
    try:
        response = requests.get(f"{BASE_URL}/review/list/야놀자?offset=1&limit=10", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            reviews = response.json()
            print(f"✅ 야놀자 리뷰 개수: {len(reviews)}")
            for review in reviews:
                print(f"  - ID: {review['id']}, 플랫폼: {review['platform']}, 작성자: {review['reviewer']}")
        else:
            print(f"❌ 야놀자 리뷰 조회 실패: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 야놀자 리뷰 조회 오류: {e}")
    
    # 5. 여기어때 리뷰 조회
    try:
        response = requests.get(f"{BASE_URL}/review/list/여기어때?offset=1&limit=10", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            reviews = response.json()
            print(f"✅ 여기어때 리뷰 개수: {len(reviews)}")
            for review in reviews:
                print(f"  - ID: {review['id']}, 플랫폼: {review['platform']}, 작성자: {review['reviewer']}")
        else:
            print(f"❌ 여기어때 리뷰 조회 실패: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 여기어때 리뷰 조회 오류: {e}")
    
    # 6. booking.com 리뷰 조회
    try:
        response = requests.get(f"{BASE_URL}/review/list/booking.com?offset=1&limit=10", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            reviews = response.json()
            print(f"✅ booking.com 리뷰 개수: {len(reviews)}")
            for review in reviews:
                print(f"  - ID: {review['id']}, 플랫폼: {review['platform']}, 작성자: {review['reviewer']}")
        else:
            print(f"❌ booking.com 리뷰 조회 실패: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ booking.com 리뷰 조회 오류: {e}")

if __name__ == "__main__":
    print("=== 플랫폼별 리뷰 필터링 테스트 ===")
    test_platform_filtering()
    print("=== 테스트 완료 ===")
