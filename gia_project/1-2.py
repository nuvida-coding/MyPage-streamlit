import streamlit as st
from pathlib import Path
import base64, csv

# =========================================================
# 기본 설정
# =========================================================
st.set_page_config(
    page_title="GIA | Cyber Intelligence",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent

ASSET_DIR = BASE_DIR / "assets" 
IMG_DIR = ASSET_DIR / "img"
IMG_EMO_DIR = IMG_DIR / "emo"
SOUND_DIR = ASSET_DIR / "sound"
VIDEO_DIR = ASSET_DIR / "video"

GIA_LOGO = IMG_DIR / "gia_logo.png"
INTRO_IMAGE = IMG_DIR / "1-2_intro.png"
MISSION1_IMAGE = IMG_DIR / "1-2_m1.png"
MISSION2_IMAGE = IMG_DIR / "1-2_m2.png"
AGENT_FILE = Path("agents.csv")

MISSIONS = {
    "Mission 1": "mission1_story",
    "Mission 2": "mission2_story",
}

# =========================================================
# 페이지별 영상 / 배경음악
# video 또는 bgm을 None으로 두면 해당 페이지에서는 재생하지 않습니다.
# =========================================================
PAGE_MEDIA = {
    "registered": {
        "video": None,
        "bgm": SOUND_DIR / "Engineering_2.mp3",
        "bgm_loop": True,
    },

    # "prologue": {
    #     "video": VIDEO_DIR / "sin2.mp4",
    #     "bgm": SOUND_DIR / "Engineering_2.mp3",
    #     "bgm_loop": True,
    # },

    "chapter_intro": {
        "video": None,
        "bgm": SOUND_DIR / "futuristicbutton_a_2.mp3",
        "bgm_loop": False,
    },

    "mission1_story": {
        "video": VIDEO_DIR / "sin1_change.mp4",
        "bgm": SOUND_DIR / "upbeatcorporation_2.mp3",
        "bgm_loop": True,
    },

    "mission1": {
        "video": None,
        "bgm": SOUND_DIR / "futuristicbutton_a_2.mp3",
        "bgm_loop": False,
    },

    "mission2_story": {
        "video": VIDEO_DIR / "sin1_idle.mp4",
        "bgm": SOUND_DIR / "brainTeaser_2.mp3",
        "bgm_loop": True,
    },

    "mission2": {
        "video": None,
        "bgm": SOUND_DIR / "sweepnext_2.mp3",
        "bgm_loop": False,
    },

    "epilogue": {
        "video": VIDEO_DIR / "sin2.mp4",
        "bgm": SOUND_DIR / "upbeatcorporation_2.mp3",
        "bgm_loop": True,
    },

    "ending": {
        "video": None,
        "bgm": SOUND_DIR / "ending.mp3",
        "bgm_loop": True,
    }
}

# 매핑에 없는 페이지에서 사용할 기본값
DEFAULT_VIDEO_PATH = VIDEO_DIR / "sin1_change.mp4"
DEFAULT_BGM_PATH = SOUND_DIR / "Engineering_2.mp3"

# =========================================================
# 캐릭터 감정별 이미지
# =========================================================
CHARACTER_IMAGES = {
    "Alex": {
        "idle": IMG_EMO_DIR / "alex_idle.png",
        "surprised": IMG_EMO_DIR / "alex_surprised.png",
        "worried": IMG_EMO_DIR / "alex_worried.png",
        "angry": IMG_EMO_DIR / "alex_angry.png",
        "furious": IMG_EMO_DIR / "alex_furious.png",
        "dumbfounded": IMG_EMO_DIR / "alex_dumbfounded.png",
        "sad": IMG_EMO_DIR / "alex_sad.png",
        "happy": IMG_EMO_DIR / "alex_happy.png",
        "bored": IMG_EMO_DIR / "alex_bored.png",
        "flustered": IMG_EMO_DIR / "alex_flustered.png",
        "determined": IMG_EMO_DIR / "alex_determinded.png",
        "embarrassed": IMG_EMO_DIR / "alex_embarrassed.png",
        "embarrassed2": IMG_EMO_DIR / "alex_embarrassed2.png",
        "serious": IMG_EMO_DIR / "alex_serious.png",
        "smile": IMG_EMO_DIR / "alex_smile.png",
        "smile2": IMG_EMO_DIR / "alex_smile2.png",
        "solemn": IMG_EMO_DIR / "alex_solem.png",
        "deep": IMG_EMO_DIR / "alex_deep.png",
        "eyeclosed": IMG_EMO_DIR / "alex_eyeclosed.png",
        "firmly": IMG_EMO_DIR / "alex_firmly.png",
        "introduce": IMG_EMO_DIR / "alex_introduce.png",
        "puzzled": IMG_EMO_DIR / "alex_puzzled.png",
        "sinister": IMG_EMO_DIR / "alex_sinister.png",
        "smirk": IMG_EMO_DIR / "alex_smirk.png",
        "talking": IMG_EMO_DIR / "alex_talking.png",
        "whatever": IMG_EMO_DIR / "alex_whatever.png"
    },
    "Mason": {
        "idle": IMG_EMO_DIR / "mason_idle.png",
        "surprised": IMG_EMO_DIR / "mason_surprised.png",
        "worried": IMG_EMO_DIR / "mason_worried.png",
        "angry": IMG_EMO_DIR / "mason_angry.png",
        "furious": IMG_EMO_DIR / "mason_furious.png",
        "dumbfounded": IMG_EMO_DIR / "mason_dumbfounded.png",
        "sad": IMG_EMO_DIR / "mason_sad.png",
        "happy": IMG_EMO_DIR / "mason_happy.png",
        "bored": IMG_EMO_DIR / "mason_bored.png",
        "flustered": IMG_EMO_DIR / "mason_flustered.png",
        "determined": IMG_EMO_DIR / "mason_determinded.png",
        "embarrassed": IMG_EMO_DIR / "mason_embarrassed.png",
        "serious": IMG_EMO_DIR / "mason_serious.png",
        "smile": IMG_EMO_DIR / "mason_smile.png",
        "smile2": IMG_EMO_DIR / "mason_smile2.png",
        "solemn": IMG_EMO_DIR / "mason_solem.png",
        "deep": IMG_EMO_DIR / "mason_deep.png",
        "eyeclosed": IMG_EMO_DIR / "mason_eyeclosed.png",
        "firmly": IMG_EMO_DIR / "mason_firmly.png",
        "introduce": IMG_EMO_DIR / "mason_introduce.png",
        "puzzled": IMG_EMO_DIR / "mason_puzzled.png",
        "sinister": IMG_EMO_DIR / "mason_sinister.png",
        "smirk": IMG_EMO_DIR / "mason_smirk.png",
        "talking": IMG_EMO_DIR / "mason_talking.png",
        "whatever": IMG_EMO_DIR / "mason_whatever.png"
    },
}

# 등장인물별 표현 설정
SPEAKER_COLORS = {
    "Alex": "#FFB85C",
    "Mason": "#5CC8FF",
    "SYSTEM": "#FF6464",
}

SPEAKER_ALIGNMENTS = {
    "Alex": "left",
    "Mason": "right",
    "SYSTEM": "center",
}


# =========================================================
# 전체 스타일
# =========================================================
st.html("""
<style>
    /* Streamlit 기본 UI 최소화 */
    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    .stApp {
        background:
            radial-gradient(circle at 50% 10%, rgba(11, 45, 55, 0.35), transparent 40%),
            #020607;
        color: #d8f5ee;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    /* 공통 GIA 패널 */
    .gia-panel {
        border: 1px solid rgba(85, 255, 208, 0.35);
        background: rgba(2, 11, 13, 0.88);
        box-shadow:
            0 0 0 1px rgba(85,255,208,0.05) inset,
            0 0 30px rgba(0,255,190,0.05);
        padding: 28px 32px;
        border-radius: 4px;
        font-family: Consolas, "Courier New", monospace;
    }

    .terminal-title {
        color: #62ffd3;
        letter-spacing: 0.15em;
        font-size: 13px;
        margin-bottom: 18px;
    }

    .terminal-main {
        color: #eafff8;
        font-family: Consolas, "Courier New", monospace;
        line-height: 1.9;
    }

    .terminal-dim {
        color: #7da49a;
    }

    .warning {
        color: #ff6666;
    }

    .success {
        color: #68ffbd;
    }

    .mission-title {
        font-family: Consolas, "Courier New", monospace;
        letter-spacing: .18em;
        color: #70ffe0;
        text-align: center;
        font-size: 16px;
        margin-bottom: 8px;
    }

    .mission-name {
        font-size: 32px;
        text-align: center;
        font-weight: 800;
        color: white;
        margin-bottom: 26px;
    }

    .data-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin: 24px 0;
    }

    .data-card {
        border: 1px solid rgba(98,255,211,.22);
        padding: 18px;
        background: rgba(0,0,0,.25);
        text-align: center;
    }

    .data-label {
        color: #78958e;
        font-size: 11px;
        letter-spacing: .08em;
    }

    .data-value {
        color: #eafff8;
        font-size: 22px;
        margin-top: 8px;
        font-weight: 700;
    }

    /* 입력창 */
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {
        background: rgba(0,0,0,.55);
        border: 1px solid rgba(98,255,211,.45);
        color: #eafff8;
        border-radius: 2px;
        font-family: Consolas, "Courier New", monospace;
    }

    div[data-testid="stTextInput"] label,
    div[data-testid="stNumberInput"] label {
        color: #95b7ae;
        font-family: Consolas, "Courier New", monospace;
        letter-spacing: .08em;
    }

    /* 일반 버튼 */
    div[data-testid="stButton"] button,
    div[data-testid="stFormSubmitButton"] button {
        border-radius: 2px;
        border: 1px solid rgba(98,255,211,.55);
        background: rgba(5,23,24,.92);
        color: #dffff7;
        font-family: Consolas, "Courier New", monospace;
        letter-spacing: .05em;
        transition: .15s ease;
    }

    div[data-testid="stButton"] button:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        border-color: #62ffd3;
        color: #62ffd3;
        box-shadow: 0 0 18px rgba(98,255,211,.12);
    }

    /* 오디오 컨트롤 숨기기 */
    audio {
        display: none !important;
    }

    /* 비디오 컨트롤/진행바 숨기기 */
    div[data-testid="stVideo"] video {
        pointer-events: none !important;
    }

    div[data-testid="stVideo"] video::-webkit-media-controls {
        display: none !important;
    }

    div[data-testid="stVideo"] video::-webkit-media-controls-enclosure {
        display: none !important;
    }

    div[data-testid="stVideo"] video::-webkit-media-controls-panel {
        display: none !important;
    }

    .mason-name {
        color: #5CC8FF;
    }
    .alex-name {
        color: #FFB85C;
    }
    .system-name {
        color: #FF6464;
    }

    .mission-image-wrap {
        display: grid;
        grid-template-columns: 1fr;
        margin: 24px 0;
    }

    .mission-image {
        width: 100%;
        max-height: 420px;
        object-fit: contain;
        display: block;
        margin: 0 auto;
    }

    .mission-info-card {
        border: 1px solid rgba(98,255,211,.22);
        padding: 18px;
        background: rgba(0,0,0,.25);
        font-family: Consolas, "Courier New", monospace;
        margin: 24px 0;
        text-align: center;
    }

    .mission-alert {
        border: 1px solid rgba(255,100,100,.35);
        color: #ff8a8a;
        padding: 14px 18px;
        font-family: Consolas, "Courier New", monospace;
        margin: 20px 0;
        text-align: center;
    }
</style>
""")

# =========================================================
# 세션 상태 초기화
# =========================================================
defaults = {
    "registered": False,
    "code_name": "",
    "page": "register",
    "dialogue_index": 0,
    "mission1_clear": False,
    "mission2_clear": False,
    "message": "",
    "mission_selector": "MISSION SELECT",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 스토리 데이터
# 형식: ("등장인물", "감정", "대사")
# SYSTEM은 감정값을 None으로 둡니다.
# =========================================================
# PROLOGUE_DIALOGUES = [
#     ("Alex", "happy", "접속 확인. {agent} 요원, 맞지?"),
#     ("Alex", "happy", "국제 정보 기관 Global Intelligence Agency에 온 걸 환영해!"),
#     ("Alex", "smile", "오늘부터 함께 움직이게 될 GIA 특수 정보 요원 Alex야."),
#     ("Mason", "idle", "그리고 난 Mason. 사이버 분석 담당이야."),
#     ("Mason", "smile2", "네 기록은 봤어. 코딩 실력이 꽤 좋다던데?"),
#     ("Alex", "dumbfounded", "Mason, 첫날부터 너무 부담 주지 마."),
#     ("Mason", "dumbfounded", "어차피 몇 분 뒤면 실전 들어갈 텐데 뭘."),
#     ("Alex", "idle", "{agent}. 원래라면 브리핑부터 천천히 진행해야 하는데, 상황이 바뀌었어."),
#     ("Mason", "idle", "가입 첫날부터 실전이다. 운이 좋은 건지 나쁜 건지는 모르겠지만..!"),
# ]

CHAPTER1_DIALOGUES = [
    ("SYSTEM", None, "PRIORITY ALERT\nCLASSIFIED INTELLIGENCE RECEIVED"),
    ("Alex", "idle", "조금 전 네덜란드에서 긴급 첩보가 들어왔어."),
    ("Alex", "dumbfounded", "우리가 추적하던 비밀 조직 <i><b>빌더버그</b></i>가 움직이기 시작했대."),
    ("Mason", "serious", "그들의 공격 타겟은 평화의 도시 <i><b>헤이그</b></i>. 정확히 무슨 일을 꾸미고 있는지는 아직 몰라."),
    ("Alex", "idle", "다만 한 가지는 확인했어. 빌더버그가 작전 통신에 사용하는 인공위성을 찾아냈어."),
    ("Mason", "serious", "위성 이름은... <i><b>INTELSAT</b></i>이야."),
    ("Alex", "happy", "빌더버그를 잡을 수 있는 정보가 인공위성 안에 있을지 몰라!"),
    ("Mason", "dumbfounded", "지금 바로 Intelsat 시스템에 침투할 준비를 시작하자."),
    ("SYSTEM", None, "⚠️WARNING⚠️\nINTELSAT ORBIT DEVIATION DETECTED"),
    ("Alex", "dumbfounded", "!!!"),
    ("Alex", "dumbfounded", "무슨일이야!?"),
    ("Mason", "flustered", "잠깐…… 상황이 안 좋은데.\nIntelsat 위성이 정지궤도를 벗어나고 있어!"),
    ("Alex", "dumbfounded", "해킹에 문제라도 생겼다는 말이야?"),
    ("Mason", "worried", "아니. 위성 자체의 문제야. 연료가 거의 소진된 것 같아."),
    ("Mason", "worried", "이대로 가면 위성이 곧 묘지궤도로 이동하게 될 거야."),
    ("Alex", "dumbfounded", "묘지궤도?"),
    ("Mason", "flustered", "수명이 끝난 위성을 보내는 궤도야.\n거기까지 올라가 버리면 Intelsat에 접근할 기회도 없어진다고 보면 돼."),
    ("Alex", "worried", "흠.. 그럼 시간이 얼마나 남은 거지?"),
    ("Mason", "dumbfounded", "그걸 지금부터 알아내야해."),
]

AFTER_M1_DIALOGUES = [
    ("SYSTEM", None, "ANALYSIS COMPLETE\nTIME REMAINING : 35 MINUTES"),
    ("Alex", "flustered", "35분이라니! 생각보다 시간이 얼마 안남았는데..."),
    ("Mason", "worried", "서둘러 접속해서 필요한 정보를 빼내야 해."),
    ("Alex", "solemn", "그럼 바로 시작하자!"),
    ("Mason", "worried", "그게…… 문제가 하나 더 있어."),
    ("Alex", "surprised", "뭐야?"),
    ("Mason", "dumbfounded", "Intelsat에 접속하는 비밀번호를 알아내야해."),
    ("Alex", "dumbfounded", "첩보로 받은 내용에 따르면 <i><b>위성의 궤도 둘레</i></b>와 관련이 있대!"),
    ("Mason", "dumbfounded", "현재 궤도는 35,786km 이고, 지구 반지름은 6,371km 이니까...\n{agent}! 서둘러 계산해서 비밀번호를 찾아줘!"),
]

EPILOGUE_DIALOGUES = [
    ("SYSTEM", None, "ACCESS CODE : 2647\nAUTHENTICATING...\nACCESS GRANTED"),
    ("Alex", "happy", "접속됐다!"),
    ("Mason", "idle", "좋아!\n여기 파일 하나를 발견했어!"),
    ("Mason", "idle", "파일 이름은 ...<b>PROJECT HAGUE</b>..."),
    ("Alex", "surprised", "헤이그.\n첩보를 보내온 도시 이름과 일치해."),
    ("Mason", "sad", "근데 좀 이상한데……"),
    ("Alex", "surprised", "뭐가??"),
    ("Mason", "flustered", "파일 내용을 읽을 수가 없어.\n파일이 손상된 것 같아!"),
    ("Alex", "worried", "{agent} 요원... 첫 임무부터 제대로 걸린 것 같은데."),
    ("SYSTEM", None, "CLASSIFIED FILE DETECTED\nPROJECT HAGUE\nENCRYPTION : ACTIVE"),
]


# =========================================================
# 유틸 함수
# =========================================================
def ensure_agent_file():
    if not AGENT_FILE.exists():
        with open(AGENT_FILE, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["code_name", "access_key"])
            writer.writeheader()


def load_agents():
    ensure_agent_file()
    agents = {}

    with open(AGENT_FILE, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code_name = row.get("code_name", "").strip().upper()
            access_key = row.get("access_key", "").strip()

            if code_name:
                agents[code_name] = access_key

    return agents


def save_agent(code_name, access_key):
    ensure_agent_file()

    with open(AGENT_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["code_name", "access_key"])
        writer.writerow({
            "code_name": code_name.upper(),
            "access_key": access_key,
        })


def jump_to_mission():
    selected = st.session_state.mission_selector
    if selected != 'MISSION SELECT':
        st.session_state.page = MISSIONS[selected]
        st.session_state.dialogue_index = 0
        st.session_state.message = ""


def show_mission_selector():
    st.selectbox(
        "MISSION QUICK ACCESS",
        ["MISSION SELECT"] + list(MISSIONS.keys()),
        key="mission_selector",
        on_change=jump_to_mission,
        accept_new_options=False,
        filter_mode=None
    )

def go(page, dialogue_index=0):
    st.session_state.page = page
    st.session_state.dialogue_index = dialogue_index
    st.session_state.message = ""
    st.rerun()


def next_dialogue(dialogues, next_page):
    if st.session_state.dialogue_index < len(dialogues) - 1:
        st.session_state.dialogue_index += 1
        st.rerun()
    else:
        go(next_page)


def get_page_media(page):
    """현재 page에 맞는 영상/BGM 경로를 반환합니다."""
    media = PAGE_MEDIA.get(page, {})

    video_path = media.get("video", DEFAULT_VIDEO_PATH)
    bgm_path = media.get("bgm", DEFAULT_BGM_PATH)
    bgm_loop = media.get("bgm_loop", True)

    return video_path, bgm_path, bgm_loop


def play_bgm(page):
    """현재 page에 설정된 BGM을 재생합니다."""
    _, bgm_path, bgm_loop = get_page_media(page)

    # None이면 이 페이지에서는 BGM을 재생하지 않음
    if bgm_path is None:
        return

    if bgm_path.exists():
        st.audio(
            str(bgm_path),
            format="audio/mpeg",
            autoplay=True,
            loop=bgm_loop,
        )


def show_video(page):
    """현재 page에 설정된 영상을 표시합니다."""
    video_path, _, _ = get_page_media(page)

    # None이면 이 페이지에서는 영상 없음
    if video_path is None:
        return

    if video_path.exists():
        st.video(
            str(video_path),
            autoplay=True,
            loop=True,
            muted=True,
            width="stretch",
        )
    else:
        st.html(f"""
        <div style="
            height:520px;
            background:
                radial-gradient(circle at 60% 30%, rgba(0,180,150,.14), transparent 26%),
                linear-gradient(145deg,#071315,#010405);
            border:1px solid rgba(98,255,211,.2);
            display:flex;
            align-items:center;
            justify-content:center;
            color:#51776e;
            font-family:Consolas,monospace;
            letter-spacing:.12em;
        ">
            VIDEO FILE NOT FOUND<br>
            {video_path}
        </div>
        """)


def image_to_base64(path):
    if not path.exists():
        return ""

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def show_dialogue(dialogues, next_page):
    idx = st.session_state.dialogue_index

    # 새 구조: (speaker, emotion, text)
    speaker, emotion, text = dialogues[idx]

    agent = st.session_state.code_name
    text = text.format(agent=agent)

    speaker_color = SPEAKER_COLORS.get(speaker, "#62FFD3")
    speaker_alignment = SPEAKER_ALIGNMENTS.get(speaker, "left")

    # 줄바꿈을 HTML <br>로 변환
    html_text = text.replace("\n", "<br>")

    # =====================================================
    # 캐릭터 이미지 설정
    # =====================================================
    character_html = ""

    if speaker in CHARACTER_IMAGES:
        # 지정한 감정 이미지가 없으면 idle 이미지로 자동 대체
        image_path = CHARACTER_IMAGES[speaker].get(
            emotion,
            CHARACTER_IMAGES[speaker]["idle"],
        )

        # 해당 감정 파일 자체가 아직 없을 때도 idle로 한 번 더 대체
        if not image_path.exists():
            image_path = CHARACTER_IMAGES[speaker]["idle"]

        img_data = image_to_base64(image_path)

        if img_data:
            side_class = (
                "alex-character"
                if speaker == "Alex"
                else "mason-character"
            )

            character_html = f"""
            <img
                src="data:image/png;base64,{img_data}"
                class="character-image {side_class}"
                alt="{speaker} - {emotion}"
            >
            """

    # 현재 페이지에 설정된 영상
    show_video(st.session_state.page)

    # 영상 위 캐릭터 + 대사창
    st.html(f"""
    <style>
        div[data-testid="stVideo"] {{
            border: 1px solid rgba(98,255,211,.25);
            box-shadow: 0 0 40px rgba(0,0,0,.5);
        }}

        /* ==============================
           캐릭터
        ============================== */
        .character-layer {{
            position: relative;
            z-index: 10;
            height: 360px;
            margin-top: -430px;
            margin-bottom: 0;
            pointer-events: none;
            overflow: visible;
        }}

        .character-image {{
            position: absolute;
            bottom: 95px;
            height: 330px;
            width: auto;
            object-fit: contain;
            filter:
                drop-shadow(0 8px 14px rgba(0,0,0,.55))
                drop-shadow(0 0 10px rgba(98,255,211,.08));
        }}

        /* Alex는 왼쪽 */
        .alex-character {{
            left: 45px;
        }}

        /* Mason은 오른쪽 */
        .mason-character {{
            right: 45px;
        }}

        /* ==============================
           대사 박스
        ============================== */
        .dialogue-box {{
            position: relative;
            z-index: 15;
            min-height: 145px;
            width: calc(100% - 60px);
            margin-left: 30px;
            margin-top: -110px;
            margin-bottom: 40px;
            padding: 20px 28px;
            box-sizing: border-box;
            background: rgba(2,10,12,.90);
            backdrop-filter: blur(7px);
            border: 1px solid rgba(98,255,211,.42);
            box-shadow: 0 10px 40px rgba(0,0,0,.5);
            font-family: Consolas, "Courier New", monospace;
        }}

        .dialogue-speaker {{
            color: {speaker_color};
            font-size: 18px;
            font-weight: 800;
            letter-spacing: .06em;
            margin-bottom: 14px;
            text-align: {speaker_alignment};
        }}

        .dialogue-text {{
            color: #eafff8;
            font-size: 16px;
            line-height: 1.7;
            text-align: {speaker_alignment};
        }}

        /* ==============================
           클릭용 투명 버튼
        ============================== */
        div[data-testid="stButton"]:last-of-type {{
            position: relative;
            z-index: 30;
            margin-top: -185px;
            margin-left: 30px;
            width: calc(100% - 60px);
            height: 145px;
            margin-bottom: 40px;
        }}

        div[data-testid="stButton"]:last-of-type button {{
            width: 100%;
            height: 145px;
            min-height: 145px;
            padding: 0;
            margin: 0;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: transparent !important;
            cursor: pointer;
        }}

        div[data-testid="stButton"]:last-of-type button:hover {{
            background: rgba(98,255,211,.025) !important;
            border: none !important;
            box-shadow: none !important;
        }}

        div[data-testid="stButton"]:last-of-type button p {{
            color: transparent !important;
            font-size: 0 !important;
        }}
    </style>

    <div class="character-layer">
        {character_html}
    </div>

    <div class="dialogue-box">
        <div class="dialogue-speaker">{speaker}</div>
        <div class="dialogue-text">{html_text}</div>
    </div>
    """)

    # 화면에는 글자를 보이지 않지만 대사창 전체가 클릭 버튼
    if st.button(
        "next",
        key=f"dialogue_{st.session_state.page}_{idx}",
        use_container_width=True,
    ):
        next_dialogue(dialogues, next_page)


# =========================================================
# 1. 요원 등록
# =========================================================
def register_page():
    gia_logo = image_to_base64(GIA_LOGO)

    st.html(f"""
    <style>
        .gia-login-wrapper {{
            max-width: 800px;
            margin: 40px auto 24px auto;
        }}

        .gia-logo {{
            display: block;
            width: 500px;
            max-height: 250px;
            object-fit: contain;
            margin: 0 auto 28px auto;
            filter:
                drop-shadow(0 0 8px rgba(98,255,211,.15));
        }}

        .boot-terminal {{
            border: 1px solid rgba(98,255,211,.35);
            background: rgba(0, 5, 7, .95);
            padding: 26px 30px;
            font-family: Consolas, "Courier New", monospace;
            color: #b9d8d0;
            font-size: 14px;
            line-height: 1.9;
            box-shadow:
                0 0 0 1px rgba(98,255,211,.03) inset,
                0 0 35px rgba(0,0,0,.65);
        }}

        .boot-success {{
            color: #62ffd3;
        }}

        .boot-info {{
            color: #86aaa1;
        }}

        .boot-warning {{
            color: #ffcc66;
        }}

        .boot-prompt {{
            margin-top: 16px;
            color: #eafff8;
        }}

        .cursor {{
            display: inline-block;
            width: 8px;
            height: 15px;
            margin-left: 4px;
            vertical-align: -2px;
            background: #62ffd3;
            animation: cursorBlink 1s infinite;
        }}

        @keyframes cursorBlink {{
            0%, 50% {{
                opacity: 1;
            }}

            51%, 100% {{
                opacity: 0;
            }}
        }}
    </style>

    <div class="gia-login-wrapper">

        <img src="data:image/png;base64,{gia_logo}" class="gia-logo">

        <div class="boot-terminal">
            <span class="boot-info">
                GIA SECURE TERMINAL v4.8.2
            </span><br>
            [BOOT] Initializing encrypted environment...<br>
            [SYS ] Loading security protocols........
            <span class="boot-success">OK</span><br>
            [NET ] Establishing secure uplink........
            <span class="boot-success">CONNECTED</span><br>
            [AUTH] Contacting GIA authentication server...
            <span class="boot-success">ONLINE</span><br>
            [CRYPT] AES-256 encryption channel.......
            <span class="boot-success">ACTIVE</span><br>
            [NODE] Secure gateway : GIA-NET-07<br>
            [PING] Response : 12ms<br><br>
            <span class="boot-success">
                SECURE CONNECTION ESTABLISHED
            </span><br>
            <span class="boot-warning">
                AUTHORIZATION REQUIRED
            </span><br>

            <div class="boot-prompt">
                > ENTER AGENT CREDENTIALS<span class="cursor"></span>
            </div>
        </div>
    </div>
    """)

    agents = load_agents()

    with st.form("agent_login"):
        code_name = st.text_input(
            "CODE NAME",
            placeholder="Enter your code name",
            max_chars=20,
        )

        access_key = st.text_input(
            "ACCESS KEY",
            placeholder="Enter access key",
            type="password",
        )

        submitted = st.form_submit_button(
            "ACCESS SECURE NETWORK",
            use_container_width=True,
        )

    if submitted:
        code_name = code_name.strip().upper()
        access_key = access_key.strip()

        if not code_name:
            st.error("CODE NAME을 입력하십시오.")

        elif not access_key:
            st.error("ACCESS KEY를 입력하십시오.")

        elif code_name in agents:
            if agents[code_name] == access_key:
                st.session_state.registered = True
                st.session_state.code_name = code_name
                st.session_state.page = "registered"
                st.rerun()
            else:
                st.error("ACCESS DENIED — ACCESS KEY가 일치하지 않습니다.")

        else:
            save_agent(code_name, access_key)
            st.session_state.registered = True
            st.session_state.code_name = code_name
            st.session_state.page = "registered"
            st.rerun()


# =========================================================
# 2. 등록 완료
# =========================================================
def registered_page():
    agent = st.session_state.code_name

    st.html(f"""
    <div class="gia-panel" style="max-width:760px;margin:80px auto;">
        <div class="terminal-title">AGENT AUTHENTICATION</div>
        <div class="terminal-main">
            VERIFYING AGENT...<br><br>
            <span class="success">IDENTITY VERIFIED</span><br><br>
            WELCOME, AGENT <b>{agent}</b><br><br>
            <span class="terminal-dim">
                SECURITY LEVEL : CLASSIFIED<br>
                DEPARTMENT : CYBER INTELLIGENCE<br>
                STATUS : ACTIVE
            </span>
        </div>
    </div>
    """)

    if st.button("ENTER SECURE NETWORK", use_container_width=True):
        go("chapter_intro")


# =========================================================
# 3. Intro 화면
# =========================================================
def chapter_intro():
    intro_img = image_to_base64(INTRO_IMAGE)

    st.html(f"""
        <div class="gia-panel" style="margin-top:90px;text-align:center;">
        <div class="terminal-title">CLASSIFIED OPERATION</div>
        <div style="font-size:17px;color:#82a69d;letter-spacing:.2em;">CHAPTER 1 — THE CORRUPTED FILE</div>
        <div style="font-size:46px;font-weight:800;margin:16px 0;color:white;">
            손상된 파일
        </div>
        <img
            src="data:image/png;base64,{intro_img}"
            style="
                width: 100%;
                max-width: 650px;
                max-height: 350px;
                object-fit: contain;
                display: block;
                margin: 25px auto;
            "
        >
        <div class="terminal-dim">
            지난 이야기:<br>
            GIA 요원들은 빌더버그 조직의 인공위성 비밀번호를 알아내 해킹에 성공한다.<br>
            하지만 그 안에서 발견한 파일은 손상되어 있는데…<br>
            위성이 묘지궤도에 도착하기 전까지 정보를 입수할 수 있을까!<br>
        </div>
    </div>
    """)

    if st.button("BEGIN OPERATION", use_container_width=True):
        go("mission1_story")


# =========================================================
# 4. Mission 01
# =========================================================
MISSION_CONFIG = {
    "mission1": {
        "number": "01",
        "title": "남은 시간을 계산하라",
        "image": MISSION1_IMAGE,
        "prompt_html": """
            <b class="mason-name">Mason</b><br>
            현재 위치에서 묘지궤도까지 최소 직선거리부터 구해야해.<br>
            아래 공식을 활용해서 남은 시간을 구해줘!<br><br>
        """,
        "card_label": "FORMULA",
        "card_value": "시간(s) = 거리(km) / 속도(km/s)",
        "input_label": "TIME REMAINING / MIN",
        "submit_label": "SUBMIT ANALYSIS",
        "answer": 35,
        "wrong_message": "ANALYSIS FAILED — 계산 결과를 다시 확인하십시오.",
        "success_message": "ANALYSIS COMPLETE",
        "continue_label": "CONTINUE OPERATION",
        "next_page": "mission2_story",
    },
    "mission2": {
        "number": "02",
        "title": "INTELSAT 접속 암호를 찾아라",
        "image": MISSION2_IMAGE,
        "alert_html": """
            <div class="mission-alert">
                ACCESS DENIED<br>
                PASSWORD REQUIRED
            </div>
        """,
        "prompt_html": """
            <b class="mason-name">Mason</b><br>
            위성의 고도는 지표면부터 잰 거리야.<br>
            원의 둘레 공식을 사용해서 위성 궤도의 둘레를 구하자!<br><br>
        """,
        "card_label": "ENCRYPTED MESSAGE",
        "card_value": "원의 둘레 = 원의 반지름 ⨯ 2 ⨯ 원주율",
        "input_label": "PASSWORD",
        "submit_label": "CONNECT",
        "answer": 2647,
        "wrong_message": "ACCESS DENIED — 접속 암호가 일치하지 않습니다.",
        "success_message": "ACCESS CODE ACCEPTED — AUTHENTICATING...",
        "continue_label": "ENTER INTELSAT SYSTEM",
        "next_page": "epilogue",
    },
}


def render_mission_page(mission_key):
    """공통 미션 UI와 정답 판정을 처리합니다."""
    config = MISSION_CONFIG[mission_key]
    image_data = image_to_base64(config["image"])
    alert_html = config.get("alert_html", "")

    st.html(f"""
    <div class="gia-panel">
        <div class="mission-title">MISSION {config["number"]}</div>
        <div class="mission-name">{config["title"]}</div>

        {alert_html}

        <div class="mission-image-wrap">
            <img
                src="data:image/png;base64,{image_data}"
                class="mission-image"
            >
        </div>

        <div class="terminal-main">
            {config["prompt_html"]}
        </div>

        <div class="mission-info-card">
            <div class="data-label">{config["card_label"]}</div>
            <div class="data-value">{config["card_value"]}</div>
        </div>
    </div>
    """)

    answer = st.number_input(
        config["input_label"],
        min_value=0,
        step=1,
        value=None,
        placeholder="정수 입력",
        key=f"{mission_key}_answer",
    )

    if st.button(
        config["submit_label"],
        use_container_width=True,
        key=f"{mission_key}_submit",
    ):
        is_correct = answer == config["answer"]
        st.session_state[f"{mission_key}_clear"] = is_correct
        st.session_state.message = "success" if is_correct else "wrong"
        st.rerun()

    if st.session_state.message == "wrong":
        st.error(config["wrong_message"])

    elif st.session_state.message == "success":
        st.success(config["success_message"])
        if st.button(
            config["continue_label"],
            type="primary",
            use_container_width=True,
            key=f"{mission_key}_continue",
        ):
            go(config["next_page"])


def mission1():
    render_mission_page("mission1")

def mission2():
    render_mission_page("mission2")


# =========================================================
# 6. 엔딩
# =========================================================
def ending():
    st.html(f"""
    <div class="gia-panel" style="margin-top:90px;text-align:center;">
        <div class="terminal-title warning">CLASSIFIED FILE DETECTED</div>
        <div style="font-size:44px;font-weight:900;color:white;margin:28px 0;">
            PROJECT HAGUE
        </div>
        <div class="terminal-dim">
            과연 이들은 시간 내에 손상된 파일을 복구하여<br>빌더버그의 공격을 무사히 막을 수 있을까?<br>
        </div>
        <div style="
            margin-top:60px;
            font-size:15px;
            letter-spacing:.3em;
            color:#62ffd3;
        ">
            TO BE CONTINUED...
        </div>
    </div>
    """)


# =========================================================
# 페이지 실행
# =========================================================
def render_current_page():
    page = st.session_state.page

    if st.session_state.registered and page != "register":
        play_bgm(page)

    if st.session_state.registered and page not in ("register", "registered"):
        _, selector_col = st.columns([4, 1])
        with selector_col:
            show_mission_selector()

    page_routes = {
        "register": register_page,
        "registered": registered_page,
        # "prologue": lambda: show_dialogue(PROLOGUE_DIALOGUES, "chapter_intro"),
        "chapter_intro": chapter_intro,
        "mission1_story": lambda: show_dialogue(CHAPTER1_DIALOGUES, "mission1"),
        "mission1": mission1,
        "mission2_story": lambda: show_dialogue(AFTER_M1_DIALOGUES, "mission2"),
        "mission2": mission2,
        "epilogue": lambda: show_dialogue(EPILOGUE_DIALOGUES, "ending"),
        "ending": ending,
    }

    page_routes.get(page, register_page)()


render_current_page()
