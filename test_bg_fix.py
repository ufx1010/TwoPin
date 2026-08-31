from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(1000)

    page.click("text=圖層控制")
    page.click("#lTab-bottom")

    # Run test with fixed bg assignment
    page.evaluate("""
        () => {
            window.applyLayerClipPathFixed = function(l) {
                const shape = l.voidShape;
                const hole = l.innerHole;
                const rot = l.voidRotation || 0;
                const key = Object.keys(layerData).find(k => layerData[k] === l);

                if (!l.el || key === 'border' || key === 'kaleido') return;

                l.el.style.transform = `translate(${l.x || 0}px, ${l.y || 0}px) scale(${l.s || 1}) rotate(${rot}deg)`;

                if (shape === 'none' || hole === 0) {
                    l.el.style.clipPath = 'none';
                    l.el.style.background = '';
                    l.el.innerHTML = '';
                    if (l.bg) {
                        if (l.bg.startsWith('url')) l.el.style.backgroundImage = l.bg;
                        else l.el.style.background = l.bg;
                    }
                    return;
                }
                // ...
            };
        }
    """)

    browser.close()
