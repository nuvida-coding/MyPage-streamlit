import streamlit as st

if "inp_exps" not in st.session_state:
    st.session_state.inp_exps = "555"
if "message" not in st.session_state:
    st.session_state.message = ""
if "result" not in st.session_state:
    st.session_state.result = ""

def is_operator(exp):
    return exp in '+-*/'

def add_exp(exp):
    if len(st.session_state.inp_exps) == 0 and is_operator(exp):
        st.session_state.message = '연산자는 처음에 입력할 수 없습니다.'
    elif is_operator(exp) and is_operator(st.session_state.inp_exps[-1]):
        st.session_state.message = '연산자는 연속해서 입력할 수 없습니다.'
    else:
        st.session_state.inp_exps += exp

def delete_exp():
    if len(st.session_state.inp_exps) > 0:
        st.session_state.inp_exps = st.session_state.inp_exps[:-1]

def calculate():
    try:
        # eval(): 문자열 상태의 파이썬 코드를 실행시켜준다.
        #         사용자가 문자열을 직접 입력할 수 있다면, 계산식이 아니라 다른 파이썬 코드도 실행될 수 있기 때문에 위험
        result = eval(st.session_state.inp_exps)
        st.session_state.result = str(result)
    except ZeroDivisionError:
        st.session_state.message = "0으로 나눌 수 없습니다."
    except Exception:
        st.session_state.message = "잘못된 계산식입니다."



st.title('Calculator')

st.text_input(label='expression', key='inp_exps', disabled=True, label_visibility='collapsed')
if st.session_state.message != '':
    st.error(st.session_state.message)
    st.session_state.message = ''
st.write(st.session_state.result)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button('7', key='bt_7', shortcut='7', width=50, on_click=add_exp, args=('7',))
    st.button('4', key='bt_4', shortcut='4', width=50, on_click=add_exp, args=('4',))
    st.button('1', key='bt_1', shortcut='1', width=50, on_click=add_exp, args=('1',))
    st.button('0', key='bt_0', shortcut='0', width=50, on_click=add_exp, args=('0',))
with col2:
    st.button('8', key='bt_8', shortcut='8', width=50, on_click=add_exp, args=('8',))
    st.button('5', key='bt_5', shortcut='5', width=50, on_click=add_exp, args=('5',))
    st.button('2', key='bt_2', shortcut='2', width=50, on_click=add_exp, args=('2',))
    st.button('<', key='bt_delete', shortcut='Backspace', width=50, on_click=delete_exp)
with col3:
    st.button('9', key='bt_9', shortcut='9', width=50, on_click=add_exp, args=('9',))
    st.button('6', key='bt_6', shortcut='6', width=50, on_click=add_exp, args=('6',))
    st.button('3', key='bt_3', shortcut='3', width=50, on_click=add_exp, args=('3',))
    st.button('=', key='bt_enter', shortcut='Enter', type='primary', on_click=calculate)
with col4:
    st.button('X', key='bt_multi', width=100, on_click=add_exp, args=('*',))
    st.button('/', key='bt_divide', width=100, on_click=add_exp, args=('/',))
    st.button('-', key='bt_minus', width=100, on_click=add_exp, args=('-',))
    st.button('+', key='bt_plus', width=100, on_click=add_exp, args=('+',))




