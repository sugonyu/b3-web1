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

test("GET /ejs/ renders the Express health status as HTML", async (testContext) => {
  const baseUrl = await startTestServer(testContext);
  const response = await fetch(`${baseUrl}/ejs/`);
  const html = await response.text();

  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type"), /text\/html/);
  assert.match(html, /BookLoop/);
  assert.match(html, /Express \/ EJS reference/);
  assert.match(html, /express-api/);
  assert.match(html, /http:\/\/127\.0\.0\.1:5000\/jinja\//);
  assert.match(html, /src="\/static\/express-logo\.svg"/);

  const logoResponse = await fetch(`${baseUrl}/static/express-logo.svg`);
  assert.equal(logoResponse.status, 200);
  assert.match(logoResponse.headers.get("content-type"), /image\/svg\+xml/);
});
