# AIP Measure Tool
import tkinter as tk
from tkinter import ttk, messagebox
import concurrent.futures
import os
import json

STATE_FILE = "visa_gui_state.json"

# Try importing pyvisa; show error if missing
try:
    import pyvisa
except ImportError:
    tk.messagebox.showerror(
        "Import Error",
        "pyvisa 模組未安裝。請執行 'pip install pyvisa' 以安裝所需套件。"
    )
    raise


def _discover_devices() -> list[tuple[str, str]]:
    """Discover VISA devices concurrently.
    Returns a list of unique (resource_name, idn_string) tuples (deduplicated by IDN).
    Devices that do not respond within 1 s are omitted.
    """
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()

    def _query(res_name: str):
        """Open a VISA resource, query *IDN?* with 1 s timeout, return (res, idn) or None."""
        try:
            instr = rm.open_resource(res_name)
            instr.timeout = 1000  # ms
            try:
                idn = instr.query("*IDN?")
            except Exception:
                return None
            finally:
                instr.close()
            return (res_name, idn.strip())
        except Exception:
            return None

    if not resources:
        return []

    max_workers = min(32, len(resources))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_query, r): r for r in resources}
        raw_results = []
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                raw_results.append(res)
    # Deduplicate by IDN (keep first occurrence)
    seen = set()
    unique: list[tuple[str, str]] = []
    for name, idn in raw_results:
        if idn not in seen:
            seen.add(idn)
            unique.append((name, idn))
    return unique


def _categorize(devices: list[tuple[str, str]]) -> dict[str, list[tuple[str, str]]]:
    """Categorise devices based on known identifiers.
    Falls back to generic heuristics if no specific match.
    """
    categories = {
        "Power Supply": [],
        "Scope": [],
        "Thermal": [],
        "Function Generator": [],
        "Data Logger": [],
        "Other": [],
    }
    for res, idn in devices:
        low = idn.lower()
        # Specific known models
        if "n6705" in low:
            categories["Power Supply"].append((res, idn))
        elif "mso" in low:
            categories["Scope"].append((res, idn))
        # Generic heuristics
        elif "power" in low or "supply" in low:
            categories["Power Supply"].append((res, idn))
        elif "scope" in low or "oscilloscope" in low:
            categories["Scope"].append((res, idn))
        elif "temp" in low or "thermal" in low or "therm" in low:
            categories["Thermal"].append((res, idn))
        elif "function" in low or "generator" in low:
            categories["Function Generator"].append((res, idn))
        elif "logger" in low or "data" in low:
            categories["Data Logger"].append((res, idn))
        else:
            categories["Other"].append((res, idn))
    return categories


class VisaGui(tk.Tk):
    """GUI containing the requested controls.
    - Thermal?: Y/N – execute temperature action when set to Y.
    - Search_Inst: Y/N – auto‑search instruments on start.
    - INSTR?: search and categorize instruments.
    - TEST_ITEM: placeholder test action.
    - INITIALIZE: reset UI to initial state.
    - Exit: close program.
    """
    def __init__(self):
        super().__init__()
        self.title("VISA Device Manager")
        self.geometry("800x600")
        # State variables
        self.thermal_var = tk.StringVar(value="N")
        self.search_inst_var = tk.StringVar(value="N")
        # Load saved state if available
        self._load_state()
        # Save state whenever toggles change
        self.thermal_var.trace_add('write', lambda *args: self._save_state())
        self.search_inst_var.trace_add('write', lambda *args: self._save_state())
        self._setup_widgets()
        # Auto‑search if enabled on start
        if self.search_inst_var.get() == "Y":
            self.instr_search()

    def _setup_widgets(self):
        toolbar = ttk.Frame(self)
        toolbar.pack(side=tk.TOP, fill=tk.X, pady=4)
        # Thermal toggle
        ttk.Label(toolbar, text="Thermal?:").pack(side=tk.LEFT, padx=2)
        ttk.OptionMenu(toolbar, self.thermal_var, "N", "Y", "N").pack(side=tk.LEFT, padx=2)
        # Search_Inst toggle
        ttk.Label(toolbar, text="Search_Inst:").pack(side=tk.LEFT, padx=2)
        ttk.OptionMenu(toolbar, self.search_inst_var, "N", "Y", "N").pack(side=tk.LEFT, padx=2)
        # INSTR? button
        ttk.Button(toolbar, text="INSTR?", command=self.instr_search).pack(side=tk.LEFT, padx=5)
        # TEST_ITEM button
        ttk.Button(toolbar, text="TEST_ITEM", command=self.test_item).pack(side=tk.LEFT, padx=5)
        # INITIALIZE button
        ttk.Button(toolbar, text="INITIALIZE", command=self.initialize).pack(side=tk.LEFT, padx=5)
        # Exit button
        ttk.Button(toolbar, text="Exit", command=self.quit).pack(side=tk.RIGHT, padx=5)
        # Treeview for displaying devices
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.heading("#0", text="Devices", anchor=tk.W)
        # Status bar
        self.status = ttk.Label(self, text="Ready", anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def set_status(self, msg: str):
        self.status.config(text=msg)
        self.update_idletasks()

    def instr_search(self):
        """Search connected instruments, populate the tree, and run thermal action if selected."""
        self.set_status("Searching instruments…")
        try:
            devices = _discover_devices()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to discover devices: {e}")
            self.set_status("Search failed")
            return
        categories = _categorize(devices)
        self.tree.delete(*self.tree.get_children())
        for cat, devs in categories.items():
            if not devs:
                continue
            cat_id = self.tree.insert("", tk.END, text=cat, open=True)
            for res, idn in devs:
                self.tree.insert(cat_id, tk.END, text=f"{res} => {idn}")
        self.set_status("Search completed")
        if self.thermal_var.get() == "Y":
            self.perform_thermal_action()

    def perform_thermal_action(self):
        """Placeholder for temperature‑related action."""
        messagebox.showinfo("Thermal Action", "Thermal action executed (placeholder).")

    def test_item(self):
        """Placeholder for TEST_ITEM functionality."""
        messagebox.showinfo("TEST_ITEM", "Test started (functionality not implemented).")
        self.set_status("Test started")

    def initialize(self):
        """Reset UI to its initial state."""
        self.thermal_var.set("N")
        self.search_inst_var.set("N")
        self.tree.delete(*self.tree.get_children())
        self.set_status("Initialized – toggles reset, list cleared")
        # Save reset state
        self._save_state()

    def _load_state(self):
        """Load toggle states from STATE_FILE if it exists."""
        try:
            if os.path.isfile(STATE_FILE):
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.thermal_var.set(data.get("thermal", "N"))
                    self.search_inst_var.set(data.get("search_inst", "N"))
        except Exception as e:
            messagebox.showwarning("State Load Warning", f"Failed to load state: {e}")

    def _save_state(self):
        """Save current toggle states to STATE_FILE."""
        try:
            data = {
                "thermal": self.thermal_var.get(),
                "search_inst": self.search_inst_var.get(),
            }
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showwarning("State Save Warning", f"Failed to save state: {e}")

if __name__ == "__main__":
    app = VisaGui()
    app.mainloop()
