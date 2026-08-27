import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64, csv, json

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
INTRO_IMAGE = IMG_DIR / "1-3_intro.png"
MISSION1_IMAGE = IMG_DIR / "1-3_m2.png"
MISSION2_IMAGE = IMG_DIR / "1-3_m2.png"
MISSION3_IMAGE = IMG_DIR / "1-3_m3.png"
AGENT_FILE = Path("agents.csv")

MISSIONS = {
    "Mission 1": "mission1_story",
    "Mission 2": "mission2_story",
    "Mission 3": "mission3_story",
}

# =========================================================
# 페이지별 영상 / 배경음악
# video 또는 bgm을 None으로 두면 해당 페이지에서는 재생하지 않습니다.
# =========================================================
PAGE_MEDIA = {
    "registered": {
        "video": None,
        "bgm": None,
        "bgm_loop": True,
    },
    "intro": {
        "video": None,
        "bgm": SOUND_DIR / "futuristicbutton_a_2.mp3",
        "bgm_loop": False,
    },
    "mission1_story": {
        "video": VIDEO_DIR / "ch01-1-1.mp4",
        "bgm": SOUND_DIR / "upbeatcorporation_2.mp3",
        "bgm_loop": True,
    },
    "mission1": {
        "video": None,
        "bgm": SOUND_DIR / "sweepnext_2.mp3",
        "bgm_loop": False,
    },
    "mission2_story": {
        "video": VIDEO_DIR / "ch01-1-2.mp4",
        "bgm": SOUND_DIR / "brainTeaser_2.mp3",
        "bgm_loop": True,
    },
    "mission2": {
        "video": None,
        "bgm": SOUND_DIR / "sweepnext_2.mp3",
        "bgm_loop": False,
    },
    "mission3_story": {
        "video": VIDEO_DIR / "sin1_idle.mp4",
        "bgm": SOUND_DIR / "brainTeaser_2.mp3",
        "bgm_loop": True,
    },
    "mission3": {
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
DEFAULT_VIDEO_PATH = VIDEO_DIR / "sin2.mp4"
DEFAULT_BGM_PATH = SOUND_DIR / "engineering_2.mp3"

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
        "talking2": IMG_EMO_DIR / "alex_talking2.png",
        "talking3": IMG_EMO_DIR / "alex_talking3.png",
        "whatever": IMG_EMO_DIR / "alex_whatever.png",
        "difficult": IMG_EMO_DIR / "alex_difficult.png",
        "gaze": IMG_EMO_DIR / "alex_gaze.png"
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
        "talking2": IMG_EMO_DIR / "mason_talking2.png",
        "talking3": IMG_EMO_DIR / "mason_talking3.png",
        "whatever": IMG_EMO_DIR / "mason_whatever.png",
        "difficult": IMG_EMO_DIR / "mason_difficult.png",
        "talking4": IMG_EMO_DIR / "mason_talking4.png"
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
    .episode-title {
        font-size: 17px;
        color: #82a69d;
        letter-spacing: .2em;
        font-weight: 700;
    }
    .intro-image {
        width: 100%;
        max-width: 900px;
        max-height: 500px;
        object-fit: contain;
        display: block;
        margin: 25px auto;
    }
    /* -----------------------------------------
    Mission Brief
    ----------------------------------------- */
    .intro-briefing {
        display: grid;
        grid-template-columns: 150px 1fr;
        gap: 24px;
        padding-top: 24px;
        border-top: 1px solid rgba(98,255,211,.13);
    }
    .briefing-label {
        color: #62ffd3;
        font-size: 11px;
        letter-spacing: .18em;
        padding-top: 3px;
    }
    .briefing-text {
        color: #91afa7;
        font-family:
            Pretendard,
            "Noto Sans KR",
            sans-serif;
        font-size: 15px;
        line-height: 1.8;
        text-align: left;
    }
    .briefing-text b {
        color: #dffff7;
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
    .chapter-label {
        font-family: Consolas, "Courier New", monospace;
        color: #62ffd3;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: .18em;
        padding-top: 32px;
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
    "mission3_clear": False,
    "message": "",
    "mission_selector": "MISSION SELECT",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 스토리 데이터
# 형식: ("등장인물", "감정", "대사")
# SYSTEM은 감정값을 None
# =========================================================
M1_DIALOGUES = [
    ("Mason", "deep", "빌더버그 조직은 이 넓은 헤이그 도시 어디에 폭발물을 설치했을까…"),
    ("Alex", "surprised", "Mason! GIA 본부에서 연락이 왔어! 혹시 몰라서 나머지 1개 파일도 분석해달라고 했거든!"),
    ("Mason", "surprised", "뭐라고 답변이 왔어?"),
    ("Alex", "talking3", "역시 내 예상이 맞았어! 이 파일에는 장소에 대한 힌트가 담겨있었어."),
    ("Alex", "talking3", "start와 end 단어 사이에 있는 문자열을 분석해보면 알 수 있대."),
    ("Mason", "talking3", "그래? 그럼 이번에도 그 사이 문자열부터 추출해야겠네."),
    ("Alex", "firmly", "응! 나는 Intelsat과 통신이 끊기기 전까지 다른 정보를 얻을 수 있는지 계속 확인해 볼게."),
    ("Mason", "idle", "알았어. 어떤 정보든 모두 수집해 줘."),
    ("Mason", "firmly", "{agent} 요원! 나와 같이 장소 정보가 담긴 문자열을 추출해보자. 서둘러!"),
]

M2_DIALOGUES = [
    ("Alex", "dumbfounded", "장소에 대한 문자열 데이터 맞아? 전혀 모르겠는데…."),
    ("Mason", "deep", "내가 보기엔 데이터에 어떤 규칙을 적용해 변형시켜 놓은 것 같아."),
    ("Alex", "puzzled", "규칙? 무슨 규칙인데?"),
    ("Mason", "talking3", "데이터가 손상되어 있긴 하지만, 뭔가 문자열이 뒤집혀 있는 것으로 보여."),
    ("Alex", "flustered", "그래? 조금만 더 서둘러줘!"),
]

M3_DIALOGUES = [
    ("SYSTEM", None, "Alex의 컴퓨터 화면은 헤이그 도시 지도로 가득 차 있다."),
    ("Alex", "serious", "Mason! 우리가 찾아낸 힌트 속 장소들은 헤이그 전 지역에 퍼져있어."),
    ("Mason", "deep", "그러네… 이 많은 곳에 전부 폭발물을 설치하진 않았을 것 같은데…"),
    ("Mason", "deep", "이 넓은 곳에서 빌더버그 녀석들은 어디를 첫 타깃으로 두었을까?"),
    ("Alex", "surprised", "아! Mason 그러고보니 아까 그 힌트 데이터 속에 단서가 있었던 것 같아!"),
    ("Mason", "surprised", "…맞아! 어떤 특정 순서로 공격한다고 했던 것 같은데…!"),
]

EPILOGUE_DIALOGUES = [
    ("SYSTEM", None, "TARGET PRIORITY ANALYSIS COMPLETE"),
    ("Alex", "surprised", "City Hall… 첫 번째 폭발물이 설치된 장소는 시청이야!"),
    ("Mason", "firmly", "좋아. 이제 정확한 장소를 알아냈어. 바로 현장 대응팀에 전달하자!"),
    ("Alex", "worried", "하지만 시간이 거의 없어. 공격 예정일은 바로 내일이야."),
    ("Mason", "determined", "아직 늦지 않았어. 다음 작전에서 반드시 폭발물을 찾아내자."),
    ("SYSTEM", None, "PRIMARY TARGET IDENTIFIED\nLOCATION : CITY HALL\nSTATUS : URGENT"),
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


# 클릭하면 미션 데이터를 클립보드에 복사합니다.
def show_copy_data_button(data, key):
    safe_data = json.dumps(data)

    components.html(f"""
        <style>
        .copy-button {{
                width: 100%;
                height: 46px;
        
                background: rgba(5,23,24,.92);
        
                border:
                    1px solid rgba(98,255,211,.40);
        
                color: #a9cfc5;
        
                font-family:
                    Consolas,
                    "Courier New",
                    monospace;
        
                font-size: 13px;
                letter-spacing: .08em;
        
                cursor: pointer;
        
                transition: .15s ease;
            }}
        
            .copy-button:hover {{
                border-color: #62ffd3;
                color: #62ffd3;
            }}
        
            .copy-button.copied {{
                border-color: #68ffbd;
                color: #68ffbd;
            }}
        </style>
        <button id="copy-{key}" class="copy-button" type="button">
            💾 COPY MISSION DATA
        </button>

        <script>
            const button = document.getElementById("copy-{key}");
            const data = {safe_data};

            button.addEventListener("click", async () => {{
                try {{
                    await navigator.clipboard.writeText(data);
                }} catch (error) {{
                    const textarea = document.createElement("textarea");
                    textarea.value = data;
                    textarea.style.position = "fixed";
                    textarea.style.opacity = "0";
                    document.body.appendChild(textarea);
                    textarea.focus();
                    textarea.select();
                    document.execCommand("copy");
                    textarea.remove();
                }}

                button.textContent = "✓ DATA COPIED TO CLIPBOARD";
                button.classList.add("copied");
                setTimeout(() => {{
                    button.textContent =
                        "💾 COPY MISSION DATA";

                    button.classList.remove("copied");
                }}, 2000);
            }});
        </script>
        """,
        height=55,
    )

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
        go("intro")


# =========================================================
# 3. Intro 화면
# =========================================================
def intro():
    intro_img = image_to_base64(INTRO_IMAGE)

    st.html(f"""
    <div class="gia-panel" style="margin-top:90px;text-align:center;">
        <div class="terminal-title">
            CLASSIFIED OPERATION
        </div>

        <img class="intro-image" src="data:image/png;base64,{intro_img}">

        <div class="intro-briefing">
            <div class="briefing-label">
                지난 이야기
            </div>

            <div class="briefing-text">
                빌더버그 조직이 헤이그 도시를 파괴하려는 날짜를 드디어 알아냈다. 바로 내일!<br>
                Intelsat 인공위성도 점점 묘지 궤도를 향하고 있어 남은 시간이 많지 않다.<br>
                아직 분석하지 않은 마지막 파일에서 정확한 공격 장소를 찾아내야 한다.<br>
            </div>
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
        "title": "필요한 부분 추출하기",
        "image": MISSION1_IMAGE,
        "alert_html": '',
        "prompt_html": """
                        <b class="mason-name">Mason</b><br>
                        장소 정보는 <b>start</b>와 <b>end</b> 사이에 있어.<br>
                        find()로 두 단어의 위치를 찾은 다음 문자열 슬라이싱으로<br>
                        그 사이에 있는 문자열만 정확하게 추출해줘!<br><br>
                    """,
        "clipboard_data": '''file_b = "a8f__GIAx91_hague_trace__q7start#.redro lacitebahpla yb kcatta trats eW .yti@sr@@evinu,tna@lp rae@@lcun,llam@ gni@@ppoh@s,lla@h@ y@tic,tekr@am kcots,noi@tats eci@l@op,ret@aeht:secalp gniwollof fo eno si tegrat ehT#end__sat_link_77x__archive"''',
        "card_label": "STRING TOOLS",
        "card_value": "find() : 특정 문자열이 처음 등장하는 위치 반환<br>문자열[시작:끝] : 원하는 범위 추출",
        "input_label": "EXTRACTED LOCATION DATA",
        "submit_label": "VERIFY DATA",
        "answer": '#.redro lacitebahpla yb kcatta trats eW .yti@sr@@evinu,tna@lp rae@@lcun,llam@ gni@@ppoh@s,lla@h@ y@tic,tekr@am kcots,noi@tats eci@l@op,ret@aeht:secalp gniwollof fo eno si tegrat ehT#',
        "answer_placeholder": 'start와 end 사이의 문자열을 입력하세요.',
        "wrong_message": "EXTRACTION FAILED — start/end 위치와 슬라이싱 범위를 다시 확인하세요.",
        "success_message": "LOCATION DATA EXTRACTED",
        "continue_label": "NEXT OPERATION",
        "next_page": "mission2_story",
    },
    "mission2": {
        "number": "02",
        "title": "데이터 속 장소 힌트 찾기",
        "image": MISSION2_IMAGE,
        "alert_html": '',
        "prompt_html": """
                    <b class="mason-name">Mason</b><br>
                    데이터가 거꾸로 뒤집혀 있고, 일부 문자도 다른 기호로 바뀌어 있어.<br>
                    문자열을 뒤집은 뒤 replace()를 사용해서 장소 목록을 복원해줘!<br><br>
                    """,
        "card_label": "STRING TOOLS",
        "card_value": "문자열[::-1] : 문자열 뒤집기<br>replace(기존, 변경) : 특정 문자열 바꾸기",
        "input_label": "RECOVERED LOCATIONS",
        "submit_label": "SUBMIT ANALYSIS",
        "answer": 'theater,police station,stock market,city hall,shopping mall,nuclear plant,university',
        "answer_placeholder": '복원한 장소 목록을 입력하세요.',
        "wrong_message": "ANALYSIS FAILED — 문자열 방향과 치환할 문자를 다시 확인하세요.",
        "success_message": "LOCATION CLUES RECOVERED",
        "continue_label": "NEXT OPERATION",
        "next_page": "mission3_story",
    },
    "mission3": {
        "number": "03",
        "title": "첫 번째 폭발물이 설치된 장소를 찾아라",
        "image": MISSION3_IMAGE,
        "alert_html": '',
        "prompt_html": """
                        <b class="mason-name">Mason</b><br>
                        미션 2에서 복원한 장소들을 다시 확인해봐.<br>
                        힌트에는 <b>알파벳 순서대로 공격을 시작한다</b>고 적혀 있었어.<br>
                        장소 문자열을 리스트로 나눈 뒤 정렬해서 첫 번째 타깃을 찾아줘!<br><br>
                    """,
        "card_label": "LIST TOOLS",
        "card_value": "split(',') : 문자열을 리스트로 분리<br>sort() / sorted() : 리스트를 오름차순으로 정렬",
        "input_label": "FIRST TARGET",
        "submit_label": "CONFIRM TARGET",
        "answer": 'city hall',
        "answer_placeholder": '첫 번째 공격 장소를 입력하세요.',
        "wrong_message": "TARGET MISMATCH — 장소 목록의 정렬 순서를 다시 확인하세요.",
        "success_message": "PRIMARY TARGET IDENTIFIED — CITY HALL",
        "continue_label": "EPILOGUE",
        "next_page": "epilogue",
    }
}


# 공통 미션 UI와 정답 판정을 처리합니다.
def render_mission_page(mission_key):
    config = MISSION_CONFIG[mission_key]
    image_data = image_to_base64(config["image"])
    alert_html = config.get("alert_html", "")
    card_html = ''
    answer = None

    if config.get("card_value"):
        card_html = f"""
        <div class="mission-info-card">
            <div class="data-label">{config["card_label"]}</div>
            <div class="data-value">{config["card_value"]}</div>
        </div>
        """

    st.html(f"""
    <div class="gia-panel">
        <div class="mission-title">MISSION {config["number"]}</div>
        <div class="mission-name">{config["title"]}</div>

        {alert_html}

        <div class="mission-image-wrap">
            <img src="data:image/png;base64,{image_data}" class="mission-image">
        </div>

        <div class="terminal-main">
            {config["prompt_html"]}
        </div>

        {card_html}
    </div>
    """)

    clipboard_data = config.get("clipboard_data")
    if clipboard_data:
        show_copy_data_button(clipboard_data.strip(), mission_key)

    if config["answer"].isdigit():
        answer = st.number_input(
            config["input_label"],
            min_value=0,
            step=1,
            value=None,
            placeholder="정수 입력",
            key=f"{mission_key}_answer"
        )
    else:
        answer = st.text_input(
            config["input_label"], 
            placeholder=config['answer_placeholder'], 
            value=None, key=f"{mission_key}_answer"
        )

    if st.button(config["submit_label"], use_container_width=True, key=f"{mission_key}_submit"):
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
def mission3():
    render_mission_page("mission3")


# =========================================================
# 6. 엔딩
# =========================================================
def ending():
    st.html(f"""
    <div class="gia-panel" style="margin-top:90px;text-align:center;">
        <div class="terminal-title warning">PRIMARY TARGET IDENTIFIED</div>
        <div style="font-size:44px;font-weight:900;color:white;margin:28px 0;">
            CITY HALL
        </div>
        <div class="terminal-dim">
            빌더버그 조직의 첫 번째 공격 장소를 찾아냈다.<br>
            공격 예정일은 바로 내일.<br>
            이제 남은 것은 폭발물을 찾아 계획을 완전히 무산시키는 것뿐이다.<br>
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
        chapter_col, selector_col = st.columns([4, 1])
        with chapter_col:
            st.html("""
            <div class="chapter-label">
                CHAPTER 01 - 
                <span style="color:rgba(255,100,100,.8);font-weight: 700;">EP.3</span>
            </div>
            """)
        with selector_col:
            show_mission_selector()

    page_routes = {
        "register": register_page,
        "registered": registered_page,
        # "prologue": lambda: show_dialogue(PROLOGUE_DIALOGUES, "intro"),
        "intro": intro,
        "mission1_story": lambda: show_dialogue(M1_DIALOGUES, "mission1"),
        "mission1": mission1,
        "mission2_story": lambda: show_dialogue(M2_DIALOGUES, "mission2"),
        "mission2": mission2,
        "mission3_story": lambda: show_dialogue(M3_DIALOGUES, "mission3"),
        "mission3": mission3,
        "epilogue": lambda: show_dialogue(EPILOGUE_DIALOGUES, "ending"),
        "ending": ending,
    }

    page_routes.get(page, register_page)()


render_current_page()
