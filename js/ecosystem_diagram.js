(function () {
  "use strict";

  var diagram = document.querySelector(".ecosystem-diagram");
  if (!diagram) return;

  /* --- Configuration --- */

  var STIFFNESS = 0.6;
  var DAMPING = 0.5;
  var SNAKE_LENGTH = 200;
  var SNAKE_SPEED = 300;
  var SNAKE_WIDTH = 1.5;
  var MIN_DELAY = 1500;
  var MAX_DELAY = 4000;

  /* --- Dark mode color --- */

  var isDark = function () {
    return document.documentElement.classList.contains("darkmode");
  };
  var snakeColor = isDark() ? "#665D00" : "#EDDD0C";
  new MutationObserver(function () {
    snakeColor = isDark() ? "#665D00" : "#EDDD0C";
  }).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["class"],
  });

  /* --- DOM references --- */

  var draggables = diagram.querySelectorAll(".draggable");
  var svgCanvas = document.getElementById("ecosystem-connector-canvas");
  var pulseCanvas = document.getElementById("ecosystem-pulse-canvas");
  var pulseCtx = pulseCanvas ? pulseCanvas.getContext("2d") : null;

  var basePaths = {
    leftTop: document.getElementById("eco-base-left-top"),
    leftBottom: document.getElementById("eco-base-left-bottom"),
    right: document.getElementById("eco-base-right"),
    rightBottom: document.getElementById("eco-base-right-bottom"),
  };
  var basePathArray = [basePaths.leftTop, basePaths.leftBottom, basePaths.right, basePaths.rightBottom];

  /* --- State --- */

  var animationFrameId = null;
  var isDraggingGlobal = false;
  var dragDistance = 0;
  var activeSnakes = [];
  var nextPathIndex = 0;
  var timeUntilNextSpawn = 0;
  var lastPulseTime = 0;
  var pulseRunning = false;

  var physicsBoxes = Array.prototype.map.call(draggables, function (el) {
    return {
      el: el,
      isDragging: false,
      pos: { x: 0, y: 0 },
      vel: { x: 0, y: 0 },
      startMouse: { x: 0, y: 0 },
    };
  });

  /* --- Helpers --- */

  function getEdgeXY(id, edge) {
    var el = document.getElementById(id);
    if (!el) return { x: 0, y: 0 };
    var rect = el.getBoundingClientRect();
    if (edge === "left") return { x: rect.left, y: rect.top + rect.height / 2 };
    if (edge === "right") return { x: rect.right, y: rect.top + rect.height / 2 };
    return { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 };
  }

  function createRoundedOrthoPath(x1, y1, x2, y2) {
    var midX = x1 + (x2 - x1) / 2;
    var dy = y2 - y1;
    var absDy = Math.abs(dy);
    var absDx = Math.abs(x2 - x1);
    var dirY = dy >= 0 ? 1 : -1;
    var r = Math.min(16, absDy / 2, absDx / 2);

    if (absDy < 10 || absDx < 2) return "M " + x1 + " " + y1 + " L " + x2 + " " + y1;
    if (x2 < x1) {
      return (
        "M " + x1 + " " + y1 +
        " Q " + midX + " " + y1 + " " + midX + " " + (y1 + dy / 2) +
        " T " + x2 + " " + y2
      );
    }

    return (
      "M " + x1 + " " + y1 +
      " L " + (midX - r) + " " + y1 +
      " Q " + midX + " " + y1 + ", " + midX + " " + (y1 + r * dirY) +
      " L " + midX + " " + (y2 - r * dirY) +
      " Q " + midX + " " + y2 + ", " + (midX + r) + " " + y2 +
      " L " + x2 + " " + y2
    );
  }

  /* --- Connector lines --- */

  function updateLines() {
    if (!basePaths.leftTop || !svgCanvas) return;

    var canvasRect = svgCanvas.getBoundingClientRect();
    svgCanvas.setAttribute("viewBox", "0 0 " + canvasRect.width + " " + canvasRect.height);
    var ox = canvasRect.left;
    var oy = canvasRect.top;

    function rel(pt) {
      return { x: pt.x - ox, y: pt.y - oy };
    }

    var s = rel(getEdgeXY("eco-box-storage", "right"));
    var d = rel(getEdgeXY("eco-box-db", "right"));
    var cL = rel(getEdgeXY("eco-box-clients", "left"));
    var cR = rel(getEdgeXY("eco-box-clients", "right"));
    var f = rel(getEdgeXY("eco-box-formats", "left"));
    var ex = rel(getEdgeXY("eco-box-exchange", "left"));

    basePaths.leftTop.setAttribute("d", createRoundedOrthoPath(s.x, s.y, cL.x, cL.y - 15));
    basePaths.leftBottom.setAttribute("d", createRoundedOrthoPath(d.x, d.y, cL.x, cL.y + 15));
    basePaths.right.setAttribute("d", createRoundedOrthoPath(cR.x, cR.y - 15, f.x, f.y));
    basePaths.rightBottom.setAttribute("d", createRoundedOrthoPath(cR.x, cR.y + 15, ex.x, ex.y));
  }

  /* --- Pulse canvas --- */

  function resizePulseCanvas() {
    if (!pulseCanvas || !pulseCanvas.parentElement) return;
    var rect = pulseCanvas.parentElement.getBoundingClientRect();
    pulseCanvas.width = rect.width;
    pulseCanvas.height = rect.height;
  }

  function isPulseVisible() {
    return pulseCanvas && pulseCanvas.offsetParent !== null;
  }

  function spawnSnake() {
    var pathEl = basePathArray[nextPathIndex];
    if (!pathEl) return;
    var len = pathEl.getTotalLength();
    if (len === 0) return;

    activeSnakes.push({
      el: pathEl,
      totalLen: len,
      currentDist: -SNAKE_LENGTH,
    });
    nextPathIndex = (nextPathIndex + 1) % basePathArray.length;
    timeUntilNextSpawn = Math.random() * (MAX_DELAY - MIN_DELAY) + MIN_DELAY;
  }

  function drawSnake(snake) {
    var headDist = snake.currentDist;
    var tailDist = headDist - SNAKE_LENGTH;
    var step = 0.5;
    var prevPoint = null;

    pulseCtx.strokeStyle = snakeColor;
    pulseCtx.lineWidth = SNAKE_WIDTH;

    for (var d = 0; d <= SNAKE_LENGTH; d += step) {
      var posOnPath = tailDist + d;
      if (posOnPath < 0 || posOnPath > snake.totalLen) {
        prevPoint = null;
        continue;
      }

      var point = snake.el.getPointAtLength(posOnPath);
      if (prevPoint) {
        pulseCtx.beginPath();
        pulseCtx.moveTo(prevPoint.x, prevPoint.y);
        pulseCtx.lineTo(point.x, point.y);
        pulseCtx.globalAlpha = Math.sin((d / SNAKE_LENGTH) * Math.PI);
        pulseCtx.stroke();
      }
      prevPoint = point;
    }
  }

  function pulseLoop(timestamp) {
    if (!isPulseVisible()) {
      pulseRunning = false;
      return;
    }

    if (!lastPulseTime) lastPulseTime = timestamp;
    var dt = timestamp - lastPulseTime;
    lastPulseTime = timestamp;

    timeUntilNextSpawn -= dt;
    if (timeUntilNextSpawn <= 0) {
      spawnSnake();
    }

    pulseCtx.clearRect(0, 0, pulseCanvas.width, pulseCanvas.height);

    for (var i = activeSnakes.length - 1; i >= 0; i--) {
      var snake = activeSnakes[i];
      snake.currentDist += (SNAKE_SPEED * dt) / 1000;

      if (snake.currentDist - SNAKE_LENGTH > snake.totalLen) {
        activeSnakes.splice(i, 1);
        continue;
      }
      drawSnake(snake);
    }

    requestAnimationFrame(pulseLoop);
  }

  function startPulseIfNeeded() {
    if (pulseCtx && !pulseRunning && isPulseVisible()) {
      pulseRunning = true;
      lastPulseTime = 0;
      requestAnimationFrame(pulseLoop);
    }
  }

  /* --- Drag logic --- */

  physicsBoxes.forEach(function (b) {
    b.el.addEventListener("pointerdown", function (e) {
      if (e.target.closest(".ecosystem-icon")) return;

      b.isDragging = true;
      isDraggingGlobal = true;
      dragDistance = 0;
      b.startMouse = { x: e.clientX - b.pos.x, y: e.clientY - b.pos.y };
      b.el.style.zIndex = "100";
      b.el.setPointerCapture(e.pointerId);
      if (!animationFrameId) renderLoop();
    });

    b.el.addEventListener("pointermove", function (e) {
      if (!b.isDragging) return;
      var currentX = e.clientX - b.startMouse.x;
      var currentY = e.clientY - b.startMouse.y;
      dragDistance = Math.sqrt(
        Math.pow(currentX - b.pos.x, 2) + Math.pow(currentY - b.pos.y, 2)
      );
      b.pos.x = currentX;
      b.pos.y = currentY;
    });

    b.el.addEventListener("pointerup", function (e) {
      if (!b.isDragging) return;
      b.isDragging = false;
      b.el.style.zIndex = "2";
      b.el.releasePointerCapture(e.pointerId);
      setTimeout(function () {
        isDraggingGlobal = false;
        dragDistance = 0;
      }, 50);
    });
  });

  /* --- Icon selection (radio within group) --- */

  diagram.querySelectorAll(".ecosystem-icon").forEach(function (icon) {
    icon.addEventListener("pointerup", function (e) {
      if (isDraggingGlobal || dragDistance > 5) return;
      e.stopPropagation();

      var grid = icon.closest(".ecosystem-icon-grid");
      var groupId = grid.getAttribute("data-group");
      var wasSelected = icon.classList.contains("selected");

      diagram
        .querySelectorAll('.ecosystem-icon-grid[data-group="' + groupId + '"] .ecosystem-icon')
        .forEach(function (sibling) {
          sibling.classList.remove("selected");
        });

      if (!wasSelected) {
        icon.classList.add("selected");
      }

    });
  });

  /* --- Render loop (spring physics) --- */

  function renderLoop() {
    var needsFrame = false;

    physicsBoxes.forEach(function (b) {
      if (!b.isDragging) {
        var forceX = -b.pos.x * STIFFNESS;
        var forceY = -b.pos.y * STIFFNESS;
        b.vel.x = (b.vel.x + forceX) * DAMPING;
        b.vel.y = (b.vel.y + forceY) * DAMPING;
        b.pos.x += b.vel.x;
        b.pos.y += b.vel.y;

        if (Math.abs(b.vel.x) > 0.05 || Math.abs(b.pos.x) > 0.05) {
          needsFrame = true;
        } else {
          b.pos.x = 0;
          b.pos.y = 0;
          b.vel.x = 0;
          b.vel.y = 0;
        }
      } else {
        needsFrame = true;
      }
      b.el.style.transform = "translate(" + b.pos.x + "px, " + b.pos.y + "px)";
    });

    updateLines();

    if (needsFrame) {
      animationFrameId = requestAnimationFrame(renderLoop);
    } else {
      animationFrameId = null;
    }
  }

  /* --- Init --- */

  window.addEventListener("resize", function () {
    updateLines();
    resizePulseCanvas();
    startPulseIfNeeded();
  });

  setTimeout(function () {
    updateLines();
    resizePulseCanvas();
    startPulseIfNeeded();
  }, 100);
})();
