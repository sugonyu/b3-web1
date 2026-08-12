import assert from "node:assert/strict";
import test from "node:test";

import { createApp } from "../src/app.js";

async function startTestServer(testContext) {
  const server = createApp().listen(0, "127.0.0.1");

  await new Promise((resolve) => server.once("listening", resolve));
  testContext.after(() => new Promise((resolve) => server.close(resolve)));

  const address = server.address();
  return `http://127.0.0.1:${address.port}`;
}

test("GET /api/health returns the Express service status", async (testContext) => {
  const baseUrl = await startTestServer(testContext);
  const response = await fetch(`${baseUrl}/api/health`);

  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), {
    app: "BookLoop",
    service: "express-api",
    status: "ok",
    version: "0.1.0",
  });
});

test("GET /api/health allows the local React origin", async (testContext) => {
  const baseUrl = await startTestServer(testContext);
  const response = await fetch(`${baseUrl}/api/health`, {
    headers: {
      Origin: "http://127.0.0.1:5173",
    },
  });

  assert.equal(response.status, 200);
  assert.equal(
    response.headers.get("access-control-allow-origin"),
    "http://127.0.0.1:5173",
  );
});
