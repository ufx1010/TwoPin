from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(1000)

    # Test Canvas drawing function implementation
    canvas_impl = """
    function drawKaleidoscopeCanvas() {
        const b = layerData.kaleido;
        const w = area.clientWidth;
        const h = area.clientHeight;
        if (w === 0 || h === 0) return;

        let canvas = b.el.querySelector('canvas');
        if (!canvas) {
            canvas = document.createElement('canvas');
            b.el.innerHTML = '';
            b.el.appendChild(canvas);
        }

        // Use 2x DPR or fixed crisp resolution for high DPI
        const dpr = window.devicePixelRatio || 2;
        canvas.width = w * dpr;
        canvas.height = h * dpr;
        canvas.style.width = '100%';
        canvas.style.height = '100%';

        const ctx = canvas.getContext('2d');
        ctx.scale(dpr, dpr);
        ctx.clearRect(0, 0, w, h);

        // Fill dark background
        ctx.fillStyle = '#050505';
        ctx.fillRect(0, 0, w, h);

        const centerX = w / 2, centerY = h / 2;
        const holeVal = b.innerHole;

        if (b.seed.length === 0) {
            for (let i = 0; i < 2000; i++) {
                b.seed.push({
                    x: Math.random(), y: Math.random(),
                    size: Math.random(),
                    type: ['arc', 'blob', 'dot', 'curve', 'flake'][Math.floor(Math.random() * 5)],
                    color: `hsl(${Math.random() * 360}, ${30 + Math.random() * 50}%, ${30 + Math.random() * 50}%)`,
                    rot: Math.random() * 360, curve: Math.random()
                });
            }
        }

        if (b.patternType === 'kaleido') {
            const segments = 10;
            const maxRadius = Math.sqrt(w * w + h * h) / 2 * (b.spread / 100);
            for (let i = 0; i < b.density; i++) {
                const s = b.seed[i]; if (!s) continue;
                const size = b.size * (0.4 + s.size);
                const radius = s.x * maxRadius;
                const angle = s.y * (Math.PI * 2 / segments);

                for (let j = 0; j < segments; j++) {
                    const currentAngle = angle + (j * Math.PI * 2 / segments);
                    const px = centerX + Math.cos(currentAngle) * radius;
                    const py = centerY + Math.sin(currentAngle) * radius;

                    if (isInsideVoid(px, py, w, h, b.voidShape, holeVal, b.voidRotation)) continue;
                    if (px < -50 || px > w + 50 || py < -50 || py > h + 50) continue;

                    let col = isBlackAndWhite ? '#ffffff' : s.color;
                    ctx.save();
                    ctx.translate(px, py);
                    ctx.rotate((s.rot + j * (360 / segments)) * Math.PI / 180);

                    if (s.type === 'arc') {
                        ctx.beginPath();
                        ctx.ellipse(0, 0, size, size * s.curve, 0, Math.PI, 2 * Math.PI);
                        ctx.strokeStyle = col;
                        ctx.globalAlpha = 0.6;
                        ctx.lineWidth = 0.8;
                        ctx.stroke();
                    } else if (s.type === 'blob') {
                        ctx.beginPath();
                        ctx.moveTo(0, -size);
                        ctx.quadraticCurveTo(size * s.curve, 0, 0, size);
                        ctx.quadraticCurveTo(-size * s.curve, 0, 0, -size);
                        ctx.fillStyle = col;
                        ctx.globalAlpha = 0.4;
                        ctx.fill();
                    } else if (s.type === 'dot') {
                        ctx.beginPath();
                        ctx.arc(0, 0, size / 3, 0, Math.PI * 2);
                        ctx.fillStyle = col;
                        ctx.globalAlpha = 0.5;
                        ctx.fill();
                    } else {
                        ctx.beginPath();
                        ctx.rotate(45 * Math.PI / 180);
                        ctx.rect(-size / 4, -size / 4, size / 2, size / 2);
                        ctx.fillStyle = col;
                        ctx.globalAlpha = 0.4;
                        ctx.fill();
                    }
                    ctx.restore();
                }
            }
        }
        b.el.style.filter = isBlackAndWhite ? 'grayscale(100%) contrast(120%)' : 'none';
    }
    """
    page.evaluate(canvas_impl)
    page.evaluate("drawKaleidoscopeCanvas()")
    page.wait_for_timeout(300)

    t0 = page.evaluate("performance.now()")
    page.evaluate("exportImage(3)")
    page.wait_for_selector("#loading", state="hidden", timeout=10000)
    t1 = page.evaluate("performance.now()")
    print(f"Canvas export time: {t1 - t0:.2f}ms")

    browser.close()
