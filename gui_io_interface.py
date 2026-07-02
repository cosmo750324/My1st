# GUI Layout replication based on the provided description
# Three entry fields, two buttons, and a listbox arranged vertically on the left side.
# No functional logic is implemented – only the visual arrangement.

import tkinter as tk
from tkinter import ttk


class IoControlInterface(tk.Tk):
    """Tkinter window that mirrors the described IO control interface.

    Layout (left side, vertical):
        • Entry 1
        • Entry 2
        • Entry 3
        • Button 1
        • Button 2
        • Listbox (display area)
    """

    def __init__(self):
        super().__init__()
        self.title("IO 控制介面")
        self.geometry("400x500")
        self._create_widgets()

    def _create_widgets(self):
        # Container frame for vertical stacking
        container = ttk.Frame(self, padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        # Three entry fields
        self.entry_vars = []
        for i in range(1, 4):
            var = tk.StringVar()
            entry = ttk.Entry(container, textvariable=var, width=30)
            entry.pack(pady=5, anchor="w")
            self.entry_vars.append(var)

        # Two buttons
        self.button1 = ttk.Button(container, text="Button 1")
        self.button1.pack(pady=5, anchor="w")
        self.button2 = ttk.Button(container, text="Button 2")
        self.button2.pack(pady=5, anchor="w")

        # Listbox (with a vertical scrollbar)
        listbox_frame = ttk.Frame(container)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.listbox = tk.Listbox(listbox_frame, height=10)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Placeholder items for visual reference (can be removed later)
        for idx in range(1, 6):
            self.listbox.insert(tk.END, f"Item {idx}")


if __name__ == "__main__":
    app = IoControlInterface()
    app.mainloop()
