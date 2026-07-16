import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='부동산 매물 관리',
    page_icon='🏠',
    layout='wide'
)

st.title('🏠 부동산 매물 관리')
st.write('조건에 맞는 부동산 매물을 검색하고 지도에서 위치를 확인해 보세요.')

# ==================================================
# 1. 초기 데이터 만들기
# ==================================================
if 'properties' not in st.session_state:
    df = pd.read_csv('./properties.csv', index_col=0, header=0)
    st.session_state.properties = df

df = st.session_state.properties

# ==================================================
# 매물 조회 탭
# ==================================================
st.subheader('매물 조건 검색')

# (지역, 매물종류, 거래유형) - select box
col1, col2, col3 = st.columns(3)

with col1:
    selected_region = st.selectbox(
        '지역',
        ['전체'] + sorted(df['지역'].dropna().unique().tolist())
    )
with col2:
    selected_type = st.selectbox(
        '매물 종류',
        ['전체'] + sorted(df['매물종류'].dropna().unique().tolist())
    )
with col3:
    selected_deal = st.selectbox(
        '거래 유형',
        ['전체'] + sorted(df['거래유형'].dropna().unique().tolist())
    )

# (면적, 방 개수) - slider, (입주가능) - 체크
col1, col2, col3 = st.columns(3) 
with col1:
    min_area = st.slider(
        '최소 면적',
        min_value=10,
        max_value=100,
        value=50
    )
with col2:
    min_rooms = st.slider(
        '최소 방 개수',
        min_value=1,
        max_value=5,
        value=2
    )
with col3:
    move_now = st.checkbox('즉시 입주 가능한 매물만 보기')


# ==================================================
# 검색 조건에 맞는 데이터 선택
# ==================================================
filtered_df = df.copy()

if selected_region != '전체':
    filtered_df = filtered_df[filtered_df['지역'] == selected_region]

if selected_type != '전체':
    filtered_df = filtered_df[filtered_df['매물종류'] == selected_type]

if selected_deal != '전체':
    filtered_df = filtered_df[filtered_df['거래유형'] == selected_deal]

filtered_df = filtered_df[filtered_df['면적(㎡)'] >= min_area]
filtered_df = filtered_df[filtered_df['방개수'] >= min_rooms]

if move_now:
    filtered_df = filtered_df[filtered_df['입주가능'] == '즉시 입주']

st.divider()

# ==================================================
# 검색 결과 - 그리드
# ==================================================
st.subheader('검색 결과')

st.metric('검색된 매물 / 전체 매물', f'{len(filtered_df)}개 / {len(df)}개')

if len(filtered_df) == 0:
    st.info('조건에 맞는 매물이 없습니다.')
else:
    display_df = filtered_df.copy()

    display_df.reset_index(inplace=True)    # '매물번호'가 인덱스로 빠져있으므로 조회하고싶으면 다시 reset
    st.dataframe(display_df[['매물번호',
                    '매물명',
                    '지역',
                    '매물종류',
                    '거래유형',
                    '가격(만원)',
                    '면적(㎡)',
                    '방개수',
                    '입주가능']],
                hide_index=True)

# ==================================================
# 검색 결과 - 지도
# ==================================================
st.subheader('매물 위치')

map_df = filtered_df.dropna(subset=['lat', 'lon']).copy()

missing_count = len(filtered_df) - len(map_df)

if missing_count > 0:
    st.warning(f'위치 정보가 없는 매물 {missing_count}개는 지도에서 제외되었습니다.')

if len(map_df) > 0:
    st.map(map_df, latitude='lat', longitude='lon')
else:
    st.info('지도에 표시할 수 있는 매물이 없습니다.')    
