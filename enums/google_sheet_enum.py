if 1 == 1:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from enum import Enum


class StockSettingSheetEnum(Enum):
    Date = "날짜"
    Category = "카테고리"
    ProductCode = "자체상품코드"
    ProductName = "상품명"
    ProductOption = "색상/사이즈"
    SoldOutType = "품절여부\n(상품OFF-\n현재접수잡힌 상품은 취소x)"
    IsFinished = "처리여부(브,카,자사,브리치)"
    Sabangnet = "사방넷"
    SellerGo = "셀러고 처리"
    CoupangPromotion = "쿠팡 프로모션 확인"


class ModifySheetEnum(Enum):
    Date = "날짜"
    Category = "카테고리"
    ProductCode = "자체상품코드"
    ProductName = "상품명"
    DetailModify = "상세수정"
    HTMLModify = "HTML수정"
    IsFinished = "처리여부(브,카,자사,브리치)"
    Sabangnet = "사방넷"


if __name__ == "__main__":
    print(StockSettingSheetEnum.IsFinished.value)
