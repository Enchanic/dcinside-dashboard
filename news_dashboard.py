import streamlit as st
import feedparser
from datetime import datetime
import plotly.express as px
import time

st.set_page_config(page_title="오늘의 뉴스 키워드", layout="centered")
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
    }
    .stApp {
        background-color: #1e1e1e;
    }
    a.link-button {
        display: inline-block;
        background-color: #444;
        color: #fff !important;
        padding: 6px 12px;
        margin: 4px 0;
        border-radius: 6px;
        text-decoration: none;
    }
    a.link-button:hover {
        background-color: #666;
    }
    .post-date {
        font-size: 0.75em;
        color: #aaaaaa;
        margin-left: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📰 오늘의 뉴스 키워드 모아보기")
st.markdown(f"#### 📅 {datetime.now().strftime('%Y-%m-%d')}")

# 실시간 인기 뉴스 제목 수(조회수 대체용) 기반 상위 뉴스 시각화
data = {}
rss_sources = {
    "연합뉴스": "https://www.yonhapnewstv.co.kr/browse/feed/",
    "SBS 뉴스": "https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=01",
    "KBS 뉴스": "https://news.kbs.co.kr/rss/rss.jsp?sc=NEWS",
    "JTBC": "https://fs.jtbc.co.kr/RSS/newsflash.xml",
    "MBC": "https://imnews.imbc.com/rss/newsflash.xml"
}

for source, url in rss_sources.items():
    feed = feedparser.parse(url)
    if feed.entries:
        for entry in feed.entries:
            title = entry.title
            data[title] = data.get(title, 0) + 1

# 상위 기사 10개로 바 차트 생성
top_articles = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]
if top_articles:
    chart = px.bar(x=[title for title, _ in top_articles],
                   y=[count for _, count in top_articles],
                   labels={'x': '뉴스 제목', 'y': '언급 수'},
                   title="실시간 인기 뉴스 그래프 (1분 간격 자동 업데이트)")
    chart.update_layout(xaxis_tickangle=-30, plot_bgcolor='#1e1e1e', paper_bgcolor='#1e1e1e', font_color='white')
    st.plotly_chart(chart, use_container_width=True)

# 1분마다 자동 새로고침
st.experimental_auto_refresh(interval=60 * 1000, key="news_refresh")

# 원문 기사 표시
for source, url in rss_sources.items():
    with st.expander(f"📌 {source} 최신 뉴스"):
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                for entry in feed.entries:
                    title = entry.title
                    link = entry.link
                    date = entry.get("published", "")
                    st.markdown(f"<a class='link-button' href='{link}' target='_blank'>{title}</a> <span class='post-date'>({date})</span>", unsafe_allow_html=True)
            else:
                st.write("(뉴스를 불러올 수 없습니다)")
        except:
            st.write("❌ 뉴스 수집 실패")
