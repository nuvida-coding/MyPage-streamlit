import ast
import base64
import contextlib
import html
import io
import traceback
import streamlit as st

# https://english-presentation-list.streamlit.app/


st.set_page_config(
    page_title="영어 발표 순서 정하기",
    page_icon="🎤",
    layout="wide",
)


# =========================================================
# 1. 문제 데이터
# =========================================================
INITIAL_QUEUE = ["Mike", "Jully", "Ann", "Bella", "Daniel", "Ethan"]

QUESTIONS = [
    {
        "title": "1. 이름을 알파벳 순서대로 정렬하기",
        "text": """
Mike, Jully, Ann, Bella, Daniel, Ethan이 발표 신청을 했습니다.  
먼저 이름을 <b>알파벳 오름차순</b>으로 정렬하세요.
""",
        "target": ["Ann", "Bella", "Daniel", "Ethan", "Jully", "Mike"],
        "hints": ["sort()"],
        "placeholder": "queue.sort()",
    },
    {
        "title": "2. 두 학생을 맨 뒤에 추가하기",
        "text": """
뒤 늦게 Isaac과 Chris가 추가로 발표 신청을 했습니다.  
두 학생을 <b>Isaac, Chris 순서대로 맨 뒤에</b> 추가하세요.
""",
        "target": [
            "Ann", "Bella", "Daniel", "Ethan",
            "Jully", "Mike", "Isaac", "Chris"
        ],
        "hints": ["append()"],
        "placeholder": 'queue.append("Isaac")\nqueue.append("Chris")',
    },
    {
        "title": "3. Daniel 바로 뒤에 Noah 추가하기",
        "text": """
Noah는 Daniel 바로 다음 순서에 발표하고 싶어 합니다.  
Daniel의 위치를 찾아 <b>바로 뒤에 Noah를 추가</b>하세요.
""",
        "target": [
            "Ann", "Bella", "Daniel", "Noah", "Ethan",
            "Jully", "Mike", "Isaac", "Chris"
        ],
        "hints": ["index()", "insert()"],
        "placeholder": '위치를 찾은 뒤 insert()를 사용해 보세요.',
    },
    {
        "title": "4. 발표를 취소한 학생 삭제하기",
        "text": """
Jully가 발표를 취소했습니다.  
현재 명단에서 <b>Jully를 삭제</b>하세요.
""",
        "target": [
            "Ann", "Bella", "Daniel", "Noah",
            "Ethan", "Mike", "Isaac", "Chris"
        ],
        "hints": ["remove()"],
        "placeholder": 'queue.remove("Jully")',
    },
    {
        "title": "5. 맨 뒤 학생을 Bella 앞으로 이동하기",
        "text": """
맨 뒤에 있는 학생이 Bella보다 먼저 발표하고 싶어 합니다.  
<b>맨 뒤 학생</b>을 꺼낸 뒤 <b>Bella 바로 앞으로</b> 옮기세요.
""",
        "target": [
            "Ann", "Chris", "Bella", "Daniel",
            "Noah", "Ethan", "Mike", "Isaac"
        ],
        "hints": ["pop()", "index()", "insert()"],
        "placeholder": "맨 뒤 학생을 변수에 저장한 뒤 이동해 보세요.",
    },
    {
        "title": "6. 오늘의 첫 발표자 정하기",
        "text": """
<b>알파벳 내림차순으로 3번째 학생</b>을 현재 명단에서 <b>맨 앞 순서로</b> 이동시키세요.
""",
        "target": [
            "Isaac", "Ann", "Chris", "Bella",
            "Daniel", "Noah", "Ethan", "Mike"
        ],
        "hints": ["sorted()", "remove()", "insert()"],
        "placeholder": "내림차순 리스트 → 3번째 학생 → 맨 앞으로 이동",
    },
]

AVATAR_INFO = {
    "Mike":   ("#7CC6FE", "#3B3B58", "#FFD3B6"),
    "Jully":  ("#FF9FB2", "#6D435A", "#F8CFA9"),
    "Ann":    ("#B8E0A5", "#5C4033", "#FFD7BA"),
    "Bella":  ("#D6B4FC", "#4A3F55", "#F4C7AB"),
    "Daniel": ("#FFD166", "#4B3621", "#DFAF87"),
    "Ethan":  ("#86E3CE", "#2F4858", "#F0C6A8"),
    "Isaac":  ("#FFB86B", "#443730", "#C98F65"),
    "Chris":  ("#90CAF9", "#5D4037", "#E0AC8B"),
    "Noah":   ("#C5E1A5", "#263238", "#B97A56"),
}


# =========================================================
# 2. 세션 상태
# =========================================================
if "queue" not in st.session_state:
    st.session_state.queue = INITIAL_QUEUE.copy()

if "step" not in st.session_state:
    st.session_state.step = 0

if "message" not in st.session_state:
    st.session_state.message = ""

if "message_type" not in st.session_state:
    st.session_state.message_type = "info"

if "code_version" not in st.session_state:
    st.session_state.code_version = 0

if "console_output" not in st.session_state:
    st.session_state.console_output = "코드를 실행하면 출력 결과가 여기에 표시됩니다."

if "ready_for_next" not in st.session_state:
    st.session_state.ready_for_next = False

if "pending_queue" not in st.session_state:
    st.session_state.pending_queue = None


# =========================================================
# 3. 안전한 코드 검사 및 실행
# =========================================================
ALLOWED_LIST_METHODS = {
    "sort", "append", "insert", "remove", "pop", "index", "reverse"
}
ALLOWED_FUNCTIONS = {"sorted", "len", "print"}
PROTECTED_NAMES = {"sorted", "len", "print"}


class SafeCodeValidator(ast.NodeVisitor):
    """수업에 필요한 리스트 코드만 허용합니다."""

    ALLOWED_NODES = (
        ast.Module,
        ast.Expr,
        ast.Assign,
        ast.Name,
        ast.Load,
        ast.Store,
        ast.Call,
        ast.Attribute,
        ast.Constant,
        ast.BinOp,
        ast.Add,
        ast.Sub,
        ast.Subscript,
        ast.List,
        ast.Tuple,
        ast.keyword,
        ast.UnaryOp,
        ast.USub,
    )

    def generic_visit(self, node):
        if not isinstance(node, self.ALLOWED_NODES):
            raise ValueError(
                f"이 문제에서는 {type(node).__name__} 문법을 사용할 수 없습니다."
            )
        super().generic_visit(node)

    def visit_Name(self, node):
        if node.id.startswith("_"):
            raise ValueError("밑줄로 시작하는 이름은 사용할 수 없습니다.")
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if not isinstance(target, ast.Name):
                raise ValueError("변수 하나에만 값을 저장할 수 있습니다.")
            if target.id in PROTECTED_NAMES:
                raise ValueError(f"'{target.id}'에는 새로운 값을 저장할 수 없습니다.")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if node.attr not in ALLOWED_LIST_METHODS:
            raise ValueError(f"리스트 함수 '{node.attr}'은 사용할 수 없습니다.")
        if node.attr.startswith("_"):
            raise ValueError("특수 속성에는 접근할 수 없습니다.")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id not in ALLOWED_FUNCTIONS:
                raise ValueError(f"함수 '{node.func.id}()'는 사용할 수 없습니다.")

        elif isinstance(node.func, ast.Attribute):
            if node.func.attr not in ALLOWED_LIST_METHODS:
                raise ValueError(
                    f"리스트 함수 '{node.func.attr}()'는 사용할 수 없습니다."
                )
        else:
            raise ValueError("이 형태의 함수 호출은 사용할 수 없습니다.")

        self.generic_visit(node)


def execute_student_code(code, current_queue):
    working_queue = current_queue.copy()
    output_buffer = io.StringIO()

    safe_globals = {
        "__builtins__": {},
        "sorted": sorted,
        "len": len,
        "print": print,
    }
    safe_locals = {"queue": working_queue}

    try:
        if not code.strip():
            raise ValueError("코드를 입력해 주세요.")

        tree = ast.parse(code, mode="exec")
        SafeCodeValidator().visit(tree)

        with contextlib.redirect_stdout(output_buffer):
            exec(
                compile(tree, "<student-code>", "exec"),
                safe_globals,
                safe_locals,
            )

        result_queue = safe_locals.get("queue")

        if not isinstance(result_queue, list):
            raise TypeError("queue는 리스트로 유지되어야 합니다.")

        if not all(isinstance(name, str) for name in result_queue):
            raise TypeError("명단에는 학생 이름 문자열만 들어갈 수 있습니다.")

        return result_queue, output_buffer.getvalue(), None

    except Exception:
        return working_queue, output_buffer.getvalue(), traceback.format_exc()


# =========================================================
# 4. 얼굴 이미지와 화면 구성
# =========================================================
def make_avatar_svg(name):
    shirt, hair, skin = AVATAR_INFO[name]
    initial = html.escape(name[0])

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="150" height="170"
         viewBox="0 0 150 170">
      <rect width="150" height="170" rx="26" fill="#FFFFFF"/>
      <circle cx="75" cy="70" r="46" fill="{skin}"/>
      <path d="M30 68 C30 20, 120 10, 121 70
               C108 47, 91 43, 75 43
               C57 43, 42 50, 30 68Z" fill="{hair}"/>
      <ellipse cx="58" cy="72" rx="5" ry="7" fill="#2F2F2F"/>
      <ellipse cx="92" cy="72" rx="5" ry="7" fill="#2F2F2F"/>
      <path d="M60 94 Q75 105 90 94" fill="none"
            stroke="#9A4E4E" stroke-width="4" stroke-linecap="round"/>
      <path d="M30 167 Q32 112 75 112 Q118 112 120 167Z" fill="{shirt}"/>
      <circle cx="75" cy="139" r="17" fill="rgba(255,255,255,0.72)"/>
      <text x="75" y="147" text-anchor="middle"
            font-size="24" font-family="Arial" font-weight="700"
            fill="#333333">{initial}</text>
    </svg>
    """
    encoded = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


def render_students(queue):
    cards = []
    for order, name in enumerate(queue, start=1):
        avatar = make_avatar_svg(name)
        cards.append(
            f"""
            <div class="student-card" style="animation-delay:{order * 0.05}s">
                <div class="order-badge">{order}</div>
                <img src="{avatar}" alt="{html.escape(name)} 얼굴">
                <div class="student-name">{html.escape(name)}</div>
            </div>
            """
        )

    st.html(
        f"""
        <div class="stage">
            <div class="stage-title">🎤 현재 발표 순서</div>
            <div class="student-row">
                {''.join(cards)}
            </div>
        </div>
        """
    )



st.html(
    """
    <style>
        .block-container {
            max-width: 1450px;
            padding-top: 4.5rem;
            padding-bottom: 3rem;
        }

        h1 {
            text-align: center;
        }

        .stage {
            margin: 1rem 0 1.6rem 0;
            padding: 1.1rem 1.2rem 1.4rem 1.2rem;
            border: 3px solid #292D3E;
            border-radius: 24px;
            background:
                linear-gradient(#F9F6EE 0 72%, #D8B384 72% 100%);
            box-shadow: 0 10px 0 rgba(41, 45, 62, 0.16);
            overflow-x: auto;
        }

        .stage-title {
            margin-bottom: 1rem;
            font-size: 1.25rem;
            font-weight: 800;
            color: #292D3E;
        }

        .student-row {
            display: flex;
            align-items: flex-end;
            justify-content: center;
            gap: 0.7rem;
            min-width: max-content;
        }

        .student-card {
            position: relative;
            width: 118px;
            padding: 0.55rem 0.45rem 0.65rem 0.45rem;
            border: 2px solid #292D3E;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.96);
            text-align: center;
            box-shadow: 0 5px 0 rgba(41, 45, 62, 0.18);
            animation: arrive 0.45s ease both;
        }

        .student-card img {
            display: block;
            width: 100%;
            height: 128px;
            object-fit: contain;
        }

        .student-name {
            margin-top: 0.15rem;
            font-size: 1.03rem;
            font-weight: 800;
            color: #292D3E;
        }

        .order-badge {
            position: absolute;
            top: -11px;
            left: -8px;
            width: 30px;
            height: 30px;
            border: 2px solid #292D3E;
            border-radius: 50%;
            background: #FFE66D;
            color: #292D3E;
            font-weight: 900;
            line-height: 26px;
        }

        @keyframes arrive {
            from {
                opacity: 0;
                transform: translateX(35px) translateY(-7px);
            }
            to {
                opacity: 1;
                transform: translateX(0) translateY(0);
            }
        }

        .problem-card {
            padding: 1.25rem 1.4rem;
            border: 2px solid #D9DDE8;
            border-radius: 18px;
            background: #FFFFFF;
            box-shadow: 0 5px 18px rgba(45, 50, 70, 0.07);
        }

        .problem-number {
            display: inline-block;
            margin-bottom: 0.65rem;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            background: #292D3E;
            color: white;
            font-weight: 800;
        }

        .queue-view {
            margin-top: 0.9rem;
            padding: 0.75rem 1rem;
            border-radius: 12px;
            background: #F2F4F8;
            font-family: Consolas, monospace;
            font-size: 1rem;
            overflow-x: auto;
        }

        .console-box {
            margin-top: 1rem;
            margin-bottom: 1rem;
            padding: 1rem 1.2rem;
            min-height: 95px;
            border: 2px solid #292D3E;
            border-radius: 14px;
            background: #202331;
            color: #F7F7F7;
            font-family: Consolas, "Courier New", monospace;
            font-size: 0.95rem;
            line-height: 1.5;
            white-space: pre-wrap;
            overflow-x: auto;
        }

        .console-title {
            margin-bottom: 0.5rem;
            color: #B9C1D9;
            font-family: sans-serif;
            font-size: 0.85rem;
            font-weight: 800;
        }

        .hint-box {
            margin-top: 1.4rem;
            padding: 1rem 1.2rem;
            border: 2px dashed #AAB1C5;
            border-radius: 16px;
            background: #FAFBFD;
        }

        .hint-chip {
            display: inline-block;
            margin: 0.22rem;
            padding: 0.3rem 0.75rem;
            border-radius: 999px;
            background: #E9E7FF;
            color: #403C78;
            font-family: Consolas, monospace;
            font-weight: 800;
        }

        div[data-testid="stTextArea"] textarea {
            font-family: Consolas, "Courier New", monospace;
            font-size: 1.05rem;
        }

        @media (max-width: 900px) {
            .student-card {
                width: 98px;
            }
            .student-card img {
                height: 105px;
            }
        }
    </style>
    """
    # unsafe_allow_html=True,
)

st.title("🎤 영어 발표 순서 정하기")
st.subheader("리스트 함수를 사용해 학생들을 올바른 발표 순서로 이동시켜 보세요.")

progress = st.session_state.step / len(QUESTIONS)
st.progress(progress, text=f"진행 상황: {st.session_state.step} / {len(QUESTIONS)}")

render_students(st.session_state.queue)

if st.session_state.step < len(QUESTIONS):
    question = QUESTIONS[st.session_state.step]

    st.html(
        f"""
        <div class="problem-card">
            <div class="problem-number">문제 {st.session_state.step + 1}</div>
            <h3>{question["title"]}</h3>
            <div>{question["text"]}</div>
        </div>
        """
        # unsafe_allow_html=True,
    )

    code_key = f"student_code_{st.session_state.code_version}"
    code_col, button_col = st.columns([5, 1])

    with code_col:
        student_code = st.text_area(
            "파이썬 코드 입력",
            value=f"queue = {st.session_state.queue!r}\n",
            key=code_key,
            height=145,
            placeholder="코드를 입력하세요."
        )

    with button_col:
        st.html("<br>")
        reset_clicked = st.button(
            "처음부터",
            use_container_width=True,
        )
        run_clicked = st.button(
            "▶ 코드 실행",
            type="primary",
            use_container_width=True,
        )

    if reset_clicked:
        st.session_state.queue = INITIAL_QUEUE.copy()
        st.session_state.step = 0
        st.session_state.message = ""
        st.session_state.message_type = "info"
        st.session_state.console_output = "코드를 실행하면 출력 결과가 여기에 표시됩니다."
        st.session_state.ready_for_next = False
        st.session_state.pending_queue = None
        st.session_state.code_version += 1
        st.rerun()

    if run_clicked:
        result_queue, printed_output, error_output = execute_student_code(
            student_code,
            st.session_state.queue,
        )

        if error_output is not None:
            st.session_state.console_output = (
                printed_output + error_output
            ).rstrip()
            st.session_state.pending_queue = None
            st.session_state.ready_for_next = False
            st.session_state.message = (
                "코드 실행 중 오류가 발생했습니다. "
                "아래 실행 결과에서 오류 내용을 확인해 보세요."
            )
            st.session_state.message_type = "error"

        else:
            st.session_state.console_output = (
                printed_output.rstrip()
                if printed_output
                else "(출력 없음)"
            )

            if result_queue == question["target"]:
                st.session_state.pending_queue = result_queue.copy()
                st.session_state.ready_for_next = True
                st.session_state.message = (
                    "정답입니다! 실행 결과를 확인한 뒤 다음 문제로 이동하세요. 🎉"
                )
                st.session_state.message_type = "success"
            else:
                st.session_state.pending_queue = None
                st.session_state.ready_for_next = False
                st.session_state.message = (
                    "발표 순서가 틀렸습니다."
                )
                st.session_state.message_type = "error"

    if st.session_state.message:
        if st.session_state.message_type == "success":
            st.success(st.session_state.message)
        elif st.session_state.message_type == "error":
            st.error(st.session_state.message)
        else:
            st.info(st.session_state.message)

    if st.session_state.ready_for_next:
        if st.button(
            "다음 문제 ▶",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.queue = st.session_state.pending_queue.copy()
            st.session_state.pending_queue = None
            st.session_state.ready_for_next = False
            st.session_state.step += 1
            st.session_state.message = ""
            st.session_state.message_type = "info"
            st.session_state.console_output = (
                "코드를 실행하면 출력 결과가 여기에 표시됩니다."
            )
            st.session_state.code_version += 1
            st.rerun()

    st.html(
        f"""
🖥️ 코드 실행 결과
<div class="console-box">
    {html.escape(st.session_state.console_output)}
</div>
        """
    )

    st.html(
        f"""
        <div class="hint-box">
            <strong>💡 사용할 수 있는 리스트 함수</strong><br>

            <span class="hint-chip">sorted()</span>
            <span class="hint-chip">remove()</span>
            <span class="hint-chip">append()</span>
            <span class="hint-chip">insert()</span>
            <span class="hint-chip">pop()</span>
            <span class="hint-chip">reverse()</span>
            <span class="hint-chip">sort()</span>
            <span class="hint-chip">index()</span>
            <span class="hint-chip">len()</span>

            <br><br>

            <small>
                문제의 조건을 읽고 필요한 함수를 직접 골라 사용해 보세요.
            </small>
        </div>
        """
        # unsafe_allow_html=True,
    )

else:
    st.balloons()
    st.success("6개의 문제를 모두 해결했습니다! 오늘의 발표 순서가 완성되었습니다. 🎉")
    # st.code(f"queue = {st.session_state.queue}", language="python")

    if st.button("🔄 다시 도전하기", type="primary"):
        st.session_state.queue = INITIAL_QUEUE.copy()
        st.session_state.step = 0
        st.session_state.message = ""
        st.session_state.message_type = "info"
        st.session_state.console_output = "코드를 실행하면 출력 결과가 여기에 표시됩니다."
        st.session_state.ready_for_next = False
        st.session_state.pending_queue = None
        st.session_state.code_version += 1
        st.rerun()



# 정답
# 1.
# queue.sort()

# 2.
# queue.append('Isaac')
# queue.append('Chris')

# 3.
# queue.insert(queue.index('Daniel') + 1, 'Noah')

# 4.
# queue.remove('Jully')

# 5.
# queue.insert(queue.index('Bella'), queue.pop(-1))

# 6.
# new_list = sorted(queue, reverse=True)
# queue.insert(0, queue.pop(queue.index(new_list[2])))
