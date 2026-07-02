import { chromium } from "playwright";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
await page.goto("http://127.0.0.1:8000", { waitUntil: "networkidle" });
await page.waitForTimeout(3000);

const controls = await page.evaluate(() => {
  const nodes = Array.from(
    document.querySelectorAll("textarea,input,[contenteditable='true'],button")
  );
  return nodes.map((node) => ({
    tag: node.tagName,
    role: node.getAttribute("role"),
    type: node.getAttribute("type"),
    aria: node.getAttribute("aria-label"),
    text: node.textContent?.trim().slice(0, 80),
    placeholder: node.getAttribute("placeholder"),
    className: node.getAttribute("class"),
  }));
});

console.log(JSON.stringify(controls, null, 2));
await browser.close();
