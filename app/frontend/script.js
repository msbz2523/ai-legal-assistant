// script.js – Modern UI mit Blur, Animationen & Interaktionen
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file');
const form = document.getElementById('uploadForm');
const resultDiv = document.getElementById('result');
const originalText = document.getElementById('original_text');
const summaryText = document.getElementById('summary');
const legalAdvice = document.getElementById('legal_recommendation');
const progressBar = document.getElementById('progress-bar');
const progress = document.getElementById('progress');

// Animiertes Drop-Zone Highlighting
['dragenter', 'dragover'].forEach(event => {
    dropZone.addEventListener(event, e => {
        e.preventDefault();
        dropZone.classList.add('dragover');
        dropZone.innerHTML = '📂 Datei hier ablegen';
    });
});

['dragleave', 'drop'].forEach(event => {
    dropZone.addEventListener(event, e => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        dropZone.innerHTML = '📁 Datei hierher ziehen oder klicken';
    });
});

dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('drop', (e) => {
    fileInput.files = e.dataTransfer.files;
});

// Hochladen mit Fortschritt + animierter Vorschau
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!fileInput.files.length) return Swal.fire('📎 Fehler', 'Bitte Datei hochladen.', 'error');

    const formData = new FormData(form);
    const xhr = new XMLHttpRequest();

    xhr.open('POST', 'http://127.0.0.1:8000/api/extract-summarize');

    xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
            const percent = Math.round((e.loaded / e.total) * 100);
            progress.style.display = 'block';
            progressBar.style.width = percent + '%';
            progressBar.textContent = percent + '%';
        }
    });

    xhr.onload = () => {
        if (xhr.status === 200) {
            try {
                const data = JSON.parse(xhr.responseText);
                originalText.textContent = data.original_text || 'Kein Text extrahiert.';
                summaryText.textContent = data.summary || 'Keine Zusammenfassung vorhanden.';
                legalAdvice.textContent = data.legal_recommendation || '';
                resultDiv.style.display = 'block';
                resultDiv.classList.add('fade-in');
                Swal.fire({ icon: 'success', title: 'Fertig!', text: 'Datei erfolgreich verarbeitet.' });
            } catch (err) {
                Swal.fire('❌ Fehler', 'Antwort konnte nicht gelesen werden.', 'error');
            }
        } else {
            Swal.fire('🚫 Fehler', 'Serverfehler: ' + xhr.status, 'error');
        }
        progress.style.display = 'none';
    };

    xhr.onerror = () => {
        Swal.fire('💥 Fehler', 'Anfrage fehlgeschlagen.', 'error');
        progress.style.display = 'none';
    };

    xhr.send(formData);
});

// Optional: Dark mode toggle
// 🌓 Dark Mode Toggle mit Animation
const toggle = document.createElement('button');
toggle.textContent = '🌓 Dark Mode';
toggle.style.position = 'absolute';
toggle.style.top = '10px';
toggle.style.right = '20px';
toggle.style.padding = '10px';
toggle.style.borderRadius = '8px';
toggle.className = 'dark-mode-toggle';
toggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    toggle.classList.toggle('active');
});
document.body.appendChild(toggle);