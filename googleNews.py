import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# 設定網頁標題
st.set_page_config(page_title="個股新聞追蹤器", page_icon="📈", layout="wide")

# 定義台灣時區
tw_tz = pytz.timezone('Asia/Taipei')

# 1. 側邊欄設定
with st.sidebar:
    st.header("⚙️ 追蹤設定")
    user_input = st.text_input("輸入個股名稱 (多個用逗號隔開)", "台積電, NVDA")
    
    st.write("---")
    st.header("⏰ 更新頻率")
    unit = st.selectbox("更新單位", ["分鐘", "小時"])
    interval_val = st.number_input(f"每隔多少{unit}更新一次", min_value=1, value=10)
    refresh_ms = (interval_val * 60 * 1000) if unit == "分鐘" else (interval_val * 60 * 60 * 1000)

st_autorefresh(interval=refresh_ms, key="news_refresh_timer")

# 解析個股清單
stock_list = [s.strip() for s in user_input.replace('，', ',').split(',') if s.strip()]

# 獲取現在的台灣時間 (中文格式)
now_tw = datetime.now(tw_tz).strftime('%Y年%m月%d日 %H:%M:%S')

st.title("📈 持股新聞自動監測")
st.caption(f"🚀 自動更新中 | 🕒 台灣最後更新：{now_tw}")

# 3. RSS 抓取與時間格式化
def get_news_via_rss(stock_name):
    encoded_query = urllib.parse.quote(stock_name)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    feed = feedparser.parse(rss_url)
    all_news = []
    
    for entry in feed.entries[:8]:
        try:
            # 轉換為台灣時區並格式化為中文
            published_struct = entry.published_parsed
            dt_utc = datetime(*published_struct[:6], tzinfo=pytz.utc)
            dt_tw = dt_utc.astimezone(tw_tz)
            # 格式改成：2026年01月22日 16:30
            formatted_time = dt_tw.strftime('%Y年%m月%d日 %H:%M')
        except:
            formatted_time = entry.published
            
        # 優化標題：嘗試切分標題與來源 (Google News RSS 標題格式通常是 "標題 - 來源")
        full_title = entry.title
        if " - " in full_title:
            display_title, source = full_title.rsplit(" - ", 1)
        else:
            display_title, source = full_title, "新聞"
            
        all_news.append({
            "標題": display_title,
            "來源": source,
            "時間": formatted_time,
            "連結": entry.link
        })
    return all_news

# 4. 畫面顯示
if stock_list:
    for stock in stock_list:
        with st.expander(f"🔍 {stock} 相關新聞", expanded=True):
            news_data = get_news_via_rss(stock)
            if news_data:
                for news in news_data:
                    col1, col2 = st.columns([4, 1.2])
                    with col1:
                        # 顯示來源與標題
                        st.markdown(f"**[{news['來源']}]** [{news['標題']}]({news['連結']})")
                    with col2:
                        # 顯示中文日期
                        st.caption(f"📅 {news['時間']}")
            else:
                st.info(f"目前沒有找到關於 {stock} 的新聞。")
else:
    st.warning("請在左側選單輸入要追蹤的個股。")