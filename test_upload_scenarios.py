import base64
from playwright.sync_api import sync_playwright

red_png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
blue_png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")

with open("/tmp/img1.png", "wb") as f:
    f.write(red_png)
with open("/tmp/img2.png", "wb") as f:
    f.write(blue_png)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(1000)

    page.click("text=圖層控制")
    page.click("#lTab-bottom")

    file_input = page.locator("#bgInput")

    # Upload image 1
    file_input.set_input_files("/tmp/img1.png")
    page.wait_for_timeout(300)

    # Change shape & innerHole
    page.select_option("#globalVoidShapeSel", "circle")
    page.fill("#range-gHole", "50")
    page.eval_on_selector("#range-gHole", "el => el.dispatchEvent(new Event('input'))")
    page.wait_for_timeout(300)

    print("Before 2nd upload with circle shape:")
    print("  voidShape:", page.evaluate("layerData.bottom.voidShape"))
    print("  innerHole:", page.evaluate("layerData.bottom.innerHole"))
    print("  bg:", page.evaluate("layerData.bottom.bg.slice(0, 40)"))
    print("  innerHTML:", page.locator("#layer-bottom").evaluate("el => el.innerHTML"))

    # Upload image 2
    file_input.set_input_files("/tmp/img2.png")
    page.wait_for_timeout(300)

    print("\nAfter 2nd upload:")
    print("  voidShape:", page.evaluate("layerData.bottom.voidShape"))
    print("  innerHole:", page.evaluate("layerData.bottom.innerHole"))
    print("  bg:", page.evaluate("layerData.bottom.bg.slice(0, 40)"))
    print("  el style bg:", page.locator("#layer-bottom").evaluate("el => el.style.backgroundImage.slice(0, 40)"))
    print("  innerHTML:", page.locator("#layer-bottom").evaluate("el => el.innerHTML"))

    browser.close()
