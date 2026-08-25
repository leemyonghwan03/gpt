from __future__ import annotations

import argparse
import os
import sys
import traceback
from pathlib import Path


def frozen_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def win_message(title: str, message: str) -> None:
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)
    except Exception:
        pass


def build_window():
    import tkinter as tk

    root = tk.Tk()
    root.title("Document Assistant - Windows Verified Shell")
    root.geometry("410x360+80+80")
    root.minsize(360, 280)
    root.configure(bg="#f5f6f8")
    root.attributes("-topmost", True)

    header = tk.Frame(root, bg="#111827", padx=16, pady=14)
    header.pack(fill="x")
    tk.Label(header, text="Document Assistant", bg="#111827", fg="white",
             font=("Malgun Gothic", 15, "bold")).pack(anchor="w")
    tk.Label(header, text="Windows verified companion shell", bg="#111827", fg="#cbd5e1",
             font=("Malgun Gothic", 9)).pack(anchor="w", pady=(2, 0))

    body = tk.Frame(root, bg="#f5f6f8", padx=14, pady=14)
    body.pack(fill="both", expand=True)

    card = tk.Frame(body, bg="white", padx=13, pady=13, highlightthickness=1,
                    highlightbackground="#e5e7eb")
    card.pack(fill="x")
    tk.Label(card, text="● Windows 실행 정상", bg="white", fg="#166534",
             font=("Malgun Gothic", 10, "bold")).pack(anchor="w")
    tk.Label(card, text="이 창은 Python이 설치되지 않은 PC에서도 실행되는\nPyInstaller 배포 구조 검증용입니다.",
             bg="white", fg="#475569", justify="left",
             font=("Malgun Gothic", 9)).pack(anchor="w", pady=(8, 0))

    actions = tk.Frame(body, bg="#f5f6f8")
    actions.pack(fill="x", pady=(12, 0))
    for text in ("문서 분석", "양식 분석", "기존 양식으로 작성", "표 자동 정리"):
        tk.Button(actions, text=text, state="disabled", relief="flat",
                  bg="#e5e7eb", fg="#64748b", padx=8, pady=9).pack(fill="x", pady=3)

    return root


def windows_probe() -> dict:
    import tkinter  # noqa
    import win32api  # noqa
    import win32con  # noqa
    import win32gui
    import win32process  # noqa
    import pythoncom  # noqa
    import pywinauto  # noqa

    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd) if hwnd else ""
    return {"hwnd": int(hwnd or 0), "title": title}


def selftest() -> int:
    out = frozen_dir() / "WINDOWS_SELFTEST_PASS.txt"
    if out.exists():
        out.unlink()

    probe = windows_probe()
    root = build_window()
    root.update_idletasks()
    root.update()
    geometry = root.geometry()
    topmost = root.attributes("-topmost")
    root.destroy()

    out.write_text(
        "WINDOWS_SELFTEST=PASS\n"
        f"PYTHON={sys.version}\n"
        f"FROZEN={getattr(sys, 'frozen', False)}\n"
        f"GEOMETRY={geometry}\n"
        f"TOPMOST={topmost}\n"
        f"FOREGROUND_HWND={probe['hwnd']}\n"
        f"FOREGROUND_TITLE={probe['title']}\n",
        encoding="utf-8",
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.selftest:
            return selftest()
        windows_probe()
        root = build_window()
        root.mainloop()
        return 0
    except Exception:
        detail = traceback.format_exc()
        try:
            (frozen_dir() / "WINDOWS_STARTUP_ERROR.txt").write_text(detail, encoding="utf-8")
        except Exception:
            pass
        if not args.selftest:
            win_message("Document Assistant 시작 실패", detail[-1800:])
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
