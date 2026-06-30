import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="맥도넛츠 키오스크",
    page_icon="🍩",
    layout="wide"
)

# 메뉴 데이터
MENU = {
    "도넛": {
        "오리지널 글레이즈드": {
            "price": 2000,
            "emoji": "🍩",
            "description": "달콤한 설탕 코팅이 올라간 기본 도넛"
        },
        "초코 도넛": {
            "price": 2500,
            "emoji": "🍫",
            "description": "진한 초콜릿이 올라간 도넛"
        },
        "딸기 도넛": {
            "price": 2500,
            "emoji": "🍓",
            "description": "상큼한 딸기 크림 도넛"
        },
        "크림 도넛": {
            "price": 2800,
            "emoji": "🍮",
            "description": "부드러운 크림이 가득 들어간 도넛"
        }
    },

    "음료": {
        "아메리카노": {
            "price": 3000,
            "emoji": "☕",
            "description": "깔끔하고 진한 아메리카노"
        },
        "카페라떼": {
            "price": 3500,
            "emoji": "🥛",
            "description": "고소한 우유가 들어간 카페라떼"
        },
        "딸기 스무디": {
            "price": 4500,
            "emoji": "🥤",
            "description": "시원하고 달콤한 딸기 스무디"
        },
        "오렌지 주스": {
            "price": 3500,
            "emoji": "🍊",
            "description": "상큼한 오렌지 주스"
        }
    },

    "세트 메뉴": {
        "도넛 세트": {
            "price": 4500,
            "emoji": "🍩",
            "description": "오리지널 도넛 1개 + 아메리카노"
        },
        "초코 세트": {
            "price": 5200,
            "emoji": "🍫",
            "description": "초코 도넛 1개 + 카페라떼"
        }
    }
}

# 세션 상태 초기화
if "cart" not in st.session_state:
    st.session_state.cart = {}

if "order_number" not in st.session_state:
    st.session_state.order_number = 1

if "order_message" not in st.session_state:
    st.session_state.order_message = ""


# 장바구니 추가
def add_to_cart(menu_name, price, quantity):
    if menu_name in st.session_state.cart:
        st.session_state.cart[menu_name]["quantity"] += quantity

    else:
        st.session_state.cart[menu_name] = {
            "price": price,
            "quantity": quantity
        }

    st.session_state.order_message = (
        f"{menu_name} {quantity}개가 장바구니에 추가되었습니다."
    )


# 수량 증가
def increase_quantity(menu_name):
    st.session_state.cart[menu_name]["quantity"] += 1


# 수량 감소
def decrease_quantity(menu_name):
    st.session_state.cart[menu_name]["quantity"] -= 1

    if st.session_state.cart[menu_name]["quantity"] <= 0:
        del st.session_state.cart[menu_name]


# 메뉴 삭제
def remove_menu(menu_name):
    if menu_name in st.session_state.cart:
        del st.session_state.cart[menu_name]


# 장바구니 전체 삭제
def clear_cart():
    st.session_state.cart = {}
    st.session_state.order_message = "장바구니를 비웠습니다."


# 주문 완료
def complete_order():
    if not st.session_state.cart:
        st.session_state.order_message = "주문할 메뉴를 먼저 선택해주세요."
        return

    order_number = st.session_state.order_number

    st.session_state.order_message = (
        f"주문이 완료되었습니다. 주문번호는 {order_number}번입니다."
    )

    st.session_state.order_number += 1
    st.session_state.cart = {}


# 제목
st.title("🍩 맥도넛츠 키오스크")
st.write("도넛과 음료를 주문해주세요.")

st.divider()

# 메뉴와 장바구니 영역
menu_area, cart_area = st.columns([2, 1])


# 메뉴 영역
with menu_area:
    st.header("메뉴 선택")

    selected_category = st.radio(
        "카테고리",
        list(MENU.keys()),
        horizontal=True
    )

    selected_menu = MENU[selected_category]
    menu_names = list(selected_menu.keys())

    # 메뉴를 한 줄에 2개씩 출력
    for index in range(0, len(menu_names), 2):
        columns = st.columns(2)

        for column_index in range(2):
            menu_index = index + column_index

            if menu_index >= len(menu_names):
                break

            menu_name = menu_names[menu_index]
            menu_info = selected_menu[menu_name]

            with columns[column_index]:
                st.subheader(
                    f"{menu_info['emoji']} {menu_name}"
                )

                st.write(menu_info["description"])
                st.write(f"가격: **{menu_info['price']:,}원**")

                quantity = st.number_input(
                    "수량",
                    min_value=1,
                    max_value=10,
                    value=1,
                    step=1,
                    key=f"quantity_{menu_name}"
                )

                st.button(
                    "장바구니 담기",
                    key=f"add_{menu_name}",
                    use_container_width=True,
                    on_click=add_to_cart,
                    args=(menu_name, menu_info["price"], quantity)
                )
                st.divider()


# 장바구니 영역
with cart_area:
    st.header("🛒 장바구니")

    if st.session_state.order_message:
        st.info(st.session_state.order_message)

    if not st.session_state.cart:
        st.write("장바구니가 비어 있습니다.")

    else:
        total_price = 0
        total_quantity = 0

        for menu_name, menu_info in list(
            st.session_state.cart.items()
        ):
            price = menu_info["price"]
            quantity = menu_info["quantity"]
            menu_total = price * quantity

            total_price += menu_total
            total_quantity += quantity

            st.subheader(menu_name)

            st.write(
                f"{price:,}원 × {quantity}개 = "
                f"**{menu_total:,}원**"
            )

            minus_col, quantity_col, plus_col, delete_col = st.columns(4)

            with minus_col:
                st.button(
                    "➖",
                    key=f"minus_{menu_name}",
                    on_click=decrease_quantity,
                    args=(menu_name,),
                    use_container_width=True
                )

            with quantity_col:
                st.write(f"수량: {quantity}")

            with plus_col:
                st.button(
                    "➕",
                    key=f"plus_{menu_name}",
                    on_click=increase_quantity,
                    args=(menu_name,),
                    use_container_width=True
                )

            with delete_col:
                st.button(
                    "삭제",
                    key=f"delete_{menu_name}",
                    on_click=remove_menu,
                    args=(menu_name,),
                    use_container_width=True
                )

            st.divider()

        st.write(f"총 주문 수량: **{total_quantity}개**")
        st.subheader(f"총 결제금액: {total_price:,}원")

        st.button(
            "주문 완료",
            type="primary",
            on_click=complete_order,
            use_container_width=True
        )

        st.button(
            "전체 삭제",
            on_click=clear_cart,
            use_container_width=True
        )

# # 1. 초기화
# menu_list = ['']
# price_list = [12000, 14000, 13000, 10000]
# if 'order_list' not in st.session_state:
#     st.session_state.order_list = []
# total_price = 0


# # 2. 메뉴 출력 / 3. 주문 반복
# st.title('🍲 맥도넛츠 키오스크')
# st.subheader('메뉴판')

# for i in range(len(menu_list)):
#     col1, col2, col3 = st.columns([2, 1, 1])
#     with col1:      # 메뉴 이름
#         st.write(menu_list[i])
#     with col2:      # 가격
#         st.write(f'{price_list[i]}원')
#     with col3:      # 버튼
#         if st.button('담기', key=i):
#             st.session_state.order_list.append(menu_list[i])
#             st.success('장바구니에 담겼습니다.')

# # 4. 결제하기
# # 총 금액 계산
# for item in st.session_state.order_list:
#     index = menu_list.index(item)
#     total_price += price_list[index]

# st.subheader('결제')
# st.write('주문 내역')
# for item in st.session_state.order_list:
#     st.write('-', item)
# st.write('총 금액 :', total_price, '원')
# my_money = st.number_input(
#     '가지고 있는 금액을 입력하세요',
#     min_value=0,
#     step=1000
# )

# if st.button('결제하기'):
#     if my_money >= total_price:
#         st.success('결제가 완료되었습니다.')
#     else:
#         st.error('잔액이 부족합니다.')