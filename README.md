# PDF Structured Data Extractor — Python Tkinter App (Full Source Code)

**PDF Structured Data Extractor** is a Python desktop application built with **Tkinter** and **ttkbootstrap** for **scanning folders, extracting structured text from PDFs, and exporting results to CSV**.  
This repository contains the full source code, allowing you to customize **OCR logic, confidence filtering, multi-threading behavior, UI styling, and export functionality** for personal, educational, or professional document processing workflows.

------------------------------------------------------------
🌟 SCREENSHOT
------------------------------------------------------------

<img alt="PDF Structured Data Extractor" src="https://github.com/rogers-cyber/PDFStructuredDataExtractor/blob/main/PDF-Structured-Data-Extractor.jpg" />

------------------------------------------------------------
🌟 FEATURES
------------------------------------------------------------

- 📂 **Recursive Folder Scanning** — Scan any directory for PDF files  
- 📄 **Digital PDF Text Extraction** — Extract embedded text using `pdfplumber`  
- 🔎 **Smart OCR Fallback** — Automatically applies OCR when no digital text is found  
- ✍️ **Handwriting Filtering** — Ignores low-confidence OCR results (likely handwriting)  
- ⚡ **Multi-threaded Processing** — Concurrent PDF processing for faster performance  
- ⏸ **Pause / Resume / Stop** — Control the scanning process in real-time  
- 📊 **Live Progress Bar** — Real-time progress feedback  
- 📋 **Structured Results Table** — Displays file name, page count, and extracted character count  
- 📤 **CSV Export** — Export structured extraction summary to CSV  
- 🖥 **Modern UI** — Clean interface powered by ttkbootstrap theme  

------------------------------------------------------------
🚀 INSTALLATION
------------------------------------------------------------

1. Clone or download this repository:

```bash
git clone https://github.com/rogers-cyber/PDFStructuredDataExtractor.git
cd PDFStructuredDataExtractor
```

2. Install required Python packages:

```bash
pip install ttkbootstrap pandas pdfplumber pytesseract pdf2image pillow
```

3. Install external dependencies:

- **Tesseract OCR** (Required for OCR fallback)  
  Download: https://github.com/tesseract-ocr/tesseract  

- **Poppler** (Required for pdf2image)  
  - Windows: Install poppler and add to PATH  
  - macOS: `brew install poppler`  
  - Linux: `sudo apt install poppler-utils`

4. Run the application:

```bash
python main.py
```

------------------------------------------------------------
💡 USAGE
------------------------------------------------------------

1. **Select Folder**  
   - Click "Select Folder" to choose the directory containing PDFs.

2. **Automatic Processing**  
   - The app scans recursively for `.pdf` files.  
   - If digital text exists → extracts directly.  
   - If not → applies OCR and filters out low-confidence text (likely handwriting).

3. **Pause / Resume / Stop Scan**  
   - Pause scanning anytime with "Pause"  
   - Resume with "Resume"  
   - Stop entirely with "Stop"

4. **View Results**  
   - File Name  
   - Total Pages  
   - Extracted Character Count  

5. **Export to CSV**  
   - Click "Export to CSV"  
   - Save structured results for further analysis in Excel or other tools.

------------------------------------------------------------
⚙️ CONFIGURATION OPTIONS
------------------------------------------------------------

Option                  | Description
----------------------- | --------------------------------------------------
OCR Confidence Filter   | Words with confidence ≤ 70 are ignored
Thread Pool Size        | 4 worker threads (modifiable in code)
Pause / Resume / Stop   | Real-time scanning control
Progress Tracking       | Percentage-based progress bar
Treeview Display        | File name, page count, character count
CSV Export              | Structured summary export

------------------------------------------------------------
📦 OUTPUT
------------------------------------------------------------

- **File Name** — Name of processed PDF  
- **Pages** — Total number of pages  
- **Extracted Characters** — Count of structured text characters extracted  
- **CSV Export File** — Contains structured results for all processed PDFs  

------------------------------------------------------------
📦 DEPENDENCIES
------------------------------------------------------------

- Python 3.10+  
- Tkinter — GUI framework (built-in with Python)  
- ttkbootstrap — Modern themed widgets  
- pandas — CSV export  
- pdfplumber — Digital PDF text extraction  
- pytesseract — OCR engine interface  
- pdf2image — Convert PDF pages to images  
- Pillow — Image processing  
- concurrent.futures — Multi-threading  
- threading / os / subprocess / sys — System operations  

------------------------------------------------------------
📝 NOTES
------------------------------------------------------------

- Fully offline desktop application  
- Designed for consistently formatted structured PDFs  
- OCR is only used when no digital text is detected  
- Low-confidence OCR results are filtered to reduce handwriting noise  
- Performance depends on CPU and number of PDFs  
- Compatible with Windows, macOS, and Linux  

------------------------------------------------------------
👤 ABOUT
------------------------------------------------------------

**PDF Structured Data Extractor** is maintained by **Mate Technologies**, providing a **fast, structured, and intelligent PDF data extraction tool** for personal, educational, or professional use.

Website / Contact: https://matetools.gumroad.com  

------------------------------------------------------------
📜 LICENSE
------------------------------------------------------------

Distributed as source code.  
You may use it for personal or educational projects.  
Redistribution, resale, or commercial use requires explicit permission.

