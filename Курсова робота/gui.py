"""gui.py
Tkinter GUI for Turbo File Copier
"""
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
import time

from copier import FileCopier


class RoundedButton:
    """A simple rounded-corner button implemented with Canvas.

    It exposes a minimal subset of the tk.Button API used by the rest of
    the GUI: pack(), config(...), and a 'state' option (normal/disabled),
    plus changing the text.
    """
    def __init__(self, parent, text, command=None, radius=12, padding=8, bg='#3aa06b', fg='white'):
        self.parent = parent
        self.command = command
        self.radius = radius
        self.padding = padding
        self.bg = bg
        self.fg = fg
        self._text = text
        self.enabled = True

        self.canvas = tk.Canvas(parent, height=radius * 2 + padding, bd=0, highlightthickness=0, relief='flat')
        self._draw_button()
        # bind events (click / hover / press)
        self.canvas.bind('<Button-1>', self._on_click)
        self.canvas.bind('<Enter>', self._on_enter)
        self.canvas.bind('<Leave>', self._on_leave)
        self.canvas.bind('<ButtonPress-1>', self._on_press)
        self.canvas.bind('<ButtonRelease-1>', self._on_release)

    def _draw_button(self):
        self.canvas.delete('all')
        w = max(100, len(self._text) * 9) + self.padding * 2
        h = self.radius * 2 + self.padding // 2
        self.canvas.config(width=w, height=h)
        x0, y0, x1, y1 = 2, 2, w - 2, h - 2
        r = self.radius
        # base rounded rectangle
        self._create_rounded_rect(x0, y0, x1, y1, r, fill=self.bg, outline='')
        # subtle highlight strip
        try:
            highlight = self._blend_color(self.bg, '#ffffff', 0.12)
            self._create_rounded_rect(x0+1, y0+1, x1-1, y0 + (h//2), max(1, r-1), fill=highlight, outline='')
        except Exception:
            pass
        # text
        self.text_id = self.canvas.create_text(w // 2, h // 2, text=self._text, fill=self.fg, font=('Segoe UI', 10, 'bold'))

    def _create_rounded_rect(self, x1, y1, x2, y2, r=10, **kwargs):
        self.canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, style='pieslice', **kwargs)
        self.canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, style='pieslice', **kwargs)
        self.canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, style='pieslice', **kwargs)
        self.canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, style='pieslice', **kwargs)
        self.canvas.create_rectangle(x1 + r, y1, x2 - r, y2, **kwargs)
        self.canvas.create_rectangle(x1, y1 + r, x2, y2 - r, **kwargs)

    def _blend_color(self, c1, c2, t=0.5):
        try:
            c1 = c1.lstrip('#')
            c2 = c2.lstrip('#')
            r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
            r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)
            r = int(r1 * (1 - t) + r2 * t)
            g = int(g1 * (1 - t) + g2 * t)
            b = int(b1 * (1 - t) + b2 * t)
            return f'#{r:02x}{g:02x}{b:02x}'
        except Exception:
            return c1

    def _on_enter(self, event):
        try:
            self.canvas.config(cursor='hand2')
            self._orig_bg = getattr(self, '_orig_bg', self.bg)
            self.bg = self._blend_color(self.bg, '#ffffff', 0.07)
            self._draw_button()
        except Exception:
            pass

    def _on_leave(self, event):
        try:
            self.canvas.config(cursor='')
            if hasattr(self, '_orig_bg'):
                self.bg = self._orig_bg
            self._draw_button()
        except Exception:
            pass

    def _on_press(self, event):
        try:
            self.canvas.move(self.text_id, 0, 1)
        except Exception:
            pass

    def _on_release(self, event):
        try:
            self.canvas.move(self.text_id, 0, -1)
        except Exception:
            pass

    def _on_click(self, event):
        if not self.enabled:
            return
        if self.command:
            try:
                self.command()
            except Exception:
                # swallow - caller will handle exceptions as needed
                pass

    # minimal API
    def pack(self, **kwargs):
        return self.canvas.pack(**kwargs)

    def grid(self, **kwargs):
        return self.canvas.grid(**kwargs)

    def place(self, **kwargs):
        return self.canvas.place(**kwargs)

    def config(self, **kwargs):
        # support text and state
        if 'text' in kwargs:
            self._text = kwargs['text']
            try:
                self.canvas.itemconfig(self.text_id, text=self._text)
            except Exception:
                pass
        if 'state' in kwargs:
            self.enabled = kwargs['state'] != 'disabled'
            alpha = 1.0 if self.enabled else 0.45
            # dim colors when disabled
            try:
                fill = self.bg
                fg = self.fg
                if not self.enabled:
                    # compute a grayed color (approx)
                    fg = '#9a9a9a'
                    fill = '#555555'
                # redraw with new colors
                self.bg = fill
                self.fg = fg
                self._draw_button()
            except Exception:
                pass

    def destroy(self):
        try:
            self.canvas.destroy()
        except Exception:
            pass



class TurboFileCopierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('⚡ Turbo File Copier')
        self.root.geometry('650x600')
        self.root.resizable(False, False)
        # theme
        self.dark_mode = tk.BooleanVar(value=False)
        self.style = ttk.Style()

        self.copier = None
        self.copy_thread = None

        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()
        self.thread_count = tk.IntVar(value=4)

        self.thread_progress_bars = []
        self.thread_labels = []

        self.create_widgets()
        # apply initial theme after widgets exist
        self.apply_theme(self.dark_mode.get())

    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg='#383838', height=60)
        header.pack(fill='x')
        title = tk.Label(header, text='⚡ TURBO FILE COPIER', bg='#383838', fg='#b99bff', font=('Segoe UI', 14, 'bold'))
        title.pack(padx=12, pady=12)

        # Files frame
        files = ttk.LabelFrame(self.root, text='📁 Files', padding=10)
        files.pack(fill='x', padx=12, pady=8)

        tk.Label(files, text='Source:').grid(row=0, column=0, sticky='w')
        src_entry = ttk.Entry(files, textvariable=self.source_path, width=60, state='readonly')
        src_entry.grid(row=0, column=1, padx=6)
        ttk.Button(files, text='Browse', command=self.browse_source).grid(row=0, column=2)

        tk.Label(files, text='Destination:').grid(row=1, column=0, sticky='w', pady=6)
        dst_entry = ttk.Entry(files, textvariable=self.dest_path, width=60, state='readonly')
        dst_entry.grid(row=1, column=1, padx=6, pady=6)
        ttk.Button(files, text='Browse', command=self.browse_dest).grid(row=1, column=2)

        # Settings
        settings = ttk.LabelFrame(self.root, text='⚙️ Settings', padding=10)
        settings.pack(fill='x', padx=12, pady=8)
        tk.Label(settings, text='Threads:').grid(row=0, column=0, sticky='w')
        scale = tk.Scale(settings, from_=1, to=16, orient='horizontal', variable=self.thread_count, showvalue=True)
        scale.grid(row=0, column=1, sticky='we', padx=6)

        # Progress
        progress = ttk.LabelFrame(self.root, text='📊 Progress', padding=10)
        progress.pack(fill='both', expand=True, padx=12, pady=8)

        tk.Label(progress, text='Overall:').pack(anchor='w')
        self.overall_pb = ttk.Progressbar(progress, orient='horizontal', length=560, mode='determinate')
        self.overall_pb.pack(pady=4)
        self.overall_label = tk.Label(progress, text='0% | 0.00 MB/s')
        self.overall_label.pack(anchor='w')

        # thread canvas
        canvas_frame = tk.Frame(progress)
        canvas_frame.pack(fill='both', expand=True, pady=8)
        self.canvas = tk.Canvas(canvas_frame, height=260)
        self.canvas.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.thread_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.thread_frame, anchor='nw')
        self.thread_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        # control buttons
        controls = tk.Frame(self.root)
        controls.pack(fill='x', padx=12, pady=8)
        # replace tk.Buttons with rounded Canvas buttons
        self.start_btn = RoundedButton(controls, text='START COPY', command=self.start_copy, bg='#c7a4ff', fg='#1f1f1f')
        self.start_btn.pack(side='left', padx=6)
        self.pause_btn = RoundedButton(controls, text='⏸️ PAUSE', command=self.pause_copy, bg='#b99bff', fg='#1f1f1f')
        self.pause_btn.pack(side='left', padx=6)
        self.pause_btn.config(state='disabled')
        self.cancel_btn = RoundedButton(controls, text='CANCEL', command=self.cancel_copy, bg='#a77bff', fg='#1f1f1f')
        self.cancel_btn.pack(side='left', padx=6)
        self.cancel_btn.config(state='disabled')
        # theme toggle
        th = ttk.Checkbutton(header, text='Dark', variable=self.dark_mode, command=self._on_theme_toggle)
        th.pack(side='right', padx=12)

    def browse_source(self):
        path = filedialog.askopenfilename()
        if path:
            self.source_path.set(path)

    def browse_dest(self):
        path = filedialog.asksaveasfilename()
        if path:
            self.dest_path.set(path)

    def create_thread_progress_bars(self, num_threads):
        # clear
        for w in self.thread_frame.winfo_children():
            w.destroy()
        self.thread_progress_bars = []
        self.thread_labels = []
        for i in range(num_threads):
            lbl = tk.Label(self.thread_frame, text=f'Thread {i}: 0%')
            lbl.pack(anchor='w')
            pb = ttk.Progressbar(self.thread_frame, orient='horizontal', length=540, mode='determinate')
            pb.pack(pady=4)
            self.thread_labels.append(lbl)
            self.thread_progress_bars.append(pb)

    def start_copy(self):
        src = self.source_path.get().strip()
        dst = self.dest_path.get().strip()
        if not src or not dst:
            messagebox.showwarning('Missing', 'Please select source and destination paths')
            return
        num = self.thread_count.get()
        self.create_thread_progress_bars(num)
        self.copier = FileCopier(num_threads=num)

        # toggle buttons
        self.start_btn.config(state='disabled')
        self.pause_btn.config(state='normal')
        self.cancel_btn.config(state='normal')

        def run():
            result = self.copier.copy_file(src, dst, progress_callback=self.update_progress)
            # schedule finish on main thread
            self.root.after(0, lambda: self.copy_finished(result))

        self.copy_thread = threading.Thread(target=run, daemon=True)
        self.copy_thread.start()

    def update_progress(self, overall_percent, speed, thread_progress):
        # executed from copier thread; schedule UI update
        def ui_update():
            self.overall_pb['value'] = overall_percent
            self.overall_label.config(text=f"{overall_percent:.1f}% | {speed:.2f} MB/s")
            # update per-thread
            for tid, val in thread_progress.items():
                if tid < len(self.thread_progress_bars):
                    chunk = self.copier._chunks[tid]
                    chunk_size = chunk[1] - chunk[0] + 1
                    pct = (val / chunk_size) * 100 if chunk_size else 0
                    self.thread_progress_bars[tid]['value'] = pct
                    self.thread_labels[tid].config(text=f'Thread {tid}: {pct:.1f}%')

        self.root.after(0, ui_update)

    def pause_copy(self):
        if not self.copier:
            return
        if not self.copier.is_paused:
            self.copier.pause()
            self.pause_btn.config(text='▶️ RESUME')
        else:
            self.copier.resume()
            self.pause_btn.config(text='⏸️ PAUSE')

    def cancel_copy(self):
        if self.copier:
            self.copier.cancel()

    def copy_finished(self, result):
        # enable/disable
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled', text='⏸️ PAUSE')
        self.cancel_btn.config(state='disabled')
        if result.get('success'):
            messagebox.showinfo('Done', f"Success: {result.get('size')} bytes in {result.get('time'):.2f}s ({result.get('speed'):.2f} MB/s)")
        else:
            messagebox.showerror('Failed', f"Error: {result.get('error')}")

    def _on_theme_toggle(self):
        self.apply_theme(self.dark_mode.get())

    def apply_theme(self, dark: bool):
        """Apply dark or light theme to widgets using ttk.Style and widget config."""
        # prefer 'clam' for better color control
        try:
            self.style.theme_use('clam')
        except Exception:
            pass

        if dark:
            # dark gray backgrounds with light-gray text and light purple accents
            bg = '#2b2b2b'       # window background
            panel = '#383838'    # panels / frames
            fg = '#d6d6d6'       # main text (light gray)
            muted = '#9a9a9a'    # secondary text
            accent = '#b99bff'   # light purple accent
            btn_bg = accent
        else:
            # light gray theme with same purple accent
            bg = '#f0f0f0'
            panel = '#e6e6e6'
            fg = '#222222'
            muted = '#777777'
            accent = '#b99bff'
            btn_bg = accent

        # root/background
        try:
            self.root.configure(bg=bg)
        except Exception:
            pass

        # frames and labels via ttk styles
        self.style.configure('TLabel', background=panel, foreground=fg)
        self.style.configure('TFrame', background=panel)
        self.style.configure('TLabelFrame', background=panel, foreground=fg)
        self.style.configure('TEntry', fieldbackground=panel, foreground=fg)
        # progressbar
        self.style.configure('TProgressbar', troughcolor=('#444444' if dark else '#eef4ff'), background=accent)

        # update some widgets directly
        # header
        for child in self.root.winfo_children():
            try:
                child.configure(bg=panel)
            except Exception:
                pass

        # specific widgets
        try:
            self.overall_label.config(bg=panel, fg=fg)
        except Exception:
            pass

        # canvas and thread frame
        try:
            self.canvas.config(bg=panel)
            self.thread_frame.config(style='TFrame')
        except Exception:
            pass

        # Buttons (tk buttons)
        try:
            self.start_btn.config(bg=btn_bg, fg='white', activebackground=btn_bg)
            self.pause_btn.config(bg='#f39c12' if not dark else '#f39c12', fg='white')
            self.cancel_btn.config(bg='#e74c3c', fg='white')
        except Exception:
            pass
