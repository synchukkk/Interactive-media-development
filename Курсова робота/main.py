import tkinter as tk
from gui import TurboFileCopierGUI
import traceback
from tkinter import messagebox
import sys


def main():
    try:
        root = tk.Tk()
        app = TurboFileCopierGUI(root)
        root.mainloop()
    except Exception:
        tb = traceback.format_exc()
        # show error in dialog (desktop users) and write to error log
        try:
            messagebox.showerror('Application Error', f'An unexpected error occurred:\n\n{tb}')
        except Exception:
            pass
        try:
            with open('error.log', 'a', encoding='utf-8') as fh:
                fh.write('\n' + ('=' * 60) + '\n')
                fh.write(tb)
        except Exception:
            pass
        # if running from console, also print
        try:
            print(tb, file=sys.stderr)
            input('Press Enter to exit...')
        except Exception:
            pass


if __name__ == '__main__':
    main()
