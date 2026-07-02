import { chromium } from "playwright";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
page.setDefaultTimeout(60_000);

await page.goto("http://127.0.0.1:8000", { waitUntil: "networkidle" });
await page.waitForTimeout(3000);

const newSession = page.getByText("New Session", { exact: true }).last();
if (await newSession.isVisible().catch(() => false)) {
  await newSession.click();
  await page.waitForTimeout(1000);
}

const input = page.locator("textarea[placeholder='Type a message...']");
await input.waitFor({ state: "visible", timeout: 30_000 });
await input.fill(
  'Dung search_documents voi query "MCP". Dung sql_query voi SQL "SELECT * FROM agent_metrics". Tom tat ngan ket qua.'
);
await page.locator("button.send-message-btn").click();
await page.waitForFunction(
  () => document.body.innerText.includes("820") || document.body.innerText.includes("2400"),
  null,
  { timeout: 120_000 }
);
await page.waitForTimeout(5000);
await page.screenshot({ path: "artifacts/screenshots/adk_web_w2_chat.png", fullPage: true });

await page.getByText("Traces", { exact: true }).click();
await page.waitForTimeout(2000);
await page.screenshot({ path: "artifacts/screenshots/adk_web_w2_trace.png", fullPage: true });

console.log("artifacts/screenshots/adk_web_w2_chat.png");
console.log("artifacts/screenshots/adk_web_w2_trace.png");
await browser.close();
