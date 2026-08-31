import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(1000)

    # 1. Select Layer tab
    page.click("text=圖層控制")
    page.wait_for_timeout(300)

    # 2. Select bottom layer
    page.click("#lTab-bottom")
    page.wait_for_timeout(300)

    # Create a dummy image file 1
    import base64
    # 100x100 red image
    red_png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
    with open("/tmp/test1.png", "wb") as f:
        f.write(red_png)
    with open("/tmp/test2.png", "wb") as f:
        f.write(red_png)

    # First upload
    file_input = page.locator("#bgInput")
    file_input.set_input_files("/tmp/test1.png")
    page.wait_for_timeout(500)

    # Check bottom layer style/content
    layer_bottom = page.locator("#layer-bottom")
    print("After 1st upload:")
    print("  bg:", layer_bottom.evaluate("el => el.style.backgroundImage"))
    print("  clipPath:", layer_bottom.evaluate("el => el.style.clipPath"))
    print("  transform:", layer_bottom.evaluate("el => el.style.transform"))
    print("  innerHTML:", layer_bottom.evaluate("el => el.innerHTML"))

    # Change shape to circle and hole to 50, rotate 30
    page.select_option("#globalVoidShapeSel", "circle")
    page.fill("#range-gHole", "50")
    page.eval_on_selector("#range-gHole", "el => el.dispatchEvent(new Event('input'))")
    page.wait_for_timeout(300)

    print("After shape change:")
    print("  bg:", layer_bottom.evaluate("el => el.style.backgroundImage"))
    print("  clipPath:", layer_bottom.evaluate("el => el.style.clipPath"))
    print("  innerHTML:", layer_bottom.evaluate("el => el.innerHTML"))

    # Second upload
    file_input.set_input_files("/tmp/test2.png")
    page.wait_for_timeout(500)

    print("After 2nd upload:")
    print("  bg:", layer_bottom.evaluate("el => el.style.backgroundImage"))
    print("  clipPath:", layer_bottom.evaluate("el => el.style.clipPath"))
    print("  transform:", layer_bottom.evaluate("el => el.style.transform"))
    print("  innerHTML:", layer_bottom.evaluate("el => el.innerHTML"))

    # Test export time
    t0 = time.time()
    page.click("text=清除&/存檔")
    page.wait_for_timeout(300)
    page.click("text=導出高清 WebP 作品")
    # Wait for loading mask to disappear or file download
    page.wait_for_selector("#loading", state="hidden", timeout=30000)
    t1 = time.time()
    print(f"Export time: {t1 - t0:.2f} seconds")

    browser.close()
