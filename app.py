from __future__ import annotations

import streamlit as st

from watermark_engine import WatermarkEngine


st.set_page_config(
    page_title="WatermarkCheck",
    page_icon="W",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #edf4f3;
        --muted: #afbfbe;
        --accent: #49c6b2;
        --paper: #0d141a;
        --surface: #17222b;
        --sidebar: #111b22;
        --input: #101920;
        --line: #30414b;
    }

    html, body, [data-testid="stAppViewContainer"], .stApp,
    [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
        background: var(--paper) !important;
        color: var(--ink) !important;
    }

    [data-testid="stHeader"] {
        background: var(--paper) !important;
    }

    .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3,
    .stApp [data-testid="stMarkdownContainer"],
    .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stWidgetLabel"] {
        color: var(--ink) !important;
    }

    .stApp [data-testid="stCaptionContainer"] p {
        color: var(--muted) !important;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 4rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: var(--ink);
        letter-spacing: -0.025em;
    }

    .project-kicker {
        color: var(--accent);
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-bottom: 0.45rem;
        display: block;
        line-height: 1.5;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--surface) !important;
        border-color: var(--line) !important;
        border-radius: 12px;
    }

    div.stButton > button {
        background: #202d36 !important;
        color: var(--ink) !important;
        border: 1px solid var(--line) !important;
        border-radius: 8px;
    }

    div.stButton > button[kind="primary"] {
        background: var(--accent) !important;
        border: 1px solid var(--accent) !important;
        color: #06211d !important;
        border-radius: 8px;
        min-height: 2.7rem;
        font-weight: 700;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #70dbc9 !important;
        border-color: #70dbc9 !important;
    }

    button[data-baseweb="tab"] {
        color: var(--muted) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--accent) !important;
        border-bottom-color: var(--accent);
    }

    textarea, input, [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {
        background: var(--input) !important;
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
        border-color: var(--line) !important;
        caret-color: var(--accent) !important;
    }

    textarea::placeholder, input::placeholder {
        color: #92a4a3 !important;
        -webkit-text-fill-color: #92a4a3 !important;
        opacity: 1 !important;
    }

    [data-baseweb="select"] > div {
        background: var(--input) !important;
        color: var(--ink) !important;
        border-color: var(--line) !important;
    }

    [data-baseweb="select"] *,
    [role="option"],
    [role="listbox"] {
        color: var(--ink) !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"],
    [role="listbox"] {
        background: var(--surface) !important;
        border-color: var(--line) !important;
    }

    [role="option"] {
        background: var(--surface) !important;
    }

    [role="option"]:hover,
    [role="option"][aria-selected="true"] {
        background: #263943 !important;
    }

    [data-testid="stSlider"] [role="slider"] {
        background: var(--accent) !important;
        border-color: var(--accent) !important;
    }

    [data-testid="stMetric"] {
        background: var(--surface) !important;
        border: 1px solid var(--line);
        padding: 0.8rem 0.9rem;
        border-radius: 10px;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: var(--ink) !important;
    }

    section[data-testid="stSidebar"] {
        background: var(--sidebar) !important;
    }

    section[data-testid="stSidebar"] * {
        color: var(--ink) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: var(--muted) !important;
    }

    div[data-testid="stAlert"] {
        background: var(--surface) !important;
        color: var(--ink) !important;
        border: 1px solid var(--line) !important;
    }

    div[data-testid="stAlert"] * {
        color: var(--ink) !important;
    }

    [data-testid="stTooltipContent"] {
        background: var(--surface) !important;
        color: var(--ink) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="project-kicker">Mini Project</div>',
    unsafe_allow_html=True,
)
st.title("WatermarkCheck")


@st.cache_resource(show_spinner="Loading GPT-2 and detector…")
def load_engine() -> WatermarkEngine:
    return WatermarkEngine.load()


with st.sidebar:
    st.subheader("WatermarkCheck")
    st.write("**Model:** GPT-2")
    st.write("**Method:** Statistical text watermark")
    st.divider()
    st.subheader("Generation settings")
    max_tokens = st.slider("Continuation length", 30, 100, 50, 10)
    temperature = st.slider("Variation", 0.2, 1.2, 0.8, 0.1)

try:
    engine = load_engine()
    st.sidebar.success(f"Model ready · {engine.device.upper()}")
except Exception as exc:
    st.error(
        "The model did not load. Check the installation and internet "
        "connection, then restart the app."
    )
    st.exception(exc)
    st.stop()


tab_generate, tab_detect, tab_robust = st.tabs(
    ["Generate samples", "Check text", "Try a text edit"]
)


with tab_generate:
    st.subheader("Generate a pair of samples")

    prompt = st.text_area(
        "Text opening",
        "Ocean pollution harms marine life because",
        height=90,
        help=(
            "A sentence opening usually works better than an instruction. "
            "For example: ‘Coral reefs are important because’."
        ),
    )

    if st.button("Generate watermarked and ordinary samples", type="primary"):
        try:
            with st.spinner("Generating both samples…"):
                watermarked_text = engine.generate(
                    prompt, max_tokens, temperature, watermarked=True
                )
                ordinary_text = engine.generate(
                    prompt, max_tokens, temperature, watermarked=False
                )

            st.session_state["wm_text"] = watermarked_text
            st.session_state["plain_text"] = ordinary_text
            st.session_state["prompt"] = prompt.strip()
            st.session_state["generation_id"] = (
                st.session_state.get("generation_id", 0) + 1
            )
        except Exception as exc:
            st.error(f"Generation failed: {exc}")

    if "wm_text" in st.session_state:
        generation_id = st.session_state.get("generation_id", 0)
        left, right = st.columns(2)

        with left:
            with st.container(border=True):
                st.markdown("#### Watermarked sample")
                st.text_area(
                    "Generated continuation",
                    st.session_state["wm_text"],
                    height=190,
                    key=f"show_wm_{generation_id}",
                )
                if st.button("Check this sample", key="detect_wm"):
                    try:
                        sample = (
                            st.session_state["prompt"]
                            + " "
                            + st.session_state["wm_text"]
                        )
                        st.session_state["last_result"] = engine.detect(sample)
                        st.session_state["last_label"] = "Watermarked sample"
                    except Exception as exc:
                        st.error(f"Could not check this sample: {exc}")

        with right:
            with st.container(border=True):
                st.markdown("#### Ordinary sample")
                st.text_area(
                    "Generated continuation",
                    st.session_state["plain_text"],
                    height=190,
                    key=f"show_plain_{generation_id}",
                )
                if st.button("Check this sample", key="detect_plain"):
                    try:
                        sample = (
                            st.session_state["prompt"]
                            + " "
                            + st.session_state["plain_text"]
                        )
                        st.session_state["last_result"] = engine.detect(sample)
                        st.session_state["last_label"] = "Ordinary sample"
                    except Exception as exc:
                        st.error(f"Could not check this sample: {exc}")


with tab_detect:
    st.subheader("Check a text sample")

    detect_text = st.text_area(
        "Text to check",
        height=220,
        key="detect_input",
        placeholder="Paste text here…",
    )

    if st.button("Check for watermark", type="primary", key="run_detection"):
        try:
            st.session_state["last_result"] = engine.detect(detect_text)
            st.session_state["last_label"] = "Text check"
        except Exception as exc:
            st.error(f"Could not check this text: {exc}")


with tab_robust:
    st.subheader("See how an edit affects detection")

    generated_text = st.session_state.get("wm_text", "")
    default_source = (
        st.session_state.get("prompt", "") + " " + generated_text
    ).strip()
    generation_id = st.session_state.get("generation_id", 0)

    source_text = st.text_area(
        "Source text",
        value=default_source,
        height=160,
        key=f"robust_input_{generation_id}",
        placeholder="Generate a watermarked sample first, or paste text here.",
    )

    edit_type = st.selectbox(
        "Edit to try",
        [
            "Random word deletion",
            "Truncate from the end",
            "Insert extra words",
            "Reorder sentences",
            "Lowercase and remove punctuation",
        ],
    )

    edit_percent = 30
    if edit_type not in (
        "Reorder sentences",
        "Lowercase and remove punctuation",
    ):
        amount_label = (
            "Words to insert (%)"
            if edit_type == "Insert extra words"
            else "Text to remove (%)"
        )
        edit_percent = st.slider(
            amount_label,
            5,
            80,
            30,
            5,
            key="edit_percent",
        )

    if st.button("Apply edit and compare", type="primary"):
        try:
            edited_text = engine.edit_text(source_text, edit_type, edit_percent)
            st.session_state["edited_text"] = edited_text
            st.session_state["edit_type"] = edit_type
            st.session_state["edit_result_id"] = (
                st.session_state.get("edit_result_id", 0) + 1
            )
            st.session_state["baseline_result"] = engine.detect(source_text)
            st.session_state["edited_result"] = engine.detect(edited_text)
        except Exception as exc:
            st.error(f"The edit test failed: {exc}")

    if "edited_text" in st.session_state:
        edit_id = st.session_state.get("edit_result_id", 0)
        st.markdown(
            f"**Edited text · {st.session_state.get('edit_type', edit_type)}**"
        )
        st.text_area(
            "Result of edit",
            st.session_state["edited_text"],
            height=140,
            key=f"edited_display_{edit_id}",
        )

        original_col, edited_col = st.columns(2)
        results = [
            (original_col, "Original", "baseline_result"),
            (edited_col, "Edited", "edited_result"),
        ]

        for col, title, result_key in results:
            result = st.session_state[result_key]
            with col:
                with st.container(border=True):
                    st.markdown(f"#### {title}")
                    st.metric(
                        "Watermark signal",
                        "Detected" if result["detected"] else "Not detected",
                    )
                    st.write(
                        f"Z-score: **{result['z_score']:.3f}**  ·  "
                        f"P-value: **{result['p_value_display']}**  ·  "
                        f"Tokens scored: **{result['tokens_scored']}**"
                    )


def show_result(result: dict, label: str) -> None:
    st.divider()
    st.subheader(label)

    cols = st.columns(4)
    cols[0].metric(
        "Watermark signal",
        "Detected" if result["detected"] else "Not detected",
    )
    cols[1].metric("Z-score", f"{result['z_score']:.3f}")
    cols[2].metric("P-value", result["p_value_display"])
    cols[3].metric("Tokens scored", result["tokens_scored"])

    if result["detected"]:
        st.success(
            "The text contains a detectable signal for this watermark setup."
        )
    else:
        st.info(
            "The detector did not find a strong signal for this watermark setup."
        )

    st.caption(
        f"Green-token fraction: {result['green_fraction']:.1%} "
        f"({result['green_tokens']} green tokens). A result applies to this "
        "watermark configuration; it does not identify who wrote the text."
    )


if "last_result" in st.session_state:
    show_result(
        st.session_state["last_result"],
        st.session_state.get("last_label", "Check result"),
    )

st.divider()
st.caption(
    "Bisista Shrestha · Dharshan G Nayak · Ayush KC · B Shivani"
)