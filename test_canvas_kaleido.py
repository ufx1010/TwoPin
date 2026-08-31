from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(1000)

    # Check if html2canvas renders canvas element properly
    # Test drawing directly on <canvas id="kaleidoCanvas">
    test_canvas_script = """
    () => {
        const area = document.getElementById('captureArea');
        const kaleidoLayer = document.getElementById('layer-kaleido');
        kaleidoLayer.innerHTML = '<canvas id="kCanvas" width="900" height="900" style="width:100%;height:100%;"></canvas>';
        const cvs = document.getElementById('kCanvas');
        const ctx = cvs.getContext('2d');
        ctx.fillStyle = '#ff0000';
        ctx.fillRect(50, 50, 200, 200);
    }
    """
    page.evaluate(test_canvas_script)
    page.wait_for_timeout(500)

    # Measure html2canvas export time
    t0 = page.evaluate("performance.now()")
    page.evaluate("exportImage(3)")
    page.wait_for_selector("#loading", state="hidden", timeout=10000)
    t1 = page.evaluate("performance.now()")
    print(f"Canvas export time: {t1 - t0:.2f}ms")

    browser.close()
