document.addEventListener("DOMContentLoaded", () => {
    // Get the canvas
    const canvas = document.getElementById("paint-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    // Set the canvas size
    canvas.width = 800;
    canvas.height = 600;

    // Create an offscreen canvas for user drawing
    const drawingCanvas = document.createElement("canvas");
    drawingCanvas.width = 800;
    drawingCanvas.height = 600;
    const drawingCtx = drawingCanvas.getContext("2d");

    // Template image setup
    const templateImg = new Image();
    templateImg.crossOrigin = "Anonymous";

    // Store active template palette for intelligent blending
    let currentTemplatePalette = [];

    // Clear the drawing
    function resetDrawing() {
        drawingCtx.clearRect(0, 0, drawingCanvas.width, drawingCanvas.height);
        updateCanvas();
    }

    // Show the drawing and template together
    function updateCanvas() {
        // Fill white background
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Draw user strokes
        ctx.drawImage(drawingCanvas, 0, 0);

        // Draw template outlines on top
        if (templateImg.complete && templateImg.src && templateImg.naturalWidth !== 0) {
            ctx.save();
            ctx.globalCompositeOperation = "multiply";
            ctx.drawImage(templateImg, 0, 0, canvas.width, canvas.height);
            ctx.restore();
        }
    }

    templateImg.onload = () => {
        updateCanvas();
    };

    // Load default template
    const templatePath = typeof ASSET_PATH !== "undefined" ? ASSET_PATH : "/static/templates/";
    templateImg.src = `${templatePath}car.png`;
    fetchPalette("car.png");

    // Get webcam and air cursor elements
    const video = document.getElementById("webcam");
    const camBtn = document.getElementById("camera-btn");
    const camPlaceholder = document.getElementById("cam-placeholder");
    const airCursor = document.getElementById("airCursor");
    const airCursorProgress = document.getElementById("airCursorProgress");
    const gestureStatus = document.getElementById("gestureStatus");
    const airDwellTimer = document.getElementById("airDwellTimer");
    const pillGallery = document.getElementById("pill-gallery");
    const imageUploader = document.getElementById("imageUploader");

    // Get tool buttons
    const toolBrush = document.getElementById("tool-brush");
    const toolEraser = document.getElementById("tool-eraser");
    const btnClear = document.getElementById("btn-clear");
    const btnSizeDown = document.getElementById("btn-size-down");
    const btnSizeUp = document.getElementById("btn-size-up");
    const brushSizeVal = document.getElementById("brushSizeVal");

    // Get color containers
    const presetSwatches = document.querySelectorAll(".color-swatch");
    const customColorPicker = document.getElementById("customColorPicker");
    const aiPaletteSection = document.getElementById("ai-palette-section");
    const aiSwatchesContainer = document.getElementById("ai-swatches-container");
    const knnSwatchesContainer = document.getElementById("knn-swatches-container");

    // Set default drawing values
    let currentMode = "brush";
    let currentColor = "#ef4444";
    let brushSize = 14;

    let isMouseDown = false;
    let lastMouseX = null, lastMouseY = null;

    // Smooth air cursor coordinates and filtering state
    let smoothX = null, smoothY = null;
    let lastAirX = null, lastAirY = null;

    // Pinch hysteresis state
    let isCurrentlyPinching = false;
    const PINCH_START_THRESHOLD = 58; // Forgiving threshold for kids
    const PINCH_RELEASE_THRESHOLD = 68; // Hysteresis buffer to prevent rapid flickering
    const SMOOTHING_FACTOR = 0.18;      // Strong exponential smoothing
    const JITTER_THRESHOLD = 2.5;       // Minimum movement deadband in pixels

    let isCameraActive = false;
    let cameraUtils = null;
    let mpHands = null;

    // Time required to click using air cursor
    let hoverTarget = null;
    let hoverStartTime = 0;
    const DWELL_DURATION = 800;

    // Select drawing tool
    function setToolMode(mode) {
        currentMode = mode;
        [toolBrush, toolEraser].forEach(button => {
            if (!button) return;
            button.classList.remove("bg-indigo-600", "text-white");
            button.classList.add("bg-slate-800", "text-slate-300");
        });

        if (mode === "brush" && toolBrush) toolBrush.classList.add("bg-indigo-600", "text-white");
        if (mode === "eraser" && toolEraser) toolEraser.classList.add("bg-indigo-600", "text-white");
    }

    if (toolBrush) toolBrush.addEventListener("click", () => setToolMode("brush"));
    if (toolEraser) toolEraser.addEventListener("click", () => setToolMode("eraser"));
    if (btnClear) btnClear.addEventListener("click", resetDrawing);

    // Decrease brush size
    if (btnSizeDown) {
        btnSizeDown.addEventListener("click", () => {
            brushSize = Math.max(2, brushSize - 3);
            if (brushSizeVal) brushSizeVal.textContent = `${brushSize}px`;
        });
    }

    // Increase brush size
    if (btnSizeUp) {
        btnSizeUp.addEventListener("click", () => {
            brushSize = Math.min(50, brushSize + 3);
            if (brushSizeVal) brushSizeVal.textContent = `${brushSize}px`;
        });
    }

    // Change the brush color
    function selectColor(hex) {
        currentColor = hex;
        if (customColorPicker) customColorPicker.value = hex;
        if (currentMode === "eraser") setToolMode("brush");
        fetchKNNRecommendations(hex);
    }

    // Preset color buttons
    presetSwatches.forEach(swatch => {
        swatch.addEventListener("click", () => {
            presetSwatches.forEach(s => s.classList.remove("active-swatch", "border-white"));
            swatch.classList.add("active-swatch", "border-white");
            selectColor(swatch.getAttribute("data-color"));
        });
    });

    // Custom color picker input
    if (customColorPicker) {
        customColorPicker.addEventListener("input", (event) => selectColor(event.target.value));
    }

    // Upload custom image
    if (imageUploader) {
        imageUploader.addEventListener("change", (event) => {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    templateImg.src = event.target.result;
                    resetDrawing();
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Draw lines on canvas
    function drawLine(x1, y1, x2, y2) {
        drawingCtx.beginPath();
        drawingCtx.moveTo(x1, y1);
        drawingCtx.lineTo(x2, y2);
        drawingCtx.lineCap = "round";
        drawingCtx.lineJoin = "round";

        if (currentMode === "eraser") {
            drawingCtx.globalCompositeOperation = "destination-out";
            drawingCtx.lineWidth = brushSize * 2.5;
        } else {
            drawingCtx.globalCompositeOperation = "source-over";
            drawingCtx.strokeStyle = currentColor;
            drawingCtx.lineWidth = brushSize;
        }
        drawingCtx.stroke();
        updateCanvas();
    }

    // Mouse drawing controls
    canvas.addEventListener("mousedown", (event) => {
        const rect = canvas.getBoundingClientRect();
        const x = (event.clientX - rect.left) * (canvas.width / rect.width);
        const y = (event.clientY - rect.top) * (canvas.height / rect.height);

        isMouseDown = true;
        lastMouseX = x;
        lastMouseY = y;
        drawLine(x, y, x, y);
    });

    canvas.addEventListener("mousemove", (event) => {
        if (!isMouseDown) return;
        const rect = canvas.getBoundingClientRect();
        const x = (event.clientX - rect.left) * (canvas.width / rect.width);
        const y = (event.clientY - rect.top) * (canvas.height / rect.height);
        drawLine(lastMouseX, lastMouseY, x, y);
        lastMouseX = x;
        lastMouseY = y;
    });

    canvas.addEventListener("mouseup", () => { isMouseDown = false; lastMouseX = null; lastMouseY = null; });
    canvas.addEventListener("mouseleave", () => { isMouseDown = false; lastMouseX = null; lastMouseY = null; });

    // Toggle camera button
    if (camBtn) {
        camBtn.addEventListener("click", () => {
            if (!isCameraActive) initHandTracking();
            else stopHandTracking();
        });
    }

    // Start the camera and hand tracking
    function initHandTracking() {
        if (!window.Hands) {
            alert("MediaPipe Hands library is loading, please try again in 5 seconds!");
            return;
        }

        mpHands = new window.Hands({
            locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
        });

        mpHands.setOptions({
            maxNumHands: 1,
            modelComplexity: 1,
            minDetectionConfidence: 0.7,
            minTrackingConfidence: 0.7
        });

        mpHands.onResults(onHandResults);

        if (window.Camera) {
            cameraUtils = new window.Camera(video, {
                onFrame: async () => {
                    if (isCameraActive && video) await mpHands.send({ image: video });
                },
                width: 640,
                height: 480
            });

            cameraUtils.start().then(() => {
                isCameraActive = true;
                if (camPlaceholder) camPlaceholder.style.display = "none";
                if (camBtn) camBtn.textContent = " Stop Camera";
                if (gestureStatus) gestureStatus.textContent = "Gesture: Touchless Active!";
            });
        }
    }

    // Stop the camera
    function stopHandTracking() {
        isCameraActive = false;
        if (cameraUtils) cameraUtils.stop();
        if (video.srcObject) {
            video.srcObject.getTracks().forEach(track => track.stop());
            video.srcObject = null;
        }
        if (camPlaceholder) camPlaceholder.style.display = "block";
        if (camBtn) camBtn.textContent = " Start Camera";
        if (airCursor) airCursor.style.display = "none";
        if (gestureStatus) gestureStatus.textContent = "Gesture: Camera Stopped";
        isCurrentlyPinching = false;
        resetDwell();
    }

    // Reset dwell click timer
    function resetDwell() {
        hoverTarget = null;
        hoverStartTime = 0;
        if (airCursorProgress) airCursorProgress.style.transform = "scale(0)";
        if (airDwellTimer) airDwellTimer.textContent = "DWELL: OFF";
    }

    // Click the button after hovering for some time
    function processAirHoverDwell(screenX, screenY) {
        const element = document.elementFromPoint(screenX, screenY);
        const targetBtn = element ? element.closest(".air-target") : null;

        if (targetBtn) {
            if (hoverTarget !== targetBtn) {
                hoverTarget = targetBtn;
                hoverStartTime = Date.now();
            }

            const elapsed = Date.now() - hoverStartTime;
            const progress = Math.min(1, elapsed / DWELL_DURATION);

            if (airCursorProgress) airCursorProgress.style.transform = `scale(${progress})`;
            if (airDwellTimer) airDwellTimer.textContent = `DWELL: ${Math.round(progress * 100)}%`;

            if (elapsed >= DWELL_DURATION) {
                targetBtn.click();
                resetDwell();
            }
        } else {
            resetDwell();
        }
    }

    // Check the detected hand with improved tracking & kid-friendly controls
    function onHandResults(results) {
        if (!isCameraActive) {
            if (airCursor) airCursor.style.display = "none";
            return;
        }

        // Check if hand is detected
        if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
            const landmarks = results.multiHandLandmarks[0];
            const indexTip = landmarks[8];
            const thumbTip = landmarks[4];

            // Gradual screen mapping with slight margin to reduce edge sensitivity
            const rawX = (1 - indexTip.x) * window.innerWidth;
            const rawY = indexTip.y * window.innerHeight;

            // Initialize or apply exponential smoothing
            if (smoothX === null || smoothY === null) {
                smoothX = rawX;
                smoothY = rawY;
            } else {
                const distToNew = Math.hypot(rawX - smoothX, rawY - smoothY);
                // Deadband filter: ignore microscopic jitter
                if (distToNew > JITTER_THRESHOLD) {
                    smoothX += (rawX - smoothX) * SMOOTHING_FACTOR;
                    smoothY += (rawY - smoothY) * SMOOTHING_FACTOR;
                }
            }

            // Calculate distance between index and thumb tip
            const distance = Math.hypot(
                ((1 - indexTip.x) - (1 - thumbTip.x)) * window.innerWidth,
                (indexTip.y - thumbTip.y) * window.innerHeight
            );

            // Pinch detection with hysteresis buffer
            if (!isCurrentlyPinching && distance < PINCH_START_THRESHOLD) {
                isCurrentlyPinching = true;
            } else if (isCurrentlyPinching && distance > PINCH_RELEASE_THRESHOLD) {
                isCurrentlyPinching = false;
            }

            // Update the air cursor position
            if (airCursor) {
                airCursor.style.display = "block";
                airCursor.style.left = `${smoothX}px`;
                airCursor.style.top = `${smoothY}px`;
                airCursor.style.borderColor = isCurrentlyPinching ? "#ef4444" : "#38bdf8";
            }

            const canvasRect = canvas.getBoundingClientRect();
            const insideCanvas = (
                smoothX >= canvasRect.left &&
                smoothX <= canvasRect.right &&
                smoothY >= canvasRect.top &&
                smoothY <= canvasRect.bottom
            );

            // Draw only when the cursor is inside the canvas
            if (insideCanvas) {
                resetDwell();
                const canvasX = (smoothX - canvasRect.left) * (canvas.width / canvasRect.width);
                const canvasY = (smoothY - canvasRect.top) * (canvas.height / canvasRect.height);

                if (gestureStatus) {
                    gestureStatus.textContent = isCurrentlyPinching ? "Gesture: DRAWING" : "Gesture: HOVER";
                }

                if (isCurrentlyPinching) {
                    if (lastAirX !== null && lastAirY !== null) {
                        drawLine(lastAirX, lastAirY, canvasX, canvasY);
                    } else {
                        drawLine(canvasX, canvasY, canvasX, canvasY);
                    }
                    lastAirX = canvasX;
                    lastAirY = canvasY;
                } else {
                    lastAirX = null;
                    lastAirY = null;
                }
            } else {
                lastAirX = null;
                lastAirY = null;
                if (gestureStatus) gestureStatus.textContent = "Gesture: MENU TARGETING";
                processAirHoverDwell(smoothX, smoothY);
            }

        } else {
            if (airCursor) airCursor.style.display = "none";
            if (gestureStatus) gestureStatus.textContent = "Gesture: No Hand Detected";
            smoothX = null;
            smoothY = null;
            lastAirX = null;
            lastAirY = null;
            isCurrentlyPinching = false;
            resetDwell();
        }
    }

    // Switch image templates from gallery
    if (pillGallery) {
        const pills = pillGallery.querySelectorAll(".template-pill");
        pills.forEach((pill) => {
            pill.addEventListener("click", () => {
                pills.forEach(p => p.classList.remove("active", "border-indigo-500"));
                pill.classList.add("active", "border-indigo-500");

                const src = pill.getAttribute("data-src");
                const targetSrc = `${templatePath}${src}`;

                drawingCtx.clearRect(0, 0, drawingCanvas.width, drawingCanvas.height);

                templateImg.src = targetSrc;
                fetchPalette(src);
            });
        });
    }

    // Get AI color palette for template
    function fetchPalette(templateSrc) {
        const filename = templateSrc.split('/').pop();
        const payloadPath = typeof ASSET_PATH !== "undefined" ? `${ASSET_PATH}${filename}` : templateSrc;
        
        fetch("/api/get-palette", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ template_path: payloadPath })
        })
        .then(res => res.json())
        .then(data => {
            const colors = data.palette || data.colors;
            if (colors && colors.length > 0) {
                currentTemplatePalette = colors;
                renderAIPaletteSwatches(colors);
            } else {
                currentTemplatePalette = [];
            }
            // Always fetch recommendations, even if palette extraction had no colors
            fetchKNNRecommendations(currentColor);
        })
        .catch(error => {
            console.error("Error fetching palette:", error);
            // Fallback: Still fetch KNN recommendations if template palette fails
            fetchKNNRecommendations(currentColor);
        });
    }

    // Helper: Calculate distance between two Hex colors in RGB space
    function hexToRgb(hex) {
        const h = hex.replace("#", "");
        return [
            parseInt(h.substring(0, 2), 16) || 0,
            parseInt(h.substring(2, 4), 16) || 0,
            parseInt(h.substring(4, 6), 16) || 0
        ];
    }

    function colorDistance(hex1, hex2) {
        const rgb1 = hexToRgb(hex1);
        const rgb2 = hexToRgb(hex2);
        return Math.hypot(rgb1[0] - rgb2[0], rgb1[1] - rgb2[1], rgb1[2] - rgb2[2]);
    }

    // Get AI color recommendations
    function fetchKNNRecommendations(hexColor) {

    fetch("/api/recommend-colors", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            color: hexColor
        })
    })
    .then(response => response.json())
    .then(data => {

        if (!data.recommendations)
            return;

        renderKNNRecommendations(data.recommendations);

    })
    .catch(error => {
        console.error(error);
    });

}

    // Show the AI color palette
    function renderAIPaletteSwatches(colors) {
        if (!aiSwatchesContainer || !aiPaletteSection) return;
        aiPaletteSection.classList.remove("hidden");
        aiSwatchesContainer.innerHTML = "";

        colors.forEach((hexColor) => {
            const swatch = document.createElement("button");
            swatch.type = "button";
            swatch.className = "air-target w-8 h-8 rounded-full border-2 border-white/30 shadow-md transition-transform hover:scale-110 focus:outline-none";
            swatch.style.backgroundColor = hexColor;

            swatch.addEventListener("click", () => {
                selectColor(hexColor);
                aiSwatchesContainer.querySelectorAll("button").forEach(button => button.style.borderColor = "rgba(255, 255, 255, 0.3)");
                swatch.style.borderColor = "#ffffff";
            });

            aiSwatchesContainer.appendChild(swatch);
        });
    }

    // Display intelligent "Suggested Colours" with top choice highlighted
    function renderKNNRecommendations(colors) {
        if (!knnSwatchesContainer || !aiPaletteSection) return;
        aiPaletteSection.classList.remove("hidden");
        knnSwatchesContainer.innerHTML = "";

        // Add contextual section header if missing
        let titleEl = document.getElementById("knn-title");
        if (!titleEl && knnSwatchesContainer.parentElement) {
            titleEl = document.createElement("p");
            titleEl.id = "knn-title";
            titleEl.className = "text-xs font-semibold text-indigo-300 uppercase tracking-wider mb-2 mt-3";
            titleEl.textContent = "Suggested Colours";
            knnSwatchesContainer.parentElement.insertBefore(titleEl, knnSwatchesContainer);
        }

        colors.forEach((hexColor, index) => {
            const swatch = document.createElement("button");
            swatch.type = "button";
            
            // Highlight top recommendation prominently
            if (index === 0) {
                swatch.className = "air-target relative w-9 h-9 rounded-full border-2 border-amber-300 shadow-lg ring-2 ring-amber-400/50 transition-transform hover:scale-110 focus:outline-none flex items-center justify-center";
                swatch.title = "Top AI Suggestion";
                swatch.innerHTML = `<span class="text-white text-xs drop-shadow-[0_1px_1px_rgba(0,0,0,0.8)] font-bold">★</span>`;
            } else {
                swatch.className = "air-target w-8 h-8 rounded-full border-2 border-indigo-400/50 shadow-md transition-transform hover:scale-110 focus:outline-none";
            }
            
            swatch.style.backgroundColor = hexColor;

            swatch.addEventListener("click", () => {
                selectColor(hexColor);
                knnSwatchesContainer.querySelectorAll("button").forEach(button => button.style.borderColor = "rgba(129, 140, 248, 0.5)");
                swatch.style.borderColor = "#ffffff";
            });

            knnSwatchesContainer.appendChild(swatch);
        });
    }

    // Show recommended colors when the page loads
    fetchKNNRecommendations(currentColor);
});