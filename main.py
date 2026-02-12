import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk
import ttkbootstrap as tb
import time
import concurrent.futures
import subprocess
import sys
import pandas as pd
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# ---------------- INFO ----------------
APP_NAME = "PDF Structured Data Extractor"
APP_VERSION = "1.0"
APP_AUTHOR = "Mate Technologies"
APP_WEBSITE = "https://matetools.gumroad.com"

class PDFExtractorApp:
    def __init__(self, master):
        self.master = master
        self.master.title(f"{APP_NAME} {APP_VERSION}")
        self.master.geometry("1000x650")
        self.style = tb.Style(theme="superhero")

        # ================= VARIABLES =================
        self.folder_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Idle")
        self.progress_val = tk.DoubleVar(value=0)
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.results = []

        # ================= UI =================
        self.create_ui()

    def create_ui(self):

        tb.Label(
            self.master,
            text=f"{APP_NAME}",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(10, 2))

        tb.Label(
            self.master,
            text="Extract structured text data from scanned PDFs (ignores handwriting)",
            font=("Segoe UI", 10, "italic"),
            foreground="#9ca3af"
        ).pack(pady=(0, 10))

        top_frame = tb.Frame(self.master, padding=10)
        top_frame.pack(fill="x")

        tb.Button(top_frame, text="Select Folder", bootstyle="primary", command=self.select_folder).pack(side="left", padx=5)
        tb.Button(top_frame, text="Export to CSV", bootstyle="success", command=self.export_csv).pack(side="left", padx=5)
        tb.Button(top_frame, text="Pause", bootstyle="secondary", command=self.pause_scan).pack(side="left", padx=5)
        tb.Button(top_frame, text="Resume", bootstyle="info", command=self.resume_scan).pack(side="left", padx=5)
        tb.Button(top_frame, text="Stop", bootstyle="danger", command=self.stop_scan).pack(side="left", padx=5)
        tb.Button(top_frame, text="About", bootstyle="warning", command=self.show_about).pack(side="right", padx=5)

        tb.Label(top_frame, textvariable=self.status_var, bootstyle="info").pack(side="right", padx=5)

        table_frame = tb.Frame(self.master)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("file", "pages", "characters"), show="headings")
        self.tree.heading("file", text="File Name")
        self.tree.heading("pages", text="Pages")
        self.tree.heading("characters", text="Extracted Characters")
        self.tree.column("file", width=400)
        self.tree.column("pages", width=100, anchor="center")
        self.tree.column("characters", width=150, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.progress_bar = tb.Progressbar(self.master, variable=self.progress_val, maximum=100)
        self.progress_bar.pack(fill="x", padx=10, pady=5)

    # ================= BUTTON ACTIONS =================

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.start_scan(folder)

    def pause_scan(self):
        self.pause_event.set()
        self.status_var.set("Paused...")

    def resume_scan(self):
        self.pause_event.clear()
        self.status_var.set("Resuming...")

    def stop_scan(self):
        self.stop_event.set()
        self.status_var.set("Stopping...")

    def show_about(self):
        messagebox.showinfo(
            f"About {APP_NAME}",
            f"{APP_NAME} v{APP_VERSION}\n\n"
            "Extract structured data from consistently formatted PDFs.\n"
            "Uses intelligent OCR filtering to ignore handwriting.\n\n"
            f"{APP_AUTHOR}\n{APP_WEBSITE}"
        )

    # ================= SCANNING =================

    def start_scan(self, folder):
        self.stop_event.clear()
        self.pause_event.clear()
        self.results.clear()
        self.tree.delete(*self.tree.get_children())
        self.progress_val.set(0)
        threading.Thread(target=self.scan_folder_thread, args=(folder,), daemon=True).start()

    def scan_folder_thread(self, folder):
        self.status_var.set("Scanning PDFs...")
        pdf_files = []

        for root, _, files in os.walk(folder):
            for f in files:
                if f.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(root, f))

        total = len(pdf_files)
        if total == 0:
            self.status_var.set("No PDFs found.")
            return

        processed = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(self.process_pdf, pdf): pdf for pdf in pdf_files}

            for future in concurrent.futures.as_completed(futures):
                if self.stop_event.is_set():
                    return
                while self.pause_event.is_set():
                    time.sleep(0.2)

                result = future.result()
                self.results.append(result)
                self.master.after(0, lambda r=result: self.update_tree(r))

                processed += 1
                progress = (processed / total) * 100
                self.master.after(0, lambda p=progress: self.progress_val.set(p))

        self.master.after(0, lambda: self.status_var.set(f"Completed: {total} PDFs processed."))

    def process_pdf(self, path):
        file_name = os.path.basename(path)
        extracted_text = ""
        page_count = 0

        try:
            with pdfplumber.open(path) as pdf:
                page_count = len(pdf.pages)
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"

            # If no digital text found, fallback to OCR
            if not extracted_text.strip():
                images = convert_from_path(path, dpi=300)
                for img in images:
                    ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                    for i, word in enumerate(ocr_data["text"]):
                        conf = int(ocr_data["conf"][i])
                        # Ignore low-confidence (likely handwriting)
                        if conf > 70:
                            extracted_text += word + " "

        except Exception as e:
            return (file_name, 0, 0)

        char_count = len(extracted_text)

        return (file_name, page_count, char_count)

    def update_tree(self, result):
        file_name, pages, chars = result
        self.tree.insert("", "end", values=(file_name, pages, chars))

    # ================= EXPORT =================

    def export_csv(self):
        if not self.results:
            messagebox.showwarning("No Data", "No extracted data to export.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if not save_path:
            return

        df = pd.DataFrame(self.results, columns=["File Name", "Pages", "Extracted Characters"])
        df.to_csv(save_path, index=False)

        messagebox.showinfo("Export Complete", "Data exported successfully.")

# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFExtractorApp(root)
    root.mainloop()
