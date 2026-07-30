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
# 2. 메뉴 탭
# ==================================================
tab1, tab2, tab3 = st.tabs([
    '🔎 숙소 조회',
    '➕ 숙소 추가',
    '✏️ 숙소 수정'
])

# ==================================================
# 2-1. [숙소 조회] 탭
# ==================================================
with tab1:
    st.subheader('숙소 조건 검색')

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_region = st.selectbox(
            '지역',
            ['전체'] + REGIONS
        )
    with col2:
        selected_type = st.selectbox(
            '숙소 종류',
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
            max_value=10,
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
# 검색 결과(그리드)
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
# 검색 결과(지도)
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


# ==================================================
# 2-2. [숙소 추가] 탭
# ==================================================
with tab2:
    st.subheader('새로운 숙소 등록')

    with st.form('add_accommodation_form', clear_on_submit=True):

        new_name = st.text_input('숙소명', placeholder='예: 남원 포레스트 리조트')

        col1, col2, col3 = st.columns(3)
        with col1:
            new_region = st.selectbox('지역', REGIONS)

        with col2:
            new_type = st.selectbox('숙소 종류', STAY_TYPE)

        with col3:
            new_grade = st.number_input(
                            '평점',
                            min_value=1.0,
                            max_value=5.0,
                            value=3.0,
                            step=0.1
                        )

        col1, col2, col3 = st.columns(3)
        with col1:
            new_price = st.number_input(
                '1박 가격(만 원)',
                min_value=1,
                value=50,
                step=5
            )

        with col2:
            new_rooms = st.number_input(
                '방 개수',
                min_value=1,
                max_value=15,
                value=2,
                step=1
            )

        with col3:
            new_capacity = st.number_input(
                '최대 수용 인원',
                min_value=2,
                max_value=10,
                value=2,
                step=1
            )


        new_state = st.radio(
            '예약 상태',
            STATE,
            horizontal=True
        )


        st.write('##### 위치 정보')

        no_location = st.checkbox('위치 정보를 아직 모릅니다.')

        col1, col2 = st.columns(2)

        with col1:
            new_lat = st.number_input(
                '위도',
                value=37.5665,
                format='%.6f',
                disabled=no_location
            )

        with col2:
            new_lon = st.number_input(
                '경도',
                value=126.9780,
                format='%.6f',
                disabled=no_location
            )


        add_button = st.form_submit_button(
            '숙소 등록하기',
            use_container_width=True
        )


    if add_button:

        if new_name.strip() == '':
            st.error('숙소명을 입력해 주세요.')

        else:
            if len(df) == 0:
                new_number = 101
            else:
                max_number = df['숙소번호'].max()
                new_number = str(int(max_number[1:]) + 1)

            if no_location:
                saved_lat = None
                saved_lon = None
            else:
                saved_lat = new_lat
                saved_lon = new_lon

            new_property = {
                '숙소번호': 'J' + new_number,
                '숙소명': new_name,
                '지역': new_region,
                '숙소종류': new_type,
                '1박가격(만원)': new_price,
                '방개수': new_rooms,
                '최대수용인원': new_capacity,
                '평점': new_grade,
                '예약상태': new_state,
                'lat': saved_lat,
                'lon': saved_lon
            }

            df.loc[len(df)] = new_property

            st.session_state.airbnb = df
            df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')

            st.success(f'{new_number}번 숙소가 등록되었습니다.')


# ==================================================
# 2-3 [숙소 수정] 탭
# ==================================================
with tab3:
    st.subheader('숙소 정보 수정')

    if len(df) == 0:
        st.info('수정할 숙소가 없습니다.')

    else:
        col1, col2 = st.columns([5, 1])
        with col1:
            update_number = st.selectbox(
                '수정할 숙소',
                df['숙소번호'].tolist(),
                format_func = lambda number: (
                    f"[{number}] "
                    f"{df.loc[df['숙소번호'] == number, '숙소명'].iloc[0]}"
                ),
                label_visibility='collapsed'
            )
        with col2:
            btn_view = st.button('정보 보기', use_container_width=True)

        if btn_view:
            condition = df['숙소번호'] == update_number

            selected_property = df[condition]

            st.dataframe(
                selected_property,
                use_container_width=True,
                hide_index=True
            )

            current_index = selected_property.index[0]

            with st.form('update_property_form'):

                changed_name = st.text_input(
                    '숙소명',
                    value=df.loc[current_index, '숙소명']
                )

                col1, col2, col3 = st.columns(3)
                with col1:
                    current_region = df.loc[current_index, '지역']

                    changed_region = st.selectbox(
                        '지역',
                        REGIONS,
                        index=REGIONS.index(current_region)
                    )
                with col2:
                    current_type = df.loc[current_index, '숙소종류']
                    current_type = STAY_TYPE[0] if pd.isna(current_type) else current_type

                    changed_type = st.selectbox(
                        '숙소 종류',
                        STAY_TYPE,
                        index = STAY_TYPE.index(current_type)
                    )
                with col3:
                    changed_grade = st.number_input(
                        '평점',
                        min_value=1.0,
                        max_value=5.0,
                        value=df.loc[current_index, '평점']
                    )


                col1, col2, col3 = st.columns(3)
                with col1:
                    current_price = df.loc[current_index, '1박가격(만원)']
                    current_price = 0 if pd.isna(current_price) else int(current_price)

                    changed_price = st.number_input(
                        '1박 가격(만 원)',
                        min_value=1,
                        max_value=50,
                        value=current_price,
                        step=5
                    )
                with col2:
                    current_capacity = df.loc[current_index, '최대수용인원']
                    current_capacity = 0 if pd.isna(current_capacity) else int(current_capacity)

                    changed_capacity = st.number_input(
                        '최대 수용 인원',
                        min_value=2,
                        max_value=10,
                        value=current_capacity,
                        step=1
                    )
                with col3:
                    current_rooms = df.loc[current_index, '방개수']
                    current_rooms = 0 if pd.isna(current_rooms) else int(current_rooms)
                    
                    changed_rooms = st.number_input(
                        '방 개수',
                        min_value=1,
                        max_value=15,
                        value=current_rooms,
                        step=1
                    )

                changed_state = st.radio(
                    '예약 상태',
                    STATE,
                    index=STATE.index(df.loc[current_index, '예약상태']),
                    horizontal=True
                )

                col1, col2 = st.columns(2)
                with col1:
                    update_button = st.form_submit_button('정보 수정하기', use_container_width=True)
                    if update_button:
                        if changed_name.strip() == '':
                            st.error('숙소명을 입력해 주세요.')

                        else:
                            df.loc[condition, ['숙소명',
                                                '지역',
                                                '숙소종류',
                                                '평점',
                                                '1박가격(만원)',
                                                '최대수용인원',
                                                '방개수',
                                                '예약상태']] = [
                                                            changed_name,
                                                            changed_region,
                                                            changed_type,
                                                            changed_grade,
                                                            changed_price,
                                                            changed_capacity,
                                                            changed_rooms,
                                                            changed_state
                                                        ]

                            st.session_state.airbnb = df
                            df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')

                            st.success(f'[{update_number}] 숙소가 수정되었습니다.')
                with col2:
                    del_button = st.form_submit_button('정보 삭제하기', type='primary', use_container_width=True)
                    if del_button:
                        df.drop(current_index, inplace=True)
                        df.reset_index(drop=True, inplace=True)

                        st.session_state.airbnb = df
                        df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')

                        st.success(f'[{update_number}] 숙소가 삭제되었습니다.')
                        st.rerun()



            st.divider()
            st.subheader('위치 정보 수정')



            selected_lat = df.loc[current_index, 'lat']

            selected_lon = df.loc[current_index, 'lon']

            if pd.isna(selected_lat) or pd.isna(selected_lon):
                st.warning('위치 정보가 없는 숙소입니다.')
                default_lat = 37.5665
                default_lon = 126.9780
            else:
                default_lat = float(selected_lat)
                default_lon = float(selected_lon)


            col1, col2 = st.columns(2)
            with col1:
                changed_lat = st.number_input(
                    '위도',
                    value=default_lat,
                    format='%.6f',
                    key='changed_lat'
                )
            with col2:
                changed_lon = st.number_input(
                    '경도',
                    value=default_lon,
                    format='%.6f',
                    key='changed_lon'
                )

            col1, col2, col3, col4 = st.columns(4)
            with col3:
                loc_saved = st.button('위치 정보 저장', use_container_width=True)
                    
            with col4:
                loc_deleted = st.button('위치 정보 삭제', type='primary', use_container_width=True)

            if loc_saved:
                df.loc[condition, ['lat', 'lon']] = [changed_lat, changed_lon]
                
                st.session_state.airbnb = df
                df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')

                st.success(f'[{update_number}] 숙소의 위치정보가 수정되었습니다.')

            elif loc_deleted:
                df.loc[condition, ['lat', 'lon']] = [None, None]

                st.session_state.airbnb = df
                df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')

                st.success(f'[{update_number}] 숙소의 위치정보가 삭제되었습니다.')
                st.rerun()

