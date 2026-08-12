/**
 * Flask 대응: app/backend/bookloop/api.py의 health()
 * Blueprint route와 Express Router route는 모두 service 결과를 JSON으로 바꾸는 HTTP adapter다.
 */
import { Router } from "express";

import { getHealthStatusService } from "../services/health.js";

export const healthRouter = Router();

healthRouter.get("/health", (request, response) => {
  response.status(200).json(getHealthStatusService());
});
