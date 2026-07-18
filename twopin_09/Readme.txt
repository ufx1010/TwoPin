這份清單整理了您目前所有調整過的關鍵設定，方便您未來自行維護或進行二次微調。這些設定通常位於 HTML 檔案的 <style>（CSS）與 <script>（JavaScript）區塊中。
1. 基礎排版與預設值 (JavaScript 部分)
這些設定控制了程式啟動時的初始狀態。請在 <script> 標籤內尋找 conf 物件與相關函式：
字體大小預設值：修改 conf 物件中的 titleSize 與 contentSize。
範例：const conf = { titleSize: 30, contentSize: 24, gap: 15 };
行距 (Gap)：修改 conf 中的 gap 數值。數值越小越緊湊。
字體行高 (Line Height)：在 render() 函式內，搜尋 * 1.3。將其改為 * 1.0 或 * 1.1 可讓文字排版更為緊密。
2. 介面初始狀態 (HTML 部分)
這些設定控制選單和輸入框在網頁剛打開時的樣子：
預設書寫方向：在 <select id="text-dir"> 中，將 selected 屬性移至橫排選項。
<option value="h-lr" selected>橫排 (由左至右)</option>
預設字體對齊：在 <select id="text-align"> 中，將 selected 移至置中選項。
<option value="center" selected>置中對齊</option>
預設文字顏色：修改 <input type="color" id="text-color"> 的 value。
範例：value="#ff0000" (代表紅色)。
控制面板數值顯示：在 HTML 的 <span> 標籤中手動修正顯示的數字（例如 id="val-title-size"），確保顯示數值與 conf 中的初始值同步。
3. 外觀樣式 (CSS 部分)
位於 <style> 標籤內：
輸入框內字體大小：修改 textarea 選擇器中的 font-size。
範例：textarea { font-size: 10px; }
4. 自訂字型匯入 (CSS 與 HTML)
若要加入新的字型（如落雁體）：
CSS @font-face：必須在 <style> 區塊最上方加入：
@font-face {
    font-family: '自訂字型名稱';
    src: url('檔案名稱.ttf') format('truetype');
}
HTML 選單：在 <select id="font-family-select"> 下新增一行：
<option value="'自訂字型名稱', serif">顯示名稱</option>
重要提示：務必確保字型檔與 HTML 檔案在同一個資料夾內。
修改小撇步 (維護建議)
養成備份習慣：在大幅修改程式碼前，先將整個 HTML 檔案內容複製一份到記事本備份。
善用搜尋：在編輯器中使用「搜尋功能 (Ctrl+F)」，直接搜尋標籤 ID（如 text-dir 或 gap）可以快速找到目標位置。
確認存檔：每次修改後，請務必點擊編輯器上的「儲存」，再到預覽頁面按下「重新整理 (Refresh)」，變更才會生效。
這份清單涵蓋了我們這幾次對話的所有調整核心，希望能協助您更順利地自行客製化您的網頁工具！
