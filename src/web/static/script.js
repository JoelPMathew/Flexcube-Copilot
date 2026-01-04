document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const inputText = document.getElementById('inputText');
    const analyzeBtn = document.getElementById('analyzeBtn');

    const impactBtn = document.getElementById('impactBtn');
    const codeBtn = document.getElementById('codeBtn');

    const reqOutput = document.getElementById('reqOutput');
    const impactOutput = document.getElementById('impactOutput');
    const codeOutput = document.getElementById('codeOutput');

    const reqStatus = document.getElementById('reqStatus');
    const impactStatus = document.getElementById('impactStatus');
    const codeStatus = document.getElementById('codeStatus');

    // State
    let currentRequirements = null;
    let currentImpact = null;

    // 1. Analyze Requirements
    analyzeBtn.addEventListener('click', async () => {
        const text = inputText.value.trim();
        if (!text) return;

        // Reset UI downstream
        reqStatus.textContent = 'Analyzing...';
        reqOutput.textContent = 'Processing...';
        impactOutput.textContent = 'Waiting for requirements...';
        impactBtn.disabled = true;
        codeOutput.innerHTML = '<div class="code-placeholder">Code will appear here...</div>';
        codeBtn.disabled = true;

        currentRequirements = null;
        currentImpact = null;

        try {
            const response = await fetch('/api/analyze/requirements', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });

            if (!response.ok) throw new Error('Analysis failed');

            const data = await response.json();
            currentRequirements = data;

            reqOutput.textContent = JSON.stringify(data, null, 2);
            reqStatus.textContent = '✓ Done';

            // Enable next step
            impactBtn.disabled = false;
        } catch (error) {
            reqOutput.textContent = 'Error: ' + error.message;
            reqStatus.textContent = '⚠ Failed';
        }
    });

    // 2. Assess Impact
    impactBtn.addEventListener('click', async () => {
        if (!currentRequirements) return;

        impactStatus.textContent = 'Assessing...';
        impactOutput.textContent = 'Processing...';
        codeBtn.disabled = true; // disable next step until this finishes
        currentImpact = null;

        try {
            const response = await fetch('/api/analyze/impact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(currentRequirements)
            });

            if (!response.ok) throw new Error('Impact analysis failed');

            const data = await response.json();
            currentImpact = data;

            impactOutput.textContent = JSON.stringify(data, null, 2);
            impactStatus.textContent = '✓ Done';

            // Enable next step
            codeBtn.disabled = false;
        } catch (error) {
            impactOutput.textContent = 'Error: ' + error.message;
            impactStatus.textContent = '⚠ Failed';
        }
    });

    // 3. Generate Code
    codeBtn.addEventListener('click', async () => {
        if (!currentImpact) return;

        codeStatus.textContent = 'Generating...';
        codeOutput.innerHTML = '<div class="code-placeholder">Generating Code...</div>';

        try {
            const response = await fetch('/api/generate/code', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(currentImpact)
            });

            if (!response.ok) throw new Error('Code generation failed');

            const data = await response.json();

            // Render Files
            codeOutput.innerHTML = ''; // Clear placeholder
            if (data.files && data.files.length > 0) {
                data.files.forEach(file => {
                    const fileBlock = document.createElement('div');
                    fileBlock.className = 'code-file';

                    const header = document.createElement('div');
                    header.className = 'file-header';
                    header.textContent = `${file.file_name} (${file.file_type})`;

                    const contentP = document.createElement('div');
                    contentP.className = 'file-content';
                    contentP.textContent = file.file_content;

                    fileBlock.appendChild(header);
                    fileBlock.appendChild(contentP);
                    codeOutput.appendChild(fileBlock);
                });
            } else {
                codeOutput.innerHTML = `<div class="file-content">${data.summary || "No code generated."}</div>`;
            }

            codeStatus.textContent = '✓ Done';
        } catch (error) {
            codeOutput.innerHTML = `<div class="file-content" style="color: #ef4444">Error: ${error.message}</div>`;
            codeStatus.textContent = '⚠ Failed';
        }
    });
});
