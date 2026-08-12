/**
 * Flask 대응: app/backend/bookloop/services/health.py
 * 두 service 모두 HTTP request/response를 모르고 상태 object/dict만 반환한다.
 */
export function getHealthStatusService() {
  // Flask get_health_status_service()의 dict와 같은 view/API용 상태 object다.
  return {
    app: "BookLoop",
    service: "express-api",
    status: "ok",
    version: "0.1.0",
  };
}
