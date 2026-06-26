import streamlit as st

st.title("📝 Todo List")

# todo 목록을 저장할 공간 만들기
if "todos" not in st.session_state:
    st.session_state.todos = []

# 할 일 입력
todo = st.text_input("할 일을 입력하세요", placeholder='예: 코딩 숙제하기')

# 추가 버튼
if st.button("추가하기"):
    if todo:
        st.session_state.todos.append({
            "text": todo,
            "done": False
        })
        st.success("할 일이 추가되었습니다.")
    else:
        st.warning("할 일을 입력해주세요.")

st.divider()

st.subheader("오늘의 할 일")

# todo 목록 출력
for i, item in enumerate(st.session_state.todos):
    checked = st.checkbox(
        item["text"],
        value=item["done"],
        key=f"todo_{i}"
    )

    st.session_state.todos[i]["done"] = checked

st.divider()

# 완료 개수 계산
done_count = 0

for item in st.session_state.todos:
    if item["done"]:
        done_count += 1

total_count = len(st.session_state.todos)

st.write(f"완료한 일: {done_count}개 / {total_count}개")

if total_count == 0:
    st.info("아직 등록된 할 일이 없습니다.")
elif done_count == total_count:
    st.success("오늘 할 일을 모두 완료했어요!")
elif done_count >= total_count / 2:
    st.info("좋아요. 절반 이상 완료했어요.")
else:
    st.warning("아직 할 일이 많이 남았어요.")