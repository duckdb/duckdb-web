const canvas = document.getElementById('snake-canvas');
if (canvas && !matchMedia('(prefers-reduced-motion: reduce)').matches && !matchMedia('(max-width: 768px)').matches) {
    const ctx = canvas.getContext('2d');
    const svgPaths = document.querySelectorAll('.track-path');

    const SNAKE_LENGTH = 400;
    const SPEED = 500;
    const SNAKE_WIDTH = 1;
    const STEP = 1;
    const MIN_DELAY = 1500;
    const MAX_DELAY = 6000;

    const COLOR_LIGHT = '#EDDD0C';
    const COLOR_DARK = '#665D00';
    const currentColor = () =>
        document.documentElement.classList.contains('darkmode') ? COLOR_DARK : COLOR_LIGHT;

    const width = 1440;
    const height = 842;
    canvas.width = width;
    canvas.height = height;

    ctx.lineCap = 'butt';
    ctx.lineWidth = SNAKE_WIDTH;

    // Pre-sample each path into a Float32Array once. Eliminates getPointAtLength() per frame.
    const pathData = Array.from(svgPaths).map(p => {
        const totalLen = p.getTotalLength();
        const stepCount = Math.ceil(totalLen / STEP) + 1;
        const points = new Float32Array(stepCount * 2);
        for (let i = 0; i < stepCount; i++) {
            const d = Math.min(i * STEP, totalLen);
            const pt = p.getPointAtLength(d);
            points[i * 2] = pt.x;
            points[i * 2 + 1] = pt.y;
        }
        return { totalLen, points, stepCount };
    });

    const SNAKE_STEPS = Math.floor(SNAKE_LENGTH / STEP);
    const opacityLUT = new Float32Array(SNAKE_STEPS + 1);
    for (let i = 0; i <= SNAKE_STEPS; i++) {
        opacityLUT[i] = Math.sin((i / SNAKE_STEPS) * Math.PI);
    }

    let activeSnakes = [];
    let nextPathIndex = 0;
    let timeUntilNextSpawn = 0;
    let lastTime = 0;
    let running = false;
    let rafId = null;

    const getRandomDelay = () => Math.random() * (MAX_DELAY - MIN_DELAY) + MIN_DELAY;

    function spawnSnake() {
        const path = pathData[nextPathIndex];
        activeSnakes.push({
            points: path.points,
            stepCount: path.stepCount,
            totalLen: path.totalLen,
            currentDist: -SNAKE_LENGTH,
        });
        nextPathIndex = (nextPathIndex + 1) % pathData.length;
        timeUntilNextSpawn = getRandomDelay();
    }

    function animate(timestamp) {
        if (!running) return;
        if (!lastTime) lastTime = timestamp;
        const dt = timestamp - lastTime;
        lastTime = timestamp;

        timeUntilNextSpawn -= dt;
        if (timeUntilNextSpawn <= 0) {
            spawnSnake();
        }

        ctx.clearRect(0, 0, width, height);
        ctx.strokeStyle = currentColor();

        for (let i = activeSnakes.length - 1; i >= 0; i--) {
            const snake = activeSnakes[i];
            snake.currentDist += (SPEED * dt) / 1000;

            if (snake.currentDist - SNAKE_LENGTH > snake.totalLen) {
                activeSnakes.splice(i, 1);
                continue;
            }
            drawSnake(snake);
        }
        rafId = requestAnimationFrame(animate);
    }

    function drawSnake(snake) {
        const headDist = snake.currentDist;
        const tailDist = headDist - SNAKE_LENGTH;
        const { points, stepCount } = snake;

        const startLUT = Math.max(0, Math.ceil(-tailDist / STEP));
        const endLUT = Math.min(SNAKE_STEPS, Math.floor((snake.totalLen - tailDist) / STEP));

        let prevX = 0, prevY = 0, havePrev = false;

        for (let j = startLUT; j <= endLUT; j++) {
            const pathIdx = Math.floor((tailDist + j * STEP) / STEP);
            if (pathIdx < 0 || pathIdx >= stepCount) {
                havePrev = false;
                continue;
            }
            const x = points[pathIdx * 2];
            const y = points[pathIdx * 2 + 1];

            if (havePrev) {
                ctx.globalAlpha = opacityLUT[j];
                ctx.beginPath();
                ctx.moveTo(prevX, prevY);
                ctx.lineTo(x, y);
                ctx.stroke();
            }
            prevX = x;
            prevY = y;
            havePrev = true;
        }
    }

    const io = new IntersectionObserver(([entry]) => {
        if (entry.isIntersecting && !running) {
            running = true;
            lastTime = 0;
            rafId = requestAnimationFrame(animate);
        } else if (!entry.isIntersecting && running) {
            running = false;
            if (rafId) cancelAnimationFrame(rafId);
        }
    });
    io.observe(canvas);
}
