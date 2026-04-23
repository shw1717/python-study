import flet as ft
import random

def main(page: ft.Page):
    page.title = "마트 관리 프로그램"
    page.scroll = "auto"

    #데이터
    items = [
    "비누", "치약", "샴푸", "린스", "바디워시", "폼클렌징", "칫솔", "수건",
    "휴지", "물티슈", "세탁세제", "섬유유연제", "주방세제", "수세미", "고무장갑",
    "쌀", "라면", "햇반", "생수", "우유", "계란", "두부", "콩나물", "시금치",
    "양파", "감자", "고구마", "사과", "바나나", "오렌지", "귤", "토마토",
    "김치", "된장", "고추장", "간장", "식용유", "참기름", "소금", "설탕",
    "커피", "차", "과자", "빵", "젤리", "초콜릿", "음료수", "맥주", "소주",
    "고기(돼지고기)", "고기(소고기)", "닭고기", "생선", "오징어", "새우", "게",
    "쌀국수", "파스타", "잼", "버터", "치즈", "요거트", "아이스크림", "통조림",
    "냉동만두", "어묵", "햄", "소시지", "김", "미역", "다시마", "멸치",
    "밀가루", "부침가루", "튀김가루", "빵가루", "식초", "소스", "향신료",
    "양초", "성냥", "건전지", "전구", "쓰레기봉투", "지퍼백", "호일", "랩"
    ]

    prices = {item: random.randint(1000, 10000) for item in items}
    stock = {item: 10 for item in items}
    cart = {}
    total_sales = 0

    #출력 영역
    output = ft.Text()

    #상품 리스트 표시
    def show_items(e):
        text = "상품 목록\n"
        for i, item in enumerate(itmes):
            text += f"{i}. {item} - {prices[item]}원 (재고: {stock[item]})\n"
        output.value = text
        page.update()

    #장바구니 담기
    def add_to_cart(e):
        try:
            index = int(item_input.value)
            qty = int(qty_input.value)

            if index < 0 or index >= len(items):
                output.value = "잘못된 상품 번호"
                page.update()
                return
            
        item = items[index]

        if stock[item] < qty:
            output.value = "재고 부족"
        else:
            cart[item] = cart.get(item, 0) + qty
            stock[item] -= qty
            output.value = f" {item} {qty}개 담김"
        
        except:
        output.value = "입력 오류"

        page.update()

    #결제
    def checkout(e):
        nonlocal total_sales

        if not cart:
            output.value = "장바구니가 비어있음"
            page.update()
            return
        
        total = 0
        text = "장바구니\n"

        for item, qty in cart.items():
            cost = prices[item] * qty
            text += f"{item} x {qty} = {cost}원\n"
            total += cost

        text += f"\n총 금액: {total}원"
        total_sales += total
        cart.clear()

        output.value = text + "\n\n 결제완료"
        page.update()

    #재고 확인
    def show_stock(e):
        text = "재고 현황\n"
        for item in items:
            text += f"{item}: {stock[item]}개\n"
        output.value = text
        page.update()

    #매출 확인
    def show_sales(e):
        output.value = f"총 매출: {total_sales}원"
        page.update()

    #입력창
    item_input = ft.TextField(label="상품 번호")
    qty_input = ft.TextField(label="수량")
    
    #버튼 UI
    page.add(
        ft.Text("🛒 마트 프로그램", size=25, weight="bold"),
        ft.Row([
            ft.ElevatedButton("상품 보기", on_click=show_items),
            ft.ElevatedButton("재고 확인", on_click=show_stock),
            ft.ElevatedButton("매출 확인", on_click=show_sales),
        ]),
        ft.Row([
            item_input,
            qty_input,
            ft.ElevatedButton("장바구니 담기", on_click=add_to_cart),
        ]),
        ft.ElevatedButton("결제", on_click=checkout),
        ft.Divider(),
        output
    )


#실행
ft.app(target=main)