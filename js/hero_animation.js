const canvas = document.getElementById('snake-canvas');
if (canvas) {
    const ctx = canvas.getContext('2d');
    const svgPaths = document.querySelectorAll('.track-path');
    
    // --- CONFIGURATION ---
    const SNAKE_LENGTH = 400; // Gradient tail length
    const SPEED = 500; // Pixels per second
    const SNAKE_WIDTH = 1;
    
    const isDark = () => document.documentElement.classList.contains('darkmode');
    let COLOR = isDark() ? '#665D00' : '#EDDD0C';
    new MutationObserver(() => { COLOR = isDark() ? '#665D00' : '#EDDD0C'; })
        .observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
    
    // Random delay range (in milliseconds)
    const MIN_DELAY = 1500; 
    const MAX_DELAY = 6000;
    
    // --- SETUP ---
    const width = 1440;
    const height = 842;
    canvas.width = width;
    canvas.height = height;
    
    ctx.lineCap = 'butt'; 
    ctx.lineWidth = SNAKE_WIDTH;
    
    // Pre-calculate path lengths
    const pathData = Array.from(svgPaths).map(p => ({
        el: p,
        totalLen: p.getTotalLength()
    }));
    
    // --- STATE ---
    let activeSnakes = [];
    let nextPathIndex = 0;
    let timeUntilNextSpawn = 0;
    let lastTime = 0;
    
    function getRandomDelay() {
        return Math.random() * (MAX_DELAY - MIN_DELAY) + MIN_DELAY;
    }
    
    function spawnSnake() {
        const pIndex = nextPathIndex;
        const path = pathData[pIndex];
        
        activeSnakes.push({
            ...path,
            currentDist: -SNAKE_LENGTH, 
            done: false
        });
        nextPathIndex = (nextPathIndex + 1) % pathData.length;
        timeUntilNextSpawn = getRandomDelay(); 
    }
    
    // --- ANIMATION LOOP ---
    function animate(timestamp) {
        if (!lastTime) lastTime = timestamp;
        const dt = (timestamp - lastTime); 
        lastTime = timestamp;
    
        timeUntilNextSpawn -= dt;
        if (timeUntilNextSpawn <= 0) {
            spawnSnake();
        }
    
        ctx.clearRect(0, 0, width, height);
    
        for (let i = activeSnakes.length - 1; i >= 0; i--) {
            const snake = activeSnakes[i];
            snake.currentDist += (SPEED * dt) / 1000;
    
            if (snake.currentDist - SNAKE_LENGTH > snake.totalLen) {
                activeSnakes.splice(i, 1);
                continue;
            }
            drawSnakeSmooth(snake);
        }
        requestAnimationFrame(animate);
    }

    function drawSnakeSmooth(snake) {
        const headDist = snake.currentDist;
        const tailDist = headDist - SNAKE_LENGTH;
        const step = .5;

        let prevPoint = null;

        for (let d = 0; d <= SNAKE_LENGTH; d += step) {
            const currentPosOnPath = tailDist + d;

            if (currentPosOnPath < 0 || currentPosOnPath > snake.totalLen) {
                prevPoint = null;
                continue;
            }

            const point = snake.el.getPointAtLength(currentPosOnPath);

            if (prevPoint) {
                const t = d / SNAKE_LENGTH;
                const opacity = Math.sin(t * Math.PI); 

                ctx.beginPath();
                ctx.moveTo(prevPoint.x, prevPoint.y);
                ctx.lineTo(point.x, point.y);
                ctx.globalAlpha = opacity;
                ctx.strokeStyle = COLOR;
                ctx.stroke();
            }
            prevPoint = point;
        }
    }

    requestAnimationFrame(animate);
}
