import tkinter as tk
from tkinter import filedialog, messagebox
import csv

class NoteHTMLGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Note HTML Generator")

        self.open_button = tk.Button(root, text="Open CSV File", command=self.open_file)
        self.open_button.pack(pady=20)

        self.file_path_label = tk.Label(root, text="No file selected")
        self.file_path_label.pack(pady=10)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Select CSV File"
        )
        
        if file_path:
            self.file_path_label.config(text=file_path)
            try:
                notes = self.read_csv(file_path)

                if not notes:
                    messagebox.showerror("Error", "CSV file is empty or headers are incorrect.")
                    return

                html_content = self.generate_html(notes)
                
                with open('notes.html', 'w') as file:
                    file.write(html_content)

                messagebox.showinfo("Success", "HTML file generated successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def read_csv(self, file_path):
        notes = []
        try:
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if 'filename' in row and 'date' in row and 'time' in row:
                        notes.append(row)
                    else:
                        return []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV file: {e}")
            return []
        return notes

    def generate_html(self, notes):
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Notes</title>
        </head>
        <body>
            <h1>Notes</h1>
            <table border="0" align="left">
        """

        for note in notes:
            filename = note.get('filename', '')
            date = note.get('date', '')
            time = note.get('time', '')
            html_content += f"""
            <tr>
                <td>
                    <a href="{filename}" style="text-decoration:none;">
                        {date} &nbsp;{time}
                    </a>
                    <font color="white"> p{date}</font>
                </td>
            </tr>
            """

        html_content += """
            </table>
        </body>
        </html>
        """

        return html_content

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteHTMLGenerator(root)
    root.mainloop()
