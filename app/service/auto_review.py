from fastapi import HTTPException
from openai import OpenAI
from app.core.config import settings

# 동기 OpenAI 클라이언트 인스턴스
client = OpenAI(api_key=settings.openai_api_key)

# 말투 매핑
TONE_MAP = {
    "정중한": "business-casual",
    "공손한": "courteous",
    "캐주얼한": "casual",
    "business-casual": "정중한",
    "courteous": "공손한",
    "casual": "캐주얼한",
}

# 말투 가이드
TONE_GUIDES = {
    "ko": {
        "정중한": """
    - 격식은 유지하되, 너무 딱딱하지 않은 말투를 사용해주세요.
    - 예시: "소중한 의견 감사합니다. 더 나은 서비스로 보답하겠습니다."
    - 문장이 끝나면 엔터처리 해서 다음 문장이 새 줄에 시작되도록 할 것.
    """,
        "공손한": """
    - 매우 격식을 갖춘 말투를 사용해주세요.
    - 예시: "귀중한 의견 진심으로 감사드립니다. 더욱 정성을 다하겠습니다."
    - 문장이 끝나면 엔터처리 해서 다음 문장이 새 줄에 시작되도록 할 것.
    """,
        "친근한": """
    - 편하고 친근한 말투로 응답해주세요.
    - 예시: "좋은 후기 고마워요! 또 놀러오세요~"
    - 문장이 끝나면 엔터처리 해서 다음 문장이 새 줄에 시작되도록 할 것.
    """,
    },
    "en": {
        "business-casual": """
    - Maintain professionalism but sound friendly and natural.
    - Example: "Thank you for your feedback. We'll keep working to improve your experience."
    """,
        "courteous": """
    - Use very polite and formal expressions.
    - Example: "We sincerely appreciate your valuable opinion and will strive to provide excellent service."
    """,
        "casual": """
    - Use a relaxed and friendly tone.
    - Example: "Thanks a lot! Hope to see you again soon :)"
    """,
    },
}


# ✅ 동기 버전: 리뷰 응답 생성
def generate_review_response(
    review_text: str, rating: int, tone: str = "정중한", language: str = "ko"
) -> str:
    try:
        tone_kr = TONE_MAP.get(tone, "정중한")
        tone_en = TONE_MAP.get(tone, "business-casual")
        tone_key = tone_kr if language == "ko" else tone_en
        tone_guide = TONE_GUIDES[language].get(tone_key, "")

# 변수가 들어가면 안됨 -> {tone}/{tone_guide} 제거바람
        system_prompt = f"""
        

        너는 숙박업소의 리뷰 담당 AI야. 고객의 리뷰와 평점을 기반으로 {tone} 말투로 응답을 생성해줘.
        응답은 반드시 다음 원칙을 지켜야 해:
        1. 고객의 감정을 공감해줄 것.
        2. 문제가 있었다면 사과할 것.
        3. 긍정적인 표현으로 마무리할 것.
        4. 이모티콘을 절대로 사용하지 않을 것.
        5. 문장이 끝나면 엔터처리 해서 다음 문장이 새 줄에 시작되도록 할 것.
        언어는 {"한국어" if language == "ko" else "영어"}로 작성해줘.
        """.strip()
        
# user_prompt = 변수 넣어도됨
        user_prompt = f"리뷰: {review_text} 평점: {rating}점"
        
        f"""다음은 {tone} 말투의 예시와 지침이야:
        {tone_guide}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("OpenAI API Error (generate):", str(e))
        raise HTTPException(status_code=500, detail="리뷰 응답 생성 중 오류 발생")


# ✅ 동기 버전: 한글 → 영어
def translate_ko2en(review_text: str) -> str:
    try:
        system_prompt = "너는 숙박업소의 리뷰 번역 담당 AI야. 고객의 한글 리뷰를 영어로 번역해줘."

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": review_text},
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("OpenAI API Error (ko2en):", str(e))
        raise HTTPException(status_code=500, detail="OpenAI 영어 번역 중 오류 발생")


# ✅ 동기 버전: 영어 → 한글
def translate_en2ko(review_text: str) -> str:
    try:
        system_prompt = "너는 숙박업소의 리뷰 번역 담당 AI야. 영어 리뷰를 한글로 번역해줘."

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": review_text},
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("OpenAI API Error (en2ko):", str(e))
        raise HTTPException(status_code=500, detail="OpenAI 한글 번역 중 오류 발생")
