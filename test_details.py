from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(1000)

    # Check all event handlers and upload logic
    page.click("text=圖層控制")

    # Test uploading on bottom layer then top layer or second time on bottom layer
    file_input = page.locator("#bgInput")

    # Upload to bottom
    page.click("#lTab-bottom")
    file_input.set_input_files("/tmp/img1.png")
    page.wait_for_timeout(300)

    # Upload to top
    page.click("#lTab-top")
    file_input.set_input_files("/tmp/img2.png")
    page.wait_for_timeout(300)

    # Upload to bottom again (2nd upload on bottom)
    page.click("#lTab-bottom")
    file_input.set_input_files("/tmp/img1.png")
    page.wait_for_timeout(300)

    print("Bottom layer data:", page.evaluate("layerData.bottom"))
    print("Bottom layer style:", page.locator("#layer-bottom").evaluate("el => ({bg: el.style.background, bgImg: el.style.backgroundImage, size: getComputedStyle(el).backgroundSize, transform: el.style.transform})"))

    browser.close()
