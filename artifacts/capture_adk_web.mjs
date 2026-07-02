import { chromium } from "playwright";

const outputDir = "artifacts/screenshots";
const baseUrl = "http://127.0.0.1:8000";

async function sendPrompt(page, prompt, waitForText) {
  const input = page.locator("textarea[placeholder='Type a message...']");
  await input.waitFor({ state: "visible", timeout: 30_000 });
  await input.fill(prompt);
  await page.locator("button.send-message-btn").click();
  await page.waitForFunction(
    (text) => document.body.innerText.includes(text),
    waitForText,
    { timeout: 120_000 }
  );
  await page.waitForTimeout(3000);
}

async function screenshot(page, name) {
  await page.screenshot({ path: `${outputDir}/${name}.png`, fullPage: true });
  console.log(`${outputDir}/${name}.png`);
}

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
page.setDefaultTimeout(60_000);

await page.goto(baseUrl, { waitUntil: "networkidle" });
await page.waitForTimeout(3000);
await screenshot(page, "adk_web_home");

await sendPrompt(
  page,
  "Transfer sang search_agent de tim web ve multi-agent orchestration.",
  "Agent card"
);
await screenshot(page, "adk_web_w1_chat");
await page.getByText("Traces", { exact: true }).click();
await page.waitForTimeout(2000);
await screenshot(page, "adk_web_w1_trace");

await page.getByText("Events", { exact: true }).click();
await sendPrompt(
  page,
  "Buoc 1: dung search_documents tim MCP. Buoc 2: dung sql_query SELECT * FROM agent_metrics. Buoc 3: tom tat bao cao ngan.",
  "agent_metrics"
);
await screenshot(page, "adk_web_w2_chat");
await page.getByText("Traces", { exact: true }).click();
await page.waitForTimeout(2000);
await screenshot(page, "adk_web_w2_trace");

await browser.close();
