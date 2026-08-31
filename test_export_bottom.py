import base64
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(1000)

    # Export image and get canvas data url
    data_url = page.evaluate("""
        async () => {
            const area = document.getElementById('captureArea');
            const canvas = await html2canvas(area, { scale: 1, useCORS: true });
            return canvas.toDataURL('image/png');
        }
    """)

    # Save exported png to inspect
    with open("/tmp/export_sample.png", "wb") as f:
        f.write(base64.b64decode(data_url.split(",")[1]))

    print("Export size:", page.evaluate("""
        async () => {
            const area = document.getElementById('captureArea');
            const canvas = await html2canvas(area, { scale: 1, useCORS: true });
            return { w: canvas.width, h: canvas.height, areaW: area.clientWidth, areaH: area.clientHeight };
        }
    """))

    browser.close()
