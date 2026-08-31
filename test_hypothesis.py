import base64
from playwright.sync_api import sync_playwright

red_png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")

with open("/tmp/img1.png", "wb") as f:
    f.write(red_png)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(1000)

    page.click("text=圖層控制")
    page.click("#lTab-bottom")

    file_input = page.locator("#bgInput")

    # 1st upload
    file_input.set_input_files("/tmp/img1.png")
    page.wait_for_timeout(300)
    print("1. After 1st upload:")
    print("   style.background:", page.locator("#layer-bottom").evaluate("el => el.style.background"))
    print("   computed backgroundSize:", page.locator("#layer-bottom").evaluate("el => getComputedStyle(el).backgroundSize"))
    print("   computed backgroundRepeat:", page.locator("#layer-bottom").evaluate("el => getComputedStyle(el).backgroundRepeat"))

    # Set shape
    page.select_option("#globalVoidShapeSel", "circle")
    page.fill("#range-gHole", "50")
    page.eval_on_selector("#range-gHole", "el => el.dispatchEvent(new Event('input'))")
    page.wait_for_timeout(300)
    print("2. After setting circle shape:")
    print("   style.background:", page.locator("#layer-bottom").evaluate("el => el.style.background"))

    # 2nd upload
    file_input.set_input_files("/tmp/img1.png")
    page.wait_for_timeout(300)
    print("3. After 2nd upload:")
    print("   style.background:", page.locator("#layer-bottom").evaluate("el => el.style.background"))
    print("   computed backgroundSize:", page.locator("#layer-bottom").evaluate("el => getComputedStyle(el).backgroundSize"))
    print("   computed backgroundRepeat:", page.locator("#layer-bottom").evaluate("el => getComputedStyle(el).backgroundRepeat"))

    browser.close()
