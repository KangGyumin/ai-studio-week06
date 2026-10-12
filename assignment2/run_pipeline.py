import os
import pandas as pd
from mock_llm import MALFORMED_STATS
from classify import classify_review

def load_reviews():
    """reviews_sample.csv 탐색 및 로드"""
    paths = ["../reviews_sample.csv", "reviews_sample.csv", "../../reviews_sample.csv"]
    for p in paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            col = "review_text" if "review_text" in df.columns else "review"
            return df[col].dropna().tolist()
    raise FileNotFoundError("reviews_sample.csv 파일을 찾을 수 없습니다.")

def main():
    reviews = load_reviews()# 200건 전체 로드

    total = len(reviews)
    success_count = 0
    fail_count = 0
    stats = {}

    print(f"=== 고객 리뷰 자동 분류 파이프라인 시작 (총 {total}건) ===\n")

    for r in reviews:
        result = classify_review(r)
        if result is None:
            fail_count += 1
            continue
        
        success_count += 1
        cat = result.get("category", "기타")
        stats[cat] = stats.get(cat, 0) + 1

    # 과제 핵심 결과 출력
    print("=" * 60)
    print(" [파이프라인 실행 요약]")
    print(f" * 처리 {success_count}건 / 실패 {fail_count}건 (총 {total}건)")
    print("-" * 60)
    print(" [불량 응답 발생 및 복구 분석]")
    print(f" * 총 불량 응답 발생: {MALFORMED_STATS['bad_total']}건")
    print(f"   - 코드펜스형: {MALFORMED_STATS['code_fence']}건 (방어 1 정규화로 정상 복구)")
    print(f"   - 사족 포함형: {MALFORMED_STATS['chatter']}건 (방어 2로 안전하게 실패 처리)")
    print(f"   - 잘린 JSON형: {MALFORMED_STATS['truncated']}건 (방어 2로 안전하게 실패 처리)")
    print("-" * 60)
    print(" [핵심 분석: 실패 건수가 불량 응답 건수보다 적은 이유]")
    print(f" => 불량 응답 중 '코드펜스형({MALFORMED_STATS['code_fence']}건)'은 classify_review의 방어 1단계")
    print("    (마크다운 백틱 제거)에 의해 정상 복구되어 파싱에 성공했기 때문입니다.")
    print("=" * 60)
    print(f"카테고리별 정상 집계: {stats}\n")

if __name__ == "__main__":
    main()