import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='제주도 숙소 관리 시스템',
    page_icon='🌴',
    layout='wide'
)

st.title('🌴 제주도 숙소 관리 시스템')
st.write('조건에 맞는 숙소를 검색하고 지도에서 위치를 확인해 보세요.')

# ==================================================
# 1. 초기 데이터 만들기
# ==================================================
if 'accommodations' not in st.session_state:
    df = pd.read_csv('./accommodations.csv', index_col=0, header=0)
    st.session_state.accommodations = df

df = st.session_state.accommodations

# ==================================================
# 매물 조회 탭
# ==================================================
st.subheader('숙소 조건 검색')

# (지역, 숙소종류) - select box, (평점) - slider
col1, col2, col3 = st.columns(3)

with col1:
    selected_region = st.selectbox(
        '지역',
        ['전체'] + sorted(df['지역'].dropna().unique().tolist())
    )
with col2:
    selected_type = st.selectbox(
        '숙소 종류',
        ['전체'] + sorted(df['숙소종류'].dropna().unique().tolist())
    )
with col3:
    min_grade = st.selectbox(
        '최소 평점',
        [1, 2, 3, 4, 5],
        index=2,
        format_func=lambda grade: '⭐' * grade,
        accept_new_options=False
    )

# (1박 가격, 방 개수, 최대수용인원) - slider, (예약상태) - 체크
col1, col2, col3, col4 = st.columns(4) 
with col1:
    min_rooms = st.slider(
        '방 개수',
        min_value=2,
        max_value=15,
        value=4
    )
with col2:
    min_rooms = st.slider(
        '최대 수용 인원',
        min_value=1,
        max_value=5,
        value=2
    )
with col3:
    min_area = st.slider(
        '1박 가격(만원)',
        min_value=1,
        max_value=50,
        value=20
    )
with col4:
    move_now = st.checkbox('예약 가능한 숙소만 보기')


# ==================================================
# 검색 조건에 맞는 데이터 선택
# ==================================================
filtered_df = df.copy()

if selected_region != '전체':
    filtered_df = filtered_df[filtered_df['지역'] == selected_region]

if selected_type != '전체':
    filtered_df = filtered_df[filtered_df['숙소종류'] == selected_type]


filtered_df = filtered_df[filtered_df['평점'].round().astype(int) >= min_grade]
filtered_df = filtered_df[filtered_df['1박가격(만원)'] >= min_area]
filtered_df = filtered_df[filtered_df['방개수'] >= min_rooms]

if move_now:
    filtered_df = filtered_df[filtered_df['예약상태'] == '가능']

st.divider()

# ==================================================
# 검색 결과 - 그리드
# ==================================================
st.subheader('검색 결과')

st.metric('검색된 숙소 / 전체 숙소', f'{len(filtered_df)}개 / {len(df)}개')

if len(filtered_df) == 0:
    st.info('조건에 맞는 숙소가 없습니다.')
else:
    display_df = filtered_df.copy()

    display_df['평점'] = display_df['평점'].apply(lambda grade: '⭐' * round(grade))

    display_df.reset_index(inplace=True)    # '숙소번호'가 인덱스로 빠져있으므로 조회하고싶으면 다시 reset
    st.dataframe(display_df[['숙소번호',
                    '숙소명',
                    '지역',
                    '숙소종류',
                    '1박가격(만원)',
                    '방개수',
                    '최대수용인원',
                    '평점',
                    '예약상태']],
                hide_index=True)

# ==================================================
# 검색 결과 - 지도
# ==================================================
st.subheader('숙소 위치')

map_df = filtered_df.dropna(subset=['lat', 'lon']).copy()

missing_count = len(filtered_df) - len(map_df)

if missing_count > 0:
    st.warning(f'위치 정보가 없는 숙소 {missing_count}개는 지도에서 제외되었습니다.')

if len(map_df) > 0:
    st.map(map_df, latitude='lat', longitude='lon')
else:
    st.info('지도에 표시할 수 있는 숙소가 없습니다.')    
