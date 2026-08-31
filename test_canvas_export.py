import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(1000)

    # Render kaleidoscope to a canvas and test html2canvas export time
    js_code = """
    async () => {
        // Measure canvas render vs SVG html2canvas
        const area = document.getElementById('captureArea');
        const t0 = performance.now();
        const canvas = await html2canvas(area, { scale: 3, useCORS: true });
        const t1 = performance.now();
        return t1 - t0;
    }
    """
    export_time_original = page.evaluate(js_code)
    print(f"Original html2canvas time: {export_time_original:.2f}ms")

    # Test replacing SVG kaleidoscope with a canvas inside layer-kaleido
    js_convert = """
    () => {
        const layer = document.getElementById('layer-kaleido');
        const svg = layer.querySelector('svg');
        if (!svg) return;
        const w = area.clientWidth;
        const h = area.clientHeight;
        const canvas = document.createElement('canvas');
        canvas.width = w * 2;
        canvas.height = h * 2;
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        const ctx = canvas.getContext('2d');
        const svgData = new XMLSerializer().serializeToString(svg);
        const img = new Image();
        const svgBlob = new Blob([svgData], {type: 'image/svg+xml;charset=utf-8'});
        const url = URL.createObjectURL(svgBlob);
        return new Promise((resolve) => {
            img.onload = () => {
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                URL.revokeObjectURL(url);
                layer.innerHTML = '';
                layer.appendChild(canvas);
                resolve('done');
            };
            img.src = url;
        });
    }
    """
    page.evaluate(js_convert)

    export_time_canvas = page.evaluate(js_code)
    print(f"HTML2Canvas time after rasterizing SVG to Canvas: {export_time_canvas:.2f}ms")

    browser.close()
