#Linebot
___
### 技術環境

- python、Heroku Cloud、Heroku Postgres、PostgreSQL、PgAdmin、Anacoda、Jupyter、Git
___
### 功能 
- 每日抽籤、自動回覆、定時自動喚醒、當日壽星、黑名單詞彙、每日重置抽籤等機制
___
### 注意事項
- 推送至Heroku指令 git push heroku HEAD:master
- 推送至Heroku需變更Database連線方式、Host、Port變更
- git commit 反悔 輸入 git reset --soft HEAD~1 回到上一步

### 推送至heroku 新 app方式
- heroku login
- heroku git:remote -a 你-APP-的名字

### 轉移至New App上 - 客家教學 - pgAdmin備份流程 - 2022/07/18測試
- 安裝pgAdmin 6.9版本 
(經過測試6.10、6.11等...或舊版本都有問題，例如：無法只顯示單一資料庫，或無法backup table) 
   - 連線到新Heroku Postgresql database
   - 對著你的table點右鍵 選擇Backup
   - 命名Filename （命名隨意，不影響）
   - 確認 Data/Obj ects裡的Type of objects 只打開Blobs
   - 修改 Options裡的 Queries，打開Use Column Inserts 和 Use Insert Commands
   - 上述完成後點擊右下Backup後至使用者文件底下查看檔案
   - 使用記事本打開Copy內容，貼到你要轉移的database query 上
   - 貼上後 修改內容的UserName，改為你新database的username即可執行
   - 參考文件 - https://www.dba-ninja.com/2022/04/how-to-copy-a-postgresql-table-to-another-database-using-pgadmin.html
---
### 參考文件
- https://ithelp.ithome.com.tw/users/20122649/ironman/3122