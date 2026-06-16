document.getElementById('check-btn').onclick = async () => {
    const path = document.getElementById('file-path').value;
    const card = document.getElementById('status-card');
    const title = document.getElementById('status-title');
    const msg = document.getElementById('status-message');
    const currentHash = document.getElementById('current-hash');
    const alertDetails = document.getElementById('alert-details');
    const oldHash = document.getElementById('old-hash');

    if (!path) return;

    try {
        const response = await fetch('/monitor', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path })
        });

        const data = await response.json();
        card.classList.remove('hidden');
        card.className = "status-card " + data.status;

        if (data.status === "baseline_created") {
            title.innerText = "BASELINE ESTABLISHED";
            msg.innerText = "File identified for the first time. Signature saved to database.";
            currentHash.innerText = data.hash;
            alertDetails.classList.add('hidden');
        } 
        else if (data.status === "verified") {
            title.innerText = "INTEGRITY VERIFIED";
            msg.innerText = "No changes detected. File matches the recorded baseline.";
            currentHash.innerText = data.hash;
            alertDetails.classList.add('hidden');
        } 
        else if (data.status === "alert") {
            title.innerText = "!!! TAMPER DETECTION !!!";
            msg.innerText = "CRITICAL: File contents have been modified!";
            currentHash.innerText = data.current;
            oldHash.innerText = data.old;
            alertDetails.classList.remove('hidden');
        }
    } catch (err) {
        alert("CRITICAL ERROR: Unable to access File System Engine.");
    }
};