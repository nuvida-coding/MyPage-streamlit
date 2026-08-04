import streamlit as st
import pandas as pd

# --------------------------------------------------
# 유틸 함수
# --------------------------------------------------
# 계산 열을 갱신하는 함수 (중복제거, 재고금액/재고상태 추가)
def update_inventory_data(df):
    # 원본 DataFrame이 직접 변경되지 않도록 복사
    df = df.copy()

    df.drop_duplicates(inplace=True)

    # 재고 금액 = 가격 × 재고
    df["재고금액"] = df["가격"] * df["재고"]

    # 기본 재고 상태
    df["재고상태"] = "정상"

    # 재고가 안전재고 이하이면 부족
    shortage_condition = df["재고"] <= df["안전재고"]
    df.loc[shortage_condition, "재고상태"] = "부족"

    # 재고가 0이면 품절
    sold_out_condition = df["재고"] == 0
    df.loc[sold_out_condition, "재고상태"] = "품절"

    return df


# --------------------------------------------------
# 페이지 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="재고 관리 시스템",
    page_icon="📦",
    layout="wide"
)

st.title("📦 편의점 재고 관리 시스템")
st.caption("상품을 조회하고 재고를 추가하거나 수정해 보세요.")

data = {
    "상품코드": [],
    "상품명": [],
    "분류": [],
    "가격": [],
    "재고": [],
    "안전재고": []
}
reset_df = pd.DataFrame(data)

if 'inventory' not in st.session_state:
    st.session_state.inventory = update_inventory_data(reset_df)
    df = st.session_state.inventory
if 'file_name' not in st.session_state:
    st.session_state.file_name = ""

df = st.session_state.inventory
file_name = st.session_state.file_name



# --------------------------------------------------
# 3. 사이드바
# --------------------------------------------------
with st.sidebar:
    st.header("⚙️ 관리 메뉴")

    csv_file = st.file_uploader('재고 파일을 선택하세요.', type=['csv'])
    if st.button("📤 선택한 파일 불러오기", use_container_width=True):
        if csv_file is None:
            st.error('먼저 csv 파일을 선택하세요.')
        else:
            try:
                uploaded_df = pd.read_csv(csv_file)

                required_columns = [
                    "상품코드",
                    "상품명",
                    "분류",
                    "가격",
                    "재고",
                    "안전재고"
                ]

                # 필요한 열이 모두 있는지 검사
                missing_columns = [column for column in required_columns if column not in uploaded_df.columns]

                if missing_columns:
                    st.error("CSV 파일에 다음 열이 없습니다: " + ", ".join(missing_columns))
                else:
                    st.session_state.inventory = update_inventory_data(uploaded_df)
                    st.session_state.file_name = csv_file.name
                    st.session_state.dupl_cnt = len(uploaded_df) - len(st.session_state.inventory)
                    st.success("파일을 불러왔습니다.")
                    csv_file = None
                    st.rerun()

            except Exception as error:
                st.error(f"파일을 읽는 중 오류가 발생했습니다: {error}")

    if st.session_state.file_name != '':
        st.write(f"등록된 파일명: {st.session_state.file_name}")
        st.write(f"등록된 상품: {len(st.session_state.inventory)}개")
        st.write(f"삭제된 중복 상품: {st.session_state.dupl_cnt}개")

    st.divider()

    # CSV 파일로 저장할 데이터 만들기
    csv_data = df.to_csv(index=False, encoding="utf-8-sig")

    st.download_button(
        label="📥 재고 데이터 다운로드",
        data=csv_data,
        file_name="inventory.csv",
        mime="text/csv",
        use_container_width=True
    )


# --------------------------------------------------
# 6. 기능별 탭 생성
# --------------------------------------------------
# tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
#     "📊 현황",
#     "🔎 재고 조회",
#     "➕ 상품 추가",
#     "✏️ 상품 수정",
#     "🚚 입출고",
#     "📝 일괄 편집"
# ])
tab1, tab2, tab3 = st.tabs([
    "📊 현황",
    "🔎 재고 조회",
    "➕ 상품 추가"
])


# ==================================================
# 탭 1. 재고 현황
# ==================================================
with tab1:
    st.subheader("재고 현황")
    if len(df) > 0:

        # 요약 정보 계산
        total_products = len(df)
        total_stock = df["재고"].sum()
        total_value = df["재고금액"].sum()

        shortage_count = len(
            df[df["재고상태"] == "부족"]
        )

        sold_out_count = len(
            df[df["재고상태"] == "품절"]
        )

        # metric 위젯 배치 (중요한 숫자 값을 카드 형태로 강조해서 보여준다)
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(
                label="등록 상품",
                value=f"{total_products}개"
            )

        with col2:
            st.metric(
                label="전체 재고",
                value=f"{total_stock}개"
            )

        with col3:
            st.metric(
                label="전체 재고 금액",
                value=f"{total_value:,}원"
            )

        with col4:
            st.metric(
                label="재고 부족",
                value=f"{shortage_count}개"
            )

        with col5:
            st.metric(
                label="품절",
                value=f"{sold_out_count}개"
            )

        st.divider()

        # left_column, right_column = st.columns([3, 2])

        # with left_column:
        #     st.markdown("#### 전체 상품 목록")

        #     st.dataframe(
        #         df,
        #         width='stretch',
        #         hide_index=True,
        #         column_config={
        #             "가격": st.column_config.NumberColumn(
        #                 "가격",
        #                 format="%d원"
        #             ),
        #             "재고금액": st.column_config.NumberColumn(
        #                 "재고금액",
        #                 format="%d원"
        #             )
        #         }
        #     )

        # with right_column:
        st.markdown("#### 분류별 재고 수량")

        category_stock = (
            df.groupby("분류")["재고"]
            .sum()
            .sort_values(ascending=False)
        )
        st.bar_chart(category_stock)


        st.divider()


        st.markdown('#### 분류별 통계')

        # 분류 선택
        selected_category = st.selectbox(
            '분류를 선택하세요.',
            sorted(df['분류'].unique())
        )

        # 선택한 분류의 데이터 조회
        category_df = df[df['분류'] == selected_category]

        # 통계 계산
        product_count = category_df['상품코드'].count()
        total_stock = category_df['재고'].sum()
        average_price = category_df['가격'].mean()
        max_price = category_df['가격'].max()
        min_price = category_df['가격'].min()


        col1, col2 = st.columns(2)
        col1.metric(
            '상품 수',
            f'{product_count}개'
        )
        col2.metric(
            '전체 재고',
            f'{total_stock}개'
        )

        col3, col4, col5 = st.columns(3)
        col3.metric(
            '평균 가격',
            f'{average_price:,.0f}원'
        )
        col4.metric(
            '최고 가격',
            f'{max_price:,}원'
        )
        col5.metric(
            '최저 가격',
            f'{min_price:,}원'
        )
        
        st.dataframe(
            category_df,
            use_container_width=True,
            hide_index=True
        )


        st.divider()


        st.markdown("#### 관리가 필요한 상품")

        warning_df = df[
            df["재고상태"].isin(["부족", "품절"])
        ]

        if len(warning_df) == 0:
            st.success("현재 재고가 부족한 상품이 없습니다.")

        else:
            st.dataframe(
                warning_df[
                    [
                        "상품코드",
                        "상품명",
                        "분류",
                        "재고",
                        "안전재고",
                        "재고상태"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )


# ==================================================
# 탭 2. 재고 조회
# ==================================================
with tab2:
    st.subheader("조건에 맞는 상품 조회")
    if len(df) > 0:
        search_col1, search_col2 = st.columns(2)

        with search_col1:
            keyword = st.text_input(
                "상품명 검색",
                placeholder="상품명의 일부를 입력하세요."
            )

            category_options = sorted(df["분류"].unique())

            selected_categories = st.multiselect(
                "분류 선택",
                options=category_options,
                default=category_options
            )

        with search_col2:
            maximum_price = int(df["가격"].max())

            price_range = st.slider(
                "가격 범위",
                min_value=0,
                max_value=maximum_price,
                value=(0, maximum_price),
                step=100
            )

            stock_status = st.radio(
                "재고 상태",
                options=["전체", "정상", "부족", "품절"],
                horizontal=True
            )

        # 원본 DataFrame 복사
        result_df = df.copy()

        # 1. 상품명 조건
        if keyword:
            name_condition = result_df["상품명"].str.contains(
                keyword,
                case=False,
                na=False
            )

            result_df = result_df[name_condition]

        # 2. 분류 조건
        category_condition = result_df["분류"].isin(
            selected_categories
        )

        result_df = result_df[category_condition]

        # 3. 가격 범위 조건
        minimum_price = price_range[0]
        maximum_price = price_range[1]

        price_condition = (
            (result_df["가격"] >= minimum_price) &
            (result_df["가격"] <= maximum_price)
        )

        result_df = result_df[price_condition]

        # 4. 재고 상태 조건
        if stock_status != "전체":
            status_condition = (
                result_df["재고상태"] == stock_status
            )

            result_df = result_df[status_condition]

        st.write(f"검색 결과: **{len(result_df)}개**")

        if len(result_df) == 0:
            st.warning("조건에 맞는 상품이 없습니다.")

        else:
            st.dataframe(
                result_df,
                use_container_width=True,
                hide_index=True
            )


# ==================================================
# 탭 3. 상품 추가
# ==================================================
with tab3:
    st.subheader("새로운 상품 등록")
    if len(df) > 0:
        # form 안의 위젯은 제출 버튼을 누를 때 한꺼번에 처리
        with st.form("add_product_form"):

            add_col1, add_col2 = st.columns(2)

            with add_col1:
                new_code = st.text_input(
                    "상품 코드",
                    placeholder="예: P009"
                )

                new_name = st.text_input(
                    "상품명",
                    placeholder="예: 딸기우유"
                )

                new_category = st.selectbox(
                    "분류",
                    options=[
                        "음료",
                        "과자",
                        "식품",
                        "유제품",
                        "생활용품",
                        "기타"
                    ]
                )

            with add_col2:
                new_price = st.number_input(
                    "가격",
                    min_value=0,
                    step=100
                )

                new_stock = st.number_input(
                    "현재 재고",
                    min_value=0,
                    step=1
                )

                new_safety_stock = st.number_input(
                    "안전 재고",
                    min_value=0,
                    step=1
                )

            add_button = st.form_submit_button(
                "상품 등록",
                use_container_width=True
            )

        if add_button:

            new_code = new_code.strip().upper()
            new_name = new_name.strip()

            # 입력값 검사
            if new_code == "" or new_name == "":
                st.error("상품 코드와 상품명을 모두 입력하세요.")

            elif new_code in df["상품코드"].values:
                st.error("이미 사용 중인 상품 코드입니다.")

            else:
                new_product = pd.DataFrame({
                    "상품코드": [new_code],
                    "상품명": [new_name],
                    "분류": [new_category],
                    "가격": [new_price],
                    "재고": [new_stock],
                    "안전재고": [new_safety_stock]
                })

                # 기존 DataFrame과 새로운 DataFrame 합치기
                updated_df = pd.concat(
                    [df, new_product],
                    ignore_index=True
                )

                updated_df = update_inventory_data(updated_df)
                st.session_state.inventory = updated_df

                st.success(f"{new_name} 상품이 등록되었습니다.")
                st.rerun()


# ==================================================
# 탭 4. 상품 정보 수정
# ==================================================
# with tab4:
#     st.subheader("상품 정보 수정")
    # if len(df) > 0:
    #     selected_code = st.selectbox(
    #         "수정할 상품 선택",
    #         options=df["상품코드"],
    #         format_func=lambda code: (
    #             f"{code} - "
    #             f"{df.loc[df['상품코드'] == code, '상품명'].iloc[0]}"
    #         )
    #     )

    #     # 선택된 상품 조회
    #     selected_condition = df["상품코드"] == selected_code
    #     selected_product = df[selected_condition].iloc[0]

    #     with st.form("update_product_form"):

    #         update_col1, update_col2 = st.columns(2)

    #         with update_col1:
    #             update_name = st.text_input(
    #                 "상품명",
    #                 value=selected_product["상품명"]
    #             )

    #             category_list = [
    #                 "음료",
    #                 "과자",
    #                 "식품",
    #                 "유제품",
    #                 "생활용품",
    #                 "기타"
    #             ]

    #             # 기존 분류가 목록에 없으면 추가
    #             if selected_product["분류"] not in category_list:
    #                 category_list.append(
    #                     selected_product["분류"]
    #                 )

    #             category_index = category_list.index(
    #                 selected_product["분류"]
    #             )

    #             update_category = st.selectbox(
    #                 "분류",
    #                 options=category_list,
    #                 index=category_index
    #             )

    #         with update_col2:
    #             update_price = st.number_input(
    #                 "가격",
    #                 min_value=0,
    #                 value=int(selected_product["가격"]),
    #                 step=100
    #             )

    #             update_safety_stock = st.number_input(
    #                 "안전 재고",
    #                 min_value=0,
    #                 value=int(selected_product["안전재고"]),
    #                 step=1
    #             )

    #         update_button = st.form_submit_button(
    #             "정보 수정",
    #             use_container_width=True
    #         )

    #     if update_button:

    #         if update_name.strip() == "":
    #             st.error("상품명을 입력하세요.")

    #         else:
    #             condition = (
    #                 st.session_state.inventory["상품코드"]
    #                 == selected_code
    #             )

    #             # 조건에 맞는 행의 특정 열 수정
    #             st.session_state.inventory.loc[
    #                 condition,
    #                 "상품명"
    #             ] = update_name.strip()

    #             st.session_state.inventory.loc[
    #                 condition,
    #                 "분류"
    #             ] = update_category

    #             st.session_state.inventory.loc[
    #                 condition,
    #                 "가격"
    #             ] = update_price

    #             st.session_state.inventory.loc[
    #                 condition,
    #                 "안전재고"
    #             ] = update_safety_stock

    #             st.session_state.inventory = update_inventory_data(
    #                 st.session_state.inventory
    #             )

    #             st.success("상품 정보가 수정되었습니다.")
    #             st.rerun()


# # ==================================================
# # 탭 5. 재고 입출고
# # ==================================================
# with tab5:
#     st.subheader("재고 입출고 처리")
#     if len(df) > 0:
    #     movement_col1, movement_col2 = st.columns(2)

    #     with movement_col1:
    #         movement_code = st.selectbox(
    #             "상품 선택",
    #             options=df["상품코드"],
    #             key="movement_product",
    #             format_func=lambda code: (
    #                 f"{code} - "
    #                 f"{df.loc[df['상품코드'] == code, '상품명'].iloc[0]}"
    #             )
    #         )

    #         movement_type = st.radio(
    #             "작업 선택",
    #             options=["입고", "출고"],
    #             horizontal=True
    #         )

    #         movement_amount = st.number_input(
    #             "수량",
    #             min_value=1,
    #             value=1,
    #             step=1
    #         )

    #     with movement_col2:
    #         movement_condition = (
    #             df["상품코드"] == movement_code
    #         )

    #         current_product = df[movement_condition].iloc[0]

    #         st.info(
    #             f"""
    #             상품명: {current_product["상품명"]}  
    #             현재 재고: {current_product["재고"]}개  
    #             안전 재고: {current_product["안전재고"]}개  
    #             재고 상태: {current_product["재고상태"]}
    #             """
    #         )

    #     if st.button(
    #         "입출고 적용",
    #         type="primary",
    #         use_container_width=True
    #     ):

    #         condition = (
    #             st.session_state.inventory["상품코드"]
    #             == movement_code
    #         )

    #         current_stock = st.session_state.inventory.loc[
    #             condition,
    #             "재고"
    #         ].iloc[0]

    #         if movement_type == "입고":
    #             st.session_state.inventory.loc[
    #                 condition,
    #                 "재고"
    #             ] = current_stock + movement_amount

    #             st.success(
    #                 f"{movement_amount}개가 입고되었습니다."
    #             )

    #         else:
    #             if movement_amount > current_stock:
    #                 st.error(
    #                     "현재 재고보다 많은 수량을 출고할 수 없습니다."
    #                 )

    #             else:
    #                 st.session_state.inventory.loc[
    #                     condition,
    #                     "재고"
    #                 ] = current_stock - movement_amount

    #                 st.success(
    #                     f"{movement_amount}개가 출고되었습니다."
    #                 )

    #         st.session_state.inventory = update_inventory_data(
    #             st.session_state.inventory
    #         )

    #         st.rerun()


# ==================================================
# 탭 6. 일괄 편집
# ==================================================
# with tab6:
#     st.subheader("표에서 직접 수정하기")
#     if len(df) > 0:
    #     st.write(
    #         "상품명, 분류, 가격, 재고, 안전재고를 표에서 직접 수정할 수 있습니다."
    #     )

    #     editable_columns = [
    #         "상품코드",
    #         "상품명",
    #         "분류",
    #         "가격",
    #         "재고",
    #         "안전재고"
    #     ]

    #     edited_df = st.data_editor(
    #         df[editable_columns],
    #         use_container_width=True,
    #         hide_index=True,
    #         disabled=["상품코드"],
    #         column_config={
    #             "가격": st.column_config.NumberColumn(
    #                 "가격",
    #                 min_value=0,
    #                 step=100,
    #                 format="%d원"
    #             ),
    #             "재고": st.column_config.NumberColumn(
    #                 "재고",
    #                 min_value=0,
    #                 step=1
    #             ),
    #             "안전재고": st.column_config.NumberColumn(
    #                 "안전재고",
    #                 min_value=0,
    #                 step=1
    #             ),
    #             "분류": st.column_config.SelectboxColumn(
    #                 "분류",
    #                 options=[
    #                     "음료",
    #                     "과자",
    #                     "식품",
    #                     "유제품",
    #                     "생활용품",
    #                     "기타"
    #                 ]
    #             )
    #         }
    #     )

    #     if st.button(
    #         "일괄 수정 내용 저장",
    #         use_container_width=True
    #     ):
    #         st.session_state.inventory = update_inventory_data(
    #             edited_df
    #         )

    #         st.success("수정 내용이 저장되었습니다.")
    #         st.rerun()