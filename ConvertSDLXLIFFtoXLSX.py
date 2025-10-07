# Convert sdlxliff to xlsx (Tkinter version, formatted output)
# pip install xlsxwriter
# By Bill Fan Zhxin

import os
import tkinter as tk
from tkinter import filedialog, messagebox
import xlsxwriter
from GetTUsInfosSDLXLIFF import GetTUsInfosSDLXLIFF


class SDLXLIFFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convert sdlxliff to XLSX 1.3")

        # 文件路径输入框
        tk.Label(root, text="File path:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.path_entry = tk.Entry(root, width=70)
        self.path_entry.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        # 选择文件按钮
        browse_btn = tk.Button(root, text="Browse .sdlxliff", command=self.browse_file)
        browse_btn.grid(row=0, column=2, padx=5, pady=10)

        # 作者信息
        tk.Label(root, text="By SuperBill (fzx2004@126.com)").grid(row=1, column=1, padx=10, sticky="w")

        # 转换按钮
        convert_btn = tk.Button(root, text="Convert to XLSX", command=self.convert_to_xlsx)
        convert_btn.grid(row=1, column=2, padx=5, pady=10, sticky="e")

    def browse_file(self):
        filenames = filedialog.askopenfilenames(
            title="Select sdlxliff files",
            filetypes=[("sdlxliff files", "*.sdlxliff"), ("All files", "*.*")]
        )
        if filenames:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, filenames[0].replace('/', '\\'))

    def convert_to_xlsx(self):
        filepath = self.path_entry.get().strip()
        if not filepath or not os.path.isfile(filepath):
            messagebox.showwarning("Warning", "Please select a valid .sdlxliff file.")
            return

        try:
            tulist = GetTUsInfosSDLXLIFF(filepath)
            if not tulist:
                messagebox.showinfo("Info", "No translation units found.")
                return

            xlsx_path = os.path.splitext(filepath)[0] + ".xlsx"
            wb = xlsxwriter.Workbook(xlsx_path)
            ws = wb.add_worksheet()

            headers = [
                "Filepath", "SegmentID", "Source", "Source Language Code",
                "Target", "Target Language Code", "Modified On", "Last Modified By", "Created On", "Created By", "Status", "Structure",
                "origin", "origin-system", "percent", "Locked"
            ]

            # === 样式设置 ===
            header_fmt = wb.add_format({
                'bold': True,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'bg_color': '#D9E1F2'
            })

            cell_fmt = wb.add_format({
                'text_wrap': True,    # 自动换行
                'valign': 'top',
                'border': 1
            })

            # 固定列宽
            ws.set_column(0, len(headers)-1, 25)

            # 写入表头
            for col, header in enumerate(headers):
                ws.write(0, col, header, header_fmt)

            # 写入翻译单元数据
            for row, tuinfo in enumerate(tulist, start=1):
                for col, value in enumerate(tuinfo):
                    ws.write(row, col, str(value), cell_fmt)

            wb.close()
            messagebox.showinfo("Success", f"Conversion completed!\nSaved as:\n{xlsx_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SDLXLIFFConverterApp(root)
    root.resizable(False, False)
    root.mainloop()
