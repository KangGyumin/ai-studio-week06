# mock_llm.py — 6~12주차용 모의 LLM 모듈
import random

# 불량 응답 발생 통계 추적용
MALFORMED_STATS = {
    "bad_total": 0,
    "code_fence": 0,   # 코드펜스형 (방어 1로 복구 가능)
    "chatter": 0,      # 사족형 (방어 2로 실패/제외)
    "truncated": 0     # 잘린 JSON형 (방어 2로 실패/제외)
}

def mock_llm_call(system, user_message, temperature=0.2, max_tokens=500):
    """실제 API와 동일한 인터페이스를 갖는 모의 함수.
    13주차에 이 함수의 내부만 실제 Anthropic 호출로 교체한다."""

    # [과제 2 요구사항] 20% 확률로 불량 응답 반환 (택 1: 사족 포함)
    if random.random() < 0.2:
        MALFORMED_STATS["bad_total"] += 1
        bad_type = random.choice(["code_fence", "chatter", "truncated"])
        
        if bad_type == "code_fence":
            MALFORMED_STATS["code_fence"] += 1
            bad_text = '```json\n{"category": "배송", "sentiment": "긍정", "score": 4}\n```'
        elif bad_type == "chatter":
            MALFORMED_STATS["chatter"] += 1
            bad_text = '물론입니다! 분석 결과는 다음과 같습니다. {"category": "배송", "sentiment": "긍정", "score": 4}'
        else:
            MALFORMED_STATS["truncated"] += 1
            bad_text = '{"category": "배송", "sentim'

        return {
            "text": bad_text,
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 120, "output_tokens": 40}
        }
    
    reviews_keywords = {
        "배송": '{"category": "배송", "sentiment": "긍정", "score": 4}',
        "환불": '{"category": "환불", "sentiment": "부정", "score": 2}',
        "품질": '{"category": "품질", "sentiment": "긍정", "score": 5}',
    }
    for keyword, canned in reviews_keywords.items():
        if keyword in user_message:
            return {"text": canned, "stop_reason": "end_turn",
                    "usage": {"input_tokens": 120, "output_tokens": 35}}
    return {"text": '{"category": "기타", "sentiment": "중립", "score": 3}',
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 120, "output_tokens": 35}}
