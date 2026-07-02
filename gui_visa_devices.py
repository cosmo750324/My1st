import tkinter as tk
from tkinter import ttk, messagebox
import concurrent.futures
import os

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
    seen_idn = set()
    unique_results: list[tuple[str, str]] = []
    for res_name, idn in raw_results:
        if idn not in seen_idn:
            seen_idn.add(idn)
            unique_results.append((res_name, idn))
    return unique_results


def _categorize(devices: list[tuple[str, str]]) -> dict[str, list[tuple[str, str]]]:
    """Categorise devices based on known IDs.
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
    def __init__(self):
        super().__init__()
        self.title("VISA Device Browser")
        self.geometry("700x500")
        self._setup_widgets()
        self.refresh_devices()

    def _setup_widgets(self):
        toolbar = ttk.Frame(self)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        refresh_btn = ttk.Button(toolbar, text="Refresh", command=self.refresh_devices)
        refresh_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.heading("#0", text="Devices", anchor=tk.W)

    def refresh_devices(self):
        self.tree.delete(*self.tree.get_children())
        try:
            devices = _discover_devices()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to discover devices: {e}")
            return
        categories = _categorize(devices)
        for cat, devs in categories.items():
            if not devs:
                continue
            cat_id = self.tree.insert("", tk.END, text=cat, open=True)
            for res, idn in devs:
                self.tree.insert(cat_id, tk.END, text=f"{res} => {idn}")
    
    # INSTR functionality removed as per user request.

if __name__ == "__main__":
    app = VisaGui()
    app.mainloop()
