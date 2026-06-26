import streamlit as st

st.set_page_config(page_title='My Home', page_icon='🌿')
st.title("Hello👋🏽 I'm Heesun🌻", anchor='top', text_alignment='center')

st.image('resources/stitch.gif', caption='me')

st.header("🙋 About Me")
st.caption("Moments of Awareness")

st.write("""
읽고,  
쓰고,  
그리기 좋아하는  
생각 많은 밖순이에요🕶️
""")

books, plants = st.columns(2)
with books:
    st.subheader("요즘 읽는 책📚")
    st.markdown("""
    - 이처럼 사소한 것들 - Claire Kegan
    - 미니멀 유목민 - 박작가
    - 주홍글자 - 너새니얼 호손
    - Maus - Art Spielgelman
    """)

with plants:
    st.subheader('반려식물🌱')
    st.markdown("""
    - 해바라기
    - 스킨답서스
    - 홍콩야자
    - 테이블 야자
    """)

st.divider()


st.latex(
    r"\text{행복} \approx \text{자유} + \text{성장} + \text{연결}"
)

with st.expander("🌿Bucket List"):
    st.markdown("""
    - 내가 만든 캠핑카타고 여행하기
    - 산티아고 순례길 걷기
    - 말이랑 친구하기
    """)

st.write("🎵 오늘의 음악")

st.audio('resources/Hollow Coves - Coastline.mp3')

st.caption("Hollow Coves - Coastline")

st.image(
    "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
    caption="2020.01.13 New Zealand"
)
st.markdown("""
<style>
.stApp {
    background-color: #E8F0E5;
}
</style>
""", unsafe_allow_html=True)

st.markdown('[:material/home: 맨 위로](#top)')