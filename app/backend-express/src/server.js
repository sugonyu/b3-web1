/**
 * Flask 대응: app/backend/run.py
 * 둘 다 application을 만든 뒤 개발 port를 열지만, DB schema 준비는 현재 Flask만 한다.
 */
import { createApp } from "./app.js";

const port = Number.parseInt(process.env.PORT ?? "3001", 10);
const app = createApp();

app.listen(port, "127.0.0.1", () => {
  console.log(`BookLoop Express health API: http://127.0.0.1:${port}/api/health`);
  console.log(`BookLoop Express EJS:        http://127.0.0.1:${port}/ejs/`);
});
