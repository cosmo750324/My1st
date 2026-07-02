"""
Utility script to list VISA-connected instruments.

Requires pyvisa: pip install pyvisa
"""

import concurrent.futures

try:
    import pyvisa
except ImportError:
    import sys
    print("pyvisa 模組未安裝。請執行 'pip install pyvisa' 以安裝所需套件。")
    sys.exit(1)

def list_visa_devices():
    """List all connected VISA resources detected on the system and print them.
    Devices that cannot be opened (e.g., not connected).
    Queries are performed concurrently to improve discovery speed.
    Each device is given a 1‑second timeout for the *IDN? query.
    """
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()

    def _query(res_name: str):
        """Open a VISA resource and query its *IDN?*.
        Return (res_name, idn) if successful, otherwise None.
        """
        try:
            instr = rm.open_resource(res_name)
            instr.timeout = 1000  # milliseconds
            try:
                idn = instr.query('*IDN?')
            except Exception:
                idn = "<no response>"
            finally:
                instr.close()
            return (res_name, idn.strip())
        except Exception:
            return None

    # Use a thread pool to query resources in parallel.
    max_workers = min(32, len(resources) or 1)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_query, r): r for r in resources}
        connected = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                connected.append(result)

    if not connected:
        print("No connected VISA devices found.")
    else:
        print("Found connected VISA devices:")
        for res, idn in connected:
            print(f" - {res} => {idn}")

if __name__ == "__main__":
    list_visa_devices()
