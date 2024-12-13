安裝步驟
1. pip install pytesseract pillow scikit-learn tk
2. 安裝tesseract主程式(需安裝自行抓取繁體中文資料集)  
[https://ithelp.ithome.com.tw/articles/10227263]  
  
左上角打開匯入選項
1. Open Image匯入圖片(匯入資料中的1F.jpg)
2. Import Setting匯入初始設定(匯入資料中的setting.json)
3. Import NodeStat匯入進階設定(匯入資料中的nodestat.json)// 目前不匯入這個，辨識後的結點都會在左上角  
[原本應該是export更正後的設定 之後可直接匯入(不用再匯入setting)，還沒寫好]
4. Extract Nodes 開始辨識
5. 點擊圖片可以跳視窗 增加節點
