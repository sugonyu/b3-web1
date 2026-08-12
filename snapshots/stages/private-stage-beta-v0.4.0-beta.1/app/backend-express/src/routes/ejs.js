/**
 * Flask 대응:
 * bookloop/clients/jinja_product.py의 /jinja/ route가
 * render_template()을 호출하듯, 이 route는 response.render()로 EJS를 호출한다.
 */
import { Router } from "express";

import { getHealthStatusService } from "../services/health.js";

export const ejsRouter = Router();

ejsRouter.get("/", (request, response) => {
  // Flask jinja_reference()의 get_health_status_service() 호출과 같은 service 단계다.
  // render_template("jinja_reference/index.html", health=...)에 대응해
  // response.render("health", { health: ... })로 template에 데이터를 전달한다.
  response.render("health", {
    health: getHealthStatusService(),
  });
});
