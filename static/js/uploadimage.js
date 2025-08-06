// upload.js
document.addEventListener('DOMContentLoaded', function() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');
    const fileInfo = document.getElementById('fileInfo');
    const imageGrid = document.getElementById('imageGrid');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analysisResults = document.getElementById('analysisResults');
    
    let uploadedFiles = [];
    
    // Browse files button click
    browseBtn.addEventListener('click', function() {
        fileInput.click();
    });
    
    // File input change
    fileInput.addEventListener('change', function(e) {
        handleFiles(e.target.files);
    });
    
    // Drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropzone.classList.add('active');
    }
    
    function unhighlight() {
        dropzone.classList.remove('active');
    }
    
    dropzone.addEventListener('drop', function(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    });
    
    // Handle uploaded files
    function handleFiles(files) {
        uploadedFiles = [...uploadedFiles, ...files];
        updateFileInfo();
        displayImages();
        analyzeBtn.disabled = uploadedFiles.length === 0;
    }
    
    // Update file information display
    function updateFileInfo() {
        if (uploadedFiles.length === 0) {
            fileInfo.textContent = '';
            return;
        }
        
        const fileCount = uploadedFiles.length;
        const totalSize = uploadedFiles.reduce((total, file) => total + file.size, 0);
        const sizeInMB = (totalSize / (1024 * 1024)).toFixed(2);
        
        fileInfo.innerHTML = `
            <p>${fileCount} file(s) selected</p>
            <p>Total size: ${sizeInMB} MB</p>
        `;
    }
    
    // Display uploaded images
    function displayImages() {
        imageGrid.innerHTML = '';
        
        uploadedFiles.forEach((file, index) => {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                const imagePreview = document.createElement('div');
                imagePreview.className = 'image-preview';
                
                imagePreview.innerHTML = `
                    <img src="${e.target.result}" alt="Uploaded image ${index + 1}">
                    <button class="remove-btn" data-index="${index}">&times;</button>
                `;
                
                imageGrid.appendChild(imagePreview);
                
                // Add remove button event
                const removeBtn = imagePreview.querySelector('.remove-btn');
                removeBtn.addEventListener('click', function() {
                    removeImage(index);
                });
            };
            
            reader.readAsDataURL(file);
        });
    }
    
    // Remove image from upload list
    function removeImage(index) {
        uploadedFiles.splice(index, 1);
        updateFileInfo();
        displayImages();
        analyzeBtn.disabled = uploadedFiles.length === 0;
    }
    
    // Analyze button click
    analyzeBtn.addEventListener('click', function() {
        if (uploadedFiles.length === 0) return;
        
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        
        // Simulate analysis (in a real app, you would send to server)
        setTimeout(function() {
            showAnalysisResults();
        }, 2000);
    });
    
    // Show analysis results
    function showAnalysisResults() {
        analysisResults.style.display = 'block';
        analysisResults.innerHTML = `
            <h3>Analysis Results</h3>
            <div class="result-item">
                <h4>Scalp Condition Detected:</h4>
                <p>Mild dryness with slight oiliness in T-zone</p>
            </div>
            <div class="result-item">
                <h4>Recommendations:</h4>
                <ul>
                    <li>Use our Hydrating Scalp Serum 3 times per week</li>
                    <li>Try our Balancing Shampoo for oily roots</li>
                    <li>Schedule a consultation for personalized advice</li>
                </ul>
            </div>
            <button class="browse-btn" id="newAnalysisBtn">Start New Analysis</button>
        `;
        
        analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analysis Complete';
        
        // New analysis button
        document.getElementById('newAnalysisBtn').addEventListener('click', function() {
            resetAnalysis();
        });
    }
    
    // Reset analysis
    function resetAnalysis() {
        uploadedFiles = [];
        updateFileInfo();
        imageGrid.innerHTML = '';
        analysisResults.style.display = 'none';
        analysisResults.innerHTML = '';
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analyze My Scalp';
    }
});