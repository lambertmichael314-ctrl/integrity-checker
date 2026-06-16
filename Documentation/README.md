**# HIDS // File Integrity Monitor (SHA-256)**



A Host-based Intrusion Detection System (HIDS) utility that monitors files for unauthorized changes. By establishing a cryptographic baseline, it can detect even single-bit modifications to sensitive system or configuration files.



**## Project Structure**

```text

integrity-checker/

├── app.py                # Hashing Engine (SHA-256 Logic)

├── signatures.json       # Baseline Signature Database

├── requirements.txt      # Dependencies

├── static/

│   ├── css/style.css     # Forensic Monitoring UI

│   └── js/main.js        # Integrity Logic \& UI Handlers

└── templates/

&nbsp;   └── index.html        # Scanner Dashboard



**Security Implementation**

* **SHA-256 Verification**: Utilizes the industry-standard Secure Hash Algorithm (256-bit) for collision-resistant file fingerprinting.
* **Baseline Establishment**: Files are registered upon first scan, creating a 'known-good' signature against which all future scans are compared.
* **Tamper Detection**: Operates on the principle of the "Avalanche Effect"—any minor change in the input results in a radically different hash output, making tampering immediately visible.
* **Forensic Comparison**: In the event of a breach, the tool displays both the current and original signatures to aid in incident response.



**Setup \& Installation**



Run Monitor:

├── python app.py

&nbsp;	├── *The system operates on Port 5005.*



**Building the Standalone Monitor**



**Windows Command**: pyinstaller --onefile --noconsole --add-data "templates;templates" --add-data "static;static" app.py

