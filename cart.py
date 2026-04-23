import flet as ft
import random
import pandas as pd
import os
from datetime import datetime

class SmartKiosk:
    def __init__(self):
        self.file = "sales.xlsx"

        # 상품 데이터
        self.items = [
            
            "비누", "치약", "샴푸", "린스", "바디워시", "폼클렌징", "칫솔", "수건",
        "휴지", "물티슈", "세탁세제", "섬유유연제", "주방세제", "수세미", "고무장갑",
        "쌀", "라면", "햇반", "생수", "우유", "계란", "두부", "콩나물", "시금치",
        "양파", "감자", "고구마", "사과", "바나나", "오렌지", "귤", "토마토",
        "김치", "된장", "고추장", "간장", "식용유", "참기름", "소금", "설탕",
        "커피", "차", "과자", "빵", "젤리", "초콜릿", "음료수", "맥주", "소주",
        "돼지고기", "소고기", "닭고기", "생선", "오징어", "새우", "게",
        "쌀국수", "파스타", "잼", "버터", "치즈", "요거트", "아이스크림", "통조림",
        "냉동만두", "어묵", "햄", "소시지", "김", "미역", "다시마", "멸치",
        "밀가루", "부침가루", "튀김가루", "빵가루", "식초", "소스", "향신료",
        "양초", "성냥", "건전지", "전구", "쓰레기봉투", "지퍼백", "호일", "랩"
        ]

        self.price = {i: random.randint(1000, 5000) for i in self.items}
        self.stock = {i: random.randint(5, 15) for i in self.items}
        self.sales_count = {i: 0 for i in self.items}

        self.cart = {}
        self.total_sales = 0

    def main(self, page: ft.Page):
        self.page = page
        page.title = "스마트 매점 키오스크"
        page.window_width = 1000
        page.window_height = 700
        page.theme_mode = ft.ThemeMode.DARK

        self.show_home()

    # ---------------- 홈 ----------------
    def show_home(self):
        self.page.controls.clear()

        self.page.add(
            ft.Column([
                ft.Text("🛒 스마트 키오스크", size=35, weight="bold"),
                ft.Row([
                    ft.ElevatedButton("고객 모드", on_click=lambda e: self.show_customer()),
                    ft.ElevatedButton("관리자 모드", on_click=lambda e: self.show_admin())
                ], alignment="center")
            ], alignment="center", horizontal_alignment="center")
        )
        self.page.update()

    # ---------------- 고객 ----------------
    def show_customer(self):
        self.page.controls.clear()

        self.search = ft.TextField(
            hint_text="상품 검색",
            on_change=lambda e: self.render_items(e.control.value)
        )

        self.grid = ft.GridView(expand=True, runs_count=2)

        self.cart_ui = ft.Column()
        self.total_text = ft.Text("총액: 0원", size=20)

        self.render_items()
        self.update_cart()

        self.page.add(
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        self.search,
                        self.grid
                    ],
                    scroll=ft.ScrollMode.AUTO,  # ⭐ 여기에 넣기
                    expand=True),
                    expand=2
                ),

        # ✅ 오른쪽 (고정 장바구니)
                ft.Container(
                    content=ft.Column([
                        ft.Text("🛒 장바구니"),
                        ft.Container(self.cart_ui, expand=True),
                        self.total_text,
                        ft.ElevatedButton("결제", on_click=self.pay),
                        ft.TextButton("뒤로", on_click=lambda e: self.show_home())
                    ]),
                    expand=1
            )

            ],
            expand=True)
        )

    def render_items(self, keyword=""):
        self.grid.controls.clear()

        for item in self.items:
            if keyword.lower() not in item.lower():
                continue

            self.grid.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(item, weight="bold"),
                            ft.Text(f"{self.price[item]}원"),
                            ft.Text(
                                f"재고: {self.stock[item]}",
                                color="red" if self.stock[item] <= 3 else "white"
                            ),
                            ft.ElevatedButton(
                                "담기",
                                on_click=lambda e, i=item: self.add_cart(i)
                            )
                        ])
                    )
                )
            )
        self.page.update()

    def add_cart(self, item):
        if self.stock[item] <= 0:
            return

        self.stock[item] -= 1
        self.cart[item] = self.cart.get(item, 0) + 1

        self.render_items()
        self.update_cart()

    def update_cart(self):
        self.cart_ui.controls.clear()
        total = 0

        for item, cnt in self.cart.items():
            total += self.price[item] * cnt

            self.cart_ui.controls.append(
                ft.Row([
                    ft.Text(f"{item} x{cnt}"),
                    ft.IconButton(
                        icon=ft.Icons.REMOVE,
                        on_click=lambda e, i=item: self.remove_cart(i)
                    )
                ])
            )

        self.total_text.value = f"총액: {total}원"
        self.page.update()

    def remove_cart(self, item):
        self.cart[item] -= 1
        self.stock[item] += 1

        if self.cart[item] == 0:
            del self.cart[item]

        self.render_items()
        self.update_cart()

    def pay(self, e):
        if not self.cart:
            return

        total = 0

        for item, cnt in self.cart.items():
            total += self.price[item] * cnt
            self.sales_count[item] += cnt

        self.total_sales += total
        self.save_excel()

        self.cart.clear()
        self.render_items()
        self.update_cart()

    # ---------------- 관리자 ----------------
    def show_admin(self):
        self.page.controls.clear()

        top5 = sorted(self.sales_count.items(), key=lambda x: x[1], reverse=True)[:5]

        self.page.add(
            ft.Column([
                ft.Text("⚙️ 관리자 모드", size=30),

                ft.Text(f"총 매출: {self.total_sales}원"),

                ft.Text("🔥 인기상품 TOP5"),
                *[ft.Text(f"{i+1}. {name} ({cnt})") for i, (name, cnt) in enumerate(top5)],

                ft.Divider(),

                ft.Column([
                    ft.Row([
                        ft.Text(item, width=100),
                        ft.Text(f"재고:{self.stock[item]}"),
                        ft.IconButton(icon=ft.Icons.ADD, on_click=lambda e, i=item: self.change_stock(i, 1)),
                        ft.IconButton(icon=ft.Icons.REMOVE, on_click=lambda e, i=item: self.change_stock(i, -1))
                    ])
                    for item in self.items
                ]),

                ft.Row([
                    ft.TextButton("뒤로", on_click=lambda e: self.show_home())
                ])
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
            )
        )

    def change_stock(self, item, val):
        self.stock[item] += val
        self.show_admin()

    # ---------------- 엑셀 ----------------
    def save_excel(self):
        data = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        for item, cnt in self.cart.items():
            data.append({
                "시간": now,
                "상품": item,
                "수량": cnt,
                "금액": self.price[item] * cnt
            })

        df = pd.DataFrame(data)

        if not os.path.exists(self.file):
            df.to_excel(self.file, index=False)
        else:
            old = pd.read_excel(self.file)
            pd.concat([old, df]).to_excel(self.file, index=False)

# 실행
app = SmartKiosk()
ft.app(target=app.main)