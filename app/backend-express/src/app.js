/**
 * Flask 대응: app/backend/bookloop/__init__.py의 create_app()
 * Flask가 extension과 Blueprint를 조립하듯 Express는 middleware와 Router를 조립한다.
 */
import cors from "cors";
import express from "express";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { ejsRouter } from "./routes/ejs.js";
import { healthRouter } from "./routes/health.js";

const currentDirectory = path.dirname(fileURLToPath(import.meta.url));

const localClientOrigins = [
  "http://127.0.0.1:3000",
  "http://localhost:3000",
  "http://127.0.0.1:5173",
  "http://localhost:5173",
  "http://127.0.0.1:8080",
  "http://localhost:8080",
];

export function createApp() {
  const app = express();

  // Flask의 templates/ + render_template()에 대응하는 Express/EJS 설정이다.
  app.set("views", path.join(currentDirectory, "views"));
  app.set("view engine", "ejs");

  // Flask의 static/ + url_for("static", ...)와 같은 local asset 제공 경계다.
  app.use("/static", express.static(path.join(currentDirectory, "public")));

  // Flask CORS 설정과 같은 local React/static client 경계를 허용한다.
  app.use(
    "/api",
    cors({
      origin: localClientOrigins,
    }),
  );

  app.use("/api", healthRouter);
  // Flask create_app()의 app.register_blueprint(jinja_client)와 같은 route module 등록이다.
  // Express Router는 /ejs/에서 EJS를, Flask Blueprint는 /jinja/에서 Jinja를 render한다.
  app.use("/ejs", ejsRouter);

  return app;
}
