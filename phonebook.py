import flet as ft

# 연락처 클래스
class Contact:
    def __init__(self, name, email, phone, address):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    def to_string(self):
        return f"{self.name} | {self.phone} | {self.email} | {self.address}"


# 전화번호부 클래스
class PhoneBook:
    def __init__(self):
        self.contacts = []

    def add(self, contact):
        self.contacts.append(contact)

    def search(self, keyword):
        result = []
        for c in self.contacts:
            if (keyword in c.name or
                keyword in c.phone or
                keyword in c.email or
                keyword in c.address):
                result.append(c)
        return result

    def get_all(self):
        return self.contacts


# Flet UI
def main(page: ft.Page):
    page.title = "📱 전화번호부"
    page.window_width = 400
    page.window_height = 600

    phonebook = PhoneBook()

    # 입력창
    name = ft.TextField(label="이름")
    phone = ft.TextField(label="전화번호")
    email = ft.TextField(label="이메일")
    address = ft.TextField(label="주소")

    search_box = ft.TextField(label="검색")

    result_area = ft.Column(scroll="auto", height=300)

    # 연락처 추가
    def add_contact(e):
        if not name.value:
            result_area.controls.append(ft.Text("이름은 필수입니다!", color="red"))
        else:
            c = Contact(name.value, email.value, phone.value, address.value)
            phonebook.add(c)

            result_area.controls.append(ft.Text("저장 완료!", color="green"))

            name.value = ""
            phone.value = ""
            email.value = ""
            address.value = ""

        page.update()

    # 전체 조회
    def show_all(e):
        result_area.controls.clear()

        for c in phonebook.get_all():
            result_area.controls.append(ft.Text(c.to_string()))

        page.update()

    # 검색
    def search_contact(e):
        result_area.controls.clear()

        keyword = search_box.value
        results = phonebook.search(keyword)

        if results:
            for c in results:
                result_area.controls.append(ft.Text(c.to_string()))
        else:
            result_area.controls.append(ft.Text("검색 결과 없음", color="red"))

        page.update()

    page.add(
        ft.Column([
            ft.Text("전화번호부", size=25, weight="bold"),

            name,
            phone,
            email,
            address,

            ft.Row([
                ft.ElevatedButton("추가", on_click=add_contact),
                ft.ElevatedButton("전체조회", on_click=show_all),
            ]),

            search_box,
            ft.ElevatedButton("검색", on_click=search_contact),

            ft.Divider(),
            result_area
        ])
    )


ft.app(target=main)