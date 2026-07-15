網頁功能分析
📋 核心功能模組
1. 翻譯引擎 (第 99-122 行)
JavaScript
async function translateText()
使用 Google Translate API (translate.googleapis.com)
支援 5 種語言互譯：中文、日文、韓文、英文、坦米爾文
提取結果的第一層陣列並串接所有翻譯片段
具有視覺反饋：綠色閃爍動畫表示翻譯中
特點：

非同步 fetch 請求，支援錯誤捕捉
若翻譯失敗顯示「翻譯失敗」訊息
2. 語音識別 (第 89-97 行)
JavaScript
function startDictation()
使用 Web Speech API 進行語音輸入
語言跟隨「來源語言」設定
紅色閃爍動畫表示錄音中
將辨識結果追加到輸入框
特點：相容 webkit 和標準版本的 SpeechRecognition API

3. 網路搜尋 (第 77-87 行)
JavaScript
function searchWeb()
將輸入文字作為搜尋關鍵詞
開啟 Google 搜尋新視窗
在結果框顯示搜尋狀態
4. 文字轉語音 (第 134-138 行)
JavaScript
function speakText()
朗讀結果框中的文字
語言跟隨「目標語言」設定
使用 Web Speech Synthesis API
5. 本地儲存 (第 69-74 行)
JavaScript
window.onload / saveLang()
儲存用戶選擇的「來源語言」和「目標語言」
頁面刷新時自動恢復設定
🎨 UI/UX 設計
功能區	組成
第一按鈕列 (6 格)	字體縮小、來源語言、翻譯、搜尋、目標語言、字體放大
第二按鈕列 (4 格)	語音輸入、清空、複製、播放
輸入區	textarea，支援自動換行
結果區	div，綠色背景，可滾動
動畫效果：

.recording 類：紅色邊框閃爍 (表示正在錄音)
.translating 類：綠色邊框閃爍 (表示翻譯中)
⚙️ 技術棧
技術	用途
Web Speech API	語音輸入 / 文字轉語音
Fetch API	翻譯請求
localStorage	語言偏好儲存
Clipboard API	複製結果
CSS Flexbox/Grid	響應式排版
⚠️ 潛在問題
Google Translate API - 使用 googleapis.com 的非官方端點，可能不穩定
無錯誤處理 - 語音識別失敗未有提示
無輸入驗證 - 空白輸入時未完全防止
無搜尋歷史 - 搜尋功能僅開新視窗，無本地記錄
