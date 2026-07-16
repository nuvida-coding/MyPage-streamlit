import streamlit as st
import pandas as pd

# --------------------------------------------------
# 1. 페이지 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title='재고 관리 시스템',
    page_icon='🗃️',
    layout='wide'
)

st.title('🗃️ 편의점 재고 관리 시스템')
# st.caption()

# --------------------------------------------------
# 2. 유틸 함수
# --------------------------------------------------
def update_inventory_data(df):
    return df

# --------------------------------------------------
# 3. 최초 실행 시 DataFrame 생성
# --------------------------------------------------
if 'inventory' not in st.session_state:
    df = pd.read_csv('./stock data.csv', index_col=0, header=0)
    # df = update_inventory_data(df)

    st.session_state.inventory = df

# session에 저장된 df 불러오기
inventory_df = st.session_state.inventory


# --------------------------------------------------
# 4. 사이드바 ()
# --------------------------------------------------


# ==================================================
# 탭 1. 재고 현황
# ==================================================
st.subheader('재고 현황')

# 요약 정보 계산 (등록 상품 수, 총 재고, 총 재고금액, 품절수)

st.divider()

st.dataframe(inventory_df)
