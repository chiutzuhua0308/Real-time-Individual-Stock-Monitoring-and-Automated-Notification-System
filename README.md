# Real-time-Individual-Stock-Monitoring-and-Automated-Notification-System
An automated RSS tool consolidating multi-source financial news for real-time stock tracking

📖 專案簡介
本專案是一套基於 RSS 技術 的自動化個股新聞追蹤工具。開發初衷是為了解決投資者在多個財經媒體間切換的低效問題，並確保使用者能第一時間掌握影響股價的關鍵資訊（Market-moving Information）。

本系統曾應用於 證券投資競賽 並協助開發者榮獲 第二名 佳績。

✨ 核心功能
多來源整合：利用 Google News RSS 彙整各主流財經媒體，解決資訊碎片化問題。

即時自動更新：內建 st_autorefresh 機制，支援使用者自定義更新頻率（分鐘/小時）。

智能化介面：自動分離新聞標題與媒體來源，並提供大字體優化閱讀體驗。

時區自動校正：針對雲端部署優化，全面採用 Asia/Taipei (UTC+8) 中文時間顯示。

高度客製化：支援多檔個股同時追蹤，並使用縮放面板（Expander）保持介面整潔。

🛠️ 技術棧 (Tech Stack)
Frontend: Streamlit (Dashboard 實作)

Backend: Python (Feedparser RSS 解析)

Deployment: Streamlit Community Cloud / GitHub

Data Handling: PyTZ (時區處理), Urllib (編碼優化)
