import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Storage")
        self.notes = []

        if not os.path.exists("notes"):
            os.makedirs("notes")

        self.filename_label = tk.Label(root, text="Filename:")
        self.filename_label.grid(row=0, column=0, padx=10, pady=5)
        self.filename_entry = tk.Entry(root)
        self.filename_entry.grid(row=0, column=1, padx=10, pady=5)

        self.note_label = tk.Label(root, text="Note Content:")
        self.note_label.grid(row=1, column=0, padx=10, pady=5)
        self.note_entry = tk.Text(root, height=10, width=30)
        self.note_entry.grid(row=1, column=1, padx=10, pady=5)

        self.save_button = tk.Button(root, text="Save Note", command=self.save_note)
        self.save_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.export_button = tk.Button(root, text="Export to CSV", command=self.export_to_csv)
        self.export_button.grid(row=3, column=0, columnspan=2, pady=10)

    def save_note(self):
        filename = self.filename_entry.get()
        content = self.note_entry.get("1.0", tk.END).strip()

        if filename and content:
            if not filename.lower().endswith(".html"):
                filename += ".html"
            
            now = datetime.now()
            date = now.strftime("%m.%d.%y")
            time = now.strftime("%I:%M %p")

            html_content = f"""
            <meta name="viewport" content="width=device-width, initial-scale=1.0,"/>
            <head>
                <link rel="stylesheet" href="mainq.css" media="screen"/>
                <link rel="stylesheet" href="noteq.css" media="screen and (max-device-width: 800px)"/>
            </head>
            <body>
            {content}
            </body>
            """
            file_path = os.path.join("notes", filename)
            try:
                with open(file_path, "w") as file:
                    file.write(html_content.strip())
                self.notes.append({"filename": filename, "date": date, "time": time})
                self.clear_entries()
                messagebox.showinfo("Info", f"Note saved successfully as {filename}!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save note: {e}")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields!")

    def clear_entries(self):
        self.filename_entry.delete(0, tk.END)
        self.note_entry.delete("1.0", tk.END)

    def export_to_csv(self):
        if not self.notes:
            messagebox.showwarning("Warning", "No notes to export!")
            return

        with open("notes.csv", "w", newline="") as csvfile:
            fieldnames = ["filename", "date", "time"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for note in self.notes:
                writer.writerow(note)

        messagebox.showinfo("Info", "Notes exported to notes.csv successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
