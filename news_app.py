import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time

# --------------------- 다크모드 테마 + 모바일 최적 레이아웃 설정 ---------------------
st.set_page_config(page_title="디시인사이드 개념글 수집기", layout="centered")
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
    }
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .block-container {
        background-color: #1e1e1e;
    }
    .stSidebar, .st-bb, .st-bx, .st-c3, .st-dc, .st-em, .st-bo, .st-bq {
        background-color: #2a2a2a !important;
        color: #ffffff !important;
    }
    .stButton>button {
        background-color: #444444;
        color: #ffffff;
    }
    a {
        color: #ffffff !important;
        text-decoration: underline;
        word-break: break-word;
    }
    .post-date {
        font-size: 0.8em;
        color: #aaaaaa;
        margin-left: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------- 인기 갤러리 목록 ---------------------
gallery_list = {
    "주식 갤러리": "stock",
    "해외연예 갤러리": "foreign",
    "프로그램 갤러리": "programming",
    "AI 그림 갤러리": "ai",
    "연애 갤러리": "love",
    "히어로물 갤러리": "superhero",
    "정치 갤러리": "politics",
    "야구 갤러리": "baseball_new9",
    "게임 갤러리": "game",
    "이세계 갤러리": "isekaigal",
    "연예 갤러리": "enter",
    "건강 갤러리": "health",
    "대학 갤러리": "univ",
    "자동차 갤러리": "car",
    "연극/뮤지컬 갤러리": "theatermusical"
}

st.title("🔥 디시인사이드 인기 갤러리 개념글 수집기")
st.markdown(f"#### 📅 오늘 날짜: {datetime.now().strftime('%Y-%m-%d')}")
st.markdown("[👉 디시인사이드 메인으로 가기](https://www.dcinside.com)")

# --------------------- 검색어 입력 ---------------------
search_query = st.sidebar.text_input("🔍 개념글 제목 검색", "")
refresh = st.sidebar.button("🔄 새로고침")
st.sidebar.markdown("---")
st.sidebar.markdown("갤러리 수: " + str(len(gallery_list)))

# --------------------- 개념글 수집 함수 ---------------------
def fetch_gall_contents(gall_id):
    url = f"https://gall.dcinside.com/mgallery/board/lists/?id={gall_id}&exception_mode=recommend&sort_type=N"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.select("tr.ub-content")
        result = []
        for row in rows:
            a_tag = row.select_one("td.gall_tit.ub-word > a")
            date_tag = row.select_one("td.gall_date")
            if not a_tag or not date_tag:
                continue
            title = a_tag.get_text(strip=True)
            href = a_tag.get("href", "")
            date = date_tag.get("title") or date_tag.get_text(strip=True)
            if re.fullmatch(r"\[\d+\]", title):
                continue
            if title and "/board/view/" in href:
                full_url = "https://gall.dcinside.com" + href
                result.append((title, full_url, date))
        return result
    except:
        pass
    return []

# --------------------- 갤러리별 개념글 출력 ---------------------
for name, gall_id in gallery_list.items():
    with st.expander(f"📌 {name} ({gall_id}) 개념글 보기"):
        with st.spinner("개념글 불러오는 중..."):
            try:
                posts = fetch_gall_contents(gall_id)
                if posts:
                    for title, link, date in posts:
                        if search_query.lower() in title.lower():
                            st.markdown(f"- [{title}]({link}) <span class='post-date'>({date})</span>", unsafe_allow_html=True)
                else:
                    st.write("(표시할 개념글이 없습니다)")
            except:
                st.write("❌ 데이터를 불러오지 못했습니다.")

# --------------------- 자동 새로고침 ---------------------
if refresh:
    st.experimental_rerun()
