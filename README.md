#Linebot

---

### 技術環境

- python、Heroku Cloud、Heroku Postgres、PostgreSQL、PgAdmin、Anacoda、Jupyter、Git

---

### 功能

- 每日抽籤、自動回覆、定時自動喚醒、當日壽星、黑名單詞彙、每日重置抽籤等機制

---

### 注意事項

- 推送至 Heroku 指令 git push heroku HEAD:master
- 推送至 Heroku 需變更 Database 連線方式、Host、Port 變更
- 收回 git commit 方法
  - git reset --soft HEAD~1 回到上一步

### 推送至 heroku 新 方式

- heroku login
- heroku git:remote -a 你-APP-的名字

### 轉移至 New App 上 - 客家教學 - pgAdmin 備份流程 - 2022/07/18 測試

- 安裝 pgAdmin 6.9 版本
  (經過測試 6.10、6.11 等...或舊版本都有問題，例如：無法只顯示單一資料庫，或無法 backup table)
  - 連線到新 Heroku Postgresql database
  - 對著你的 table 點右鍵 選擇 Backup
  - 命名 Filename （命名隨意，不影響）
  - 確認 Data/Obj ects 裡的 Type of objects 只打開 Blobs
  - 修改 Options 裡的 Queries，打開 Use Column Inserts 和 Use Insert Commands
  - 上述完成後點擊右下 Backup 後至使用者文件底下查看檔案
  - 使用記事本打開 Copy 內容，貼到你要轉移的 database query 上
  - 貼上後 修改內容的 UserName，改為你新 database 的 username 即可執行
  - 參考文件 - https://www.dba-ninja.com/2022/04/how-to-copy-a-postgresql-table-to-another-database-using-pgadmin.html

---

### 參考文件

- https://ithelp.ithome.com.tw/users/20122649/ironman/3122
