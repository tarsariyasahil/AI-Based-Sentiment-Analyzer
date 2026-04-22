(function () {
    "use strict";

    const $ = (sel) => document.querySelector(sel);
    const dropZone = $("#dropZone");
    const fileInput = $("#fileInput");
    const uploadZoneContent = $("#uploadZoneContent");
    const uploadActions = $("#uploadActions");
    const fileName = $("#fileName");
    const removeBtn = $("#removeFile");
    const analyzeBtn = $("#analyzeBtn");
    const uploadSection = $("#uploadSection");
    const loadingSection = $("#loadingSection");
    const resultsSection = $("#resultsSection");
    const errorSection = $("#errorSection");
    const previewImage = $("#previewImage");
    const predictionsList = $("#predictionsList");
    const errorMessage = $("#errorMessage");
    const retryBtn = $("#retryBtn");
    const newUploadBtn = $("#newUploadBtn");
    const loadingBarFill = $("#loadingBarFill");

    let selectedFile = null;

    /* ---- Helpers ---- */
    function showSection(section) {
        [uploadSection, loadingSection, resultsSection, errorSection].forEach((s) => (s.style.display = "none"));
        section.style.display = "";
        section.classList.remove("fade-in-up");
        void section.offsetWidth;
        section.classList.add("fade-in-up");
    }

    function resetUpload() {
        selectedFile = null;
        fileInput.value = "";
        uploadActions.style.display = "none";
        uploadZoneContent.style.display = "";
        dropZone.style.display = "";
        loadingBarFill.style.animation = "none";
        void loadingBarFill.offsetWidth;
        loadingBarFill.style.animation = "";
    }

    /* ---- File Selection ---- */
    function handleFile(file) {
        if (!file) return;
        const allowed = ["png", "jpg", "jpeg", "bmp", "webp"];
        const ext = file.name.split(".").pop().toLowerCase();
        if (!allowed.includes(ext)) {
            alert("Invalid file type. Allowed: PNG, JPG, JPEG, BMP, WEBP");
            return;
        }
        selectedFile = file;
        fileName.textContent = file.name;
        uploadZoneContent.style.display = "none";
        dropZone.style.display = "none";
        uploadActions.style.display = "flex";
    }

    dropZone.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length) handleFile(e.target.files[0]);
    });

    removeBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        resetUpload();
    });

    /* ---- Drag & Drop ---- */
    ["dragenter", "dragover"].forEach((ev) => {
        dropZone.addEventListener(ev, (e) => {
            e.preventDefault();
            dropZone.classList.add("drag-over");
        });
    });

    ["dragleave", "drop"].forEach((ev) => {
        dropZone.addEventListener(ev, (e) => {
            e.preventDefault();
            dropZone.classList.remove("drag-over");
        });
    });

    dropZone.addEventListener("drop", (e) => {
        const files = e.dataTransfer.files;
        if (files.length) handleFile(files[0]);
    });

    /* ---- Analyze ---- */
    analyzeBtn.addEventListener("click", () => {
        if (!selectedFile) return;
        showSection(loadingSection);

        const formData = new FormData();
        formData.append("image", selectedFile);

        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
        };
        reader.readAsDataURL(selectedFile);

        fetch("/predict", { method: "POST", body: formData })
            .then((res) => res.json())
            .then((data) => {
                if (data.error) {
                    errorMessage.textContent = data.error;
                    showSection(errorSection);
                    return;
                }
                renderPredictions(data.predictions);
                showSection(resultsSection);
            })
            .catch((err) => {
                errorMessage.textContent = "Network error. Please try again.";
                showSection(errorSection);
            });
    });

    /* ---- Render Predictions ---- */
    function renderPredictions(predictions) {
        predictionsList.innerHTML = "";
        const maxConf = predictions.length ? predictions[0].confidence : 100;

        predictions.forEach((pred, i) => {
            const item = document.createElement("div");
            item.className = "prediction-item" + (i === 0 ? " top-prediction" : "");

            const barWidth = Math.max(2, (pred.confidence / maxConf) * 100);

            item.innerHTML = `
                <div class="prediction-rank">${i + 1}</div>
                <div class="prediction-info">
                    <div class="prediction-name">${pred.description}</div>
                    <div class="prediction-bar-track">
                        <div class="prediction-bar-fill" data-width="${barWidth}"></div>
                    </div>
                </div>
                <div class="prediction-confidence">${pred.confidence}%</div>
            `;
            predictionsList.appendChild(item);
        });

        requestAnimationFrame(() => {
            document.querySelectorAll(".prediction-bar-fill").forEach((bar) => {
                bar.style.width = bar.dataset.width + "%";
            });
        });
    }

    /* ---- Retry / New Upload ---- */
    retryBtn.addEventListener("click", () => {
        resetUpload();
        showSection(uploadSection);
    });

    newUploadBtn.addEventListener("click", () => {
        resetUpload();
        showSection(uploadSection);
    });
})();
