import os
import pandas as pd
from classify import classify_review

def load_reviews():
    """리뷰 데이터셋 로드 (reviews_sample.csv 우선 탐색)"""
    candidate_paths = [
        "../reviews_sample.csv",
        "reviews_sample.csv",
        "../reviews_labeled.csv",
        "reviews_labeled.csv",
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            col = "review_text" if "review_text" in df.columns else "review"
            return df[col].dropna().tolist()

    # 파일 미발견 시 폴백 더미 데이터 (12건)
    return [
        "배송이 하루 만에 왔어요 최고입니다.",
        "품질이 생각했던 것보다 너무 별로네요.",
        "고객센터 응대가 정말 친절하고 만족스러웠습니다.",
        "가격 대비 가성비가 훌륭합니다.",
        "포장 박스가 다 찌그러져서 왔어요.",
        "색상이 화면이랑 달라서 환불 신청합니다.",
        "마감 처리가 아주 꼼꼼해서 마음에 들어요.",
        "배송 예정일보다 3일이나 늦게 도착했습니다.",
        "문의 답변도 빠르고 서비스가 좋습니다.",
        "재구매 의사 100%입니다 품질 굿!",
        "가격이 다른 곳에 비해 조금 비싼 편이네요.",
        "제품에 스크래치가 있어서 교환 요청합니다.",
    ]

def main():
    reviews = load_reviews()
    # [요구사항] 10건 이상 실행 (15건 추출)
    target_reviews = reviews[:15]

    total = len(target_reviews)
    success_count = 0
    fail_count = 0
    category_stats = {}

    print(f"=== 고객 리뷰 자동 분류 파이프라인 시작 (총 {total}건) ===\n")

    for idx, review in enumerate(target_reviews, 1):
        print(f"[{idx}/{total}] 리뷰: {review}")
        result = classify_review(review)

        if result is None:
            print("  -> 결과: [분류 실패] 파이프라인 예외 처리로 정상 통과\n")
            fail_count += 1
            continue

        print(f"  -> 결과: [분류 성공] {result}\n")
        success_count += 1
        cat = result.get("category", "기타")
        category_stats[cat] = category_stats.get(cat, 0) + 1

    print("=" * 50)
    print("파이프라인 실행 요약:")
    print(f"처리 {success_count}건 / 실패 {fail_count}건 (총 {total}건)")
    print(f"카테고리별 정상 집계 결과: {category_stats}")
    print("=" * 50)

if __name__ == "__main__":
    main()