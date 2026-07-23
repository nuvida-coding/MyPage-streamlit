import pandas as pd
import streamlit as st

CSV_PATH = './airbnb.csv'


# ==================================================
# 1. 초기 데이터 만들기
# ==================================================
if 'airbnb' not in st.session_state:
    df = pd.read_csv(CSV_PATH, header=0)
    st.session_state.airbnb = df

df = st.session_state.airbnb

SORT_TYPE = {
    '1박가격 낮은순': {'label': '1박가격(만원)', 'ascending': True},
    '1박가격 높은순': {'label': '1박가격(만원)', 'ascending': False},
    '평점 낮은순': {'label': '평점', 'ascending': True},
    '평점 높은순': {'label': '평점', 'ascending': False}
}
REGIONS = [
    '제주시',
    '애월읍',
    '한림읍',
    '한경면',
    '조천읍',
    '구좌읍',
    '우도면',
    '서귀포시',
    '중문동',
    '대정읍',
    '안덕면',
    '남원읍',
    '표선면',
    '성산읍'
]
STAY_TYPE = ['리조트', '독채', '호텔', '한옥스테이', '펜션', '게스트하우스']
STATE = ['가능', '불가능']

# ==================================================
# 유틸
# ==================================================
def result_sort(df, sort_type):
    return df.sort_values(by=sort_type['label'], ascending=sort_type['ascending'])






st.set_page_config(
    page_title='제주도 숙소 관리 시스템',
    page_icon='🌴',
    layout='wide'
)

st.title('🌴 제주도 숙소 관리 시스템')
st.write('조건에 맞는 숙소를 검색하고 지도에서 위치를 확인해 보세요.')

# ==================================================
# 숙소 조회 탭
# ==================================================
st.subheader('숙소 조건 검색')

# (지역, 숙소종류) - select box, (평점) - slider
col1, col2, col3 = st.columns(3)

with col1:
    selected_region = st.selectbox(
        '지역',
        # ['전체'] + sorted(df['지역'].dropna().unique().tolist())
        ['전체'] + REGIONS
    )
with col2:
    selected_type = st.selectbox(
        '숙소 종류',
        # ['전체'] + sorted(df['숙소종류'].dropna().unique().tolist())
        ['전체'] + STAY_TYPE
    )
with col3:
    min_grade = st.selectbox(
        '최소 평점',
        [1, 2, 3, 4, 5],
        index=2,
        format_func=lambda grade: '⭐' * grade,
        accept_new_options=False,
        filter_mode=None
    )

# (1박 가격, 방 개수, 최대수용인원) - slider, (예약상태) - 체크
col1, col2, col3, col4 = st.columns(4) 
with col1:
    min_rooms = st.slider(
        '최소 방 개수',
        min_value=1,
        max_value=15,
        value=4
    )
with col2:
    min_capacity = st.slider(
        '최대 수용 인원',
        min_value=2,
        max_value=5,
        value=2
    )
with col3:
    max_price = st.slider(
        '최대 1박 가격(만원)',
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
filtered_df = filtered_df[filtered_df['1박가격(만원)'] <= max_price]
filtered_df = filtered_df[filtered_df['방개수'] >= min_rooms]
filtered_df = filtered_df[filtered_df['최대수용인원'] >= min_capacity]

if move_now:
    filtered_df = filtered_df[filtered_df['예약상태'] == STATE[0]]

st.divider()

# ==================================================
# 검색 결과 - 그리드
# ==================================================
st.subheader('검색 결과')

col1, col2 = st.columns([3, 1])

with col1:
    st.metric('검색된 숙소 / 전체 숙소', f'{len(filtered_df)}개 / {len(df)}개')
with col2:
    selected_sort = st.selectbox(
        '정렬 기준',
        SORT_TYPE.keys(),
        filter_mode=None
    )

filtered_df = result_sort(filtered_df, SORT_TYPE[selected_sort])

if len(filtered_df) == 0:
    st.info('조건에 맞는 숙소가 없습니다.')
else:
    display_df = filtered_df.copy()

    display_df['평점'] = display_df['평점'].apply(lambda grade: '⭐' * round(grade))
    
    # display_df.reset_index(inplace=True)    # '숙소번호'가 인덱스로 빠져있으므로 조회하고싶으면 다시 reset
    st.dataframe(display_df[['숙소번호',
                    '숙소명',
                    '지역',
                    '숙소종류',
                    '방개수',
                    '최대수용인원',
                    '1박가격(만원)',
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
