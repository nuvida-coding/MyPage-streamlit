import streamlit as st

# 1. 초기화
menu_list = ['부대찌개', '닭갈비', '제육볶음', '떡볶이세트']
price_list = [12000, 14000, 13000, 10000]
if 'order_list' not in st.session_state:
    st.session_state.order_list = []
total_price = 0


# 2. 메뉴 출력 / 3. 주문 반복
st.title('🍲 한식 밀키트 키오스크')
st.subheader('메뉴판')

for i in range(len(menu_list)):
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:      # 메뉴 이름
        st.write(menu_list[i])
    with col2:      # 가격
        st.write(f'{price_list[i]}원')
    with col3:      # 버튼
        if st.button('담기', key=i):
            st.session_state.order_list.append(menu_list[i])
            st.success('장바구니에 담겼습니다.')

# 4. 결제하기
# 총 금액 계산
for item in st.session_state.order_list:
    index = menu_list.index(item)
    total_price += price_list[index]

st.subheader('결제')
st.write('주문 내역')
for item in st.session_state.order_list:
    st.write('-', item)
st.write('총 금액 :', total_price, '원')
my_money = st.number_input(
    '가지고 있는 금액을 입력하세요',
    min_value=0,
    step=1000
)

if st.button('결제하기'):
    if my_money >= total_price:
        st.success('결제가 완료되었습니다.')
    else:
        st.error('잔액이 부족합니다.')