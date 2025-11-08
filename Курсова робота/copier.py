"""copier.py
Core FileCopier class implementing multi-threaded file copying with pause/resume/cancel
and per-thread progress reporting. Uses only Python standard library.
"""
import os
import threading
import time


class FileCopier:
    def __init__(self, num_threads=4, chunk_size=4 * 1024 * 1024):
        self.num_threads = max(1, int(num_threads))
        self.chunk_size = int(chunk_size)

        # runtime fields
        self.total_size = 0
        self.copied_size = 0
        self.start_time = None
        self.is_paused = False
        self.is_cancelled = False
        self.error = None

        # per-thread progress (bytes copied by that thread)
        self.thread_progress = {}

        # internal
        self._lock = threading.Lock()
        self._threads = []
        self._chunks = []  # list of (start, end)

    def calculate_chunks(self, file_size):
        # split file_size into self.num_threads parts (last takes remainder)
        parts = []
        part = file_size // self.num_threads
        for i in range(self.num_threads):
            start = i * part
            if i == self.num_threads - 1:
                end = file_size - 1
            else:
                end = (i + 1) * part - 1
            parts.append((start, end))
        return parts

    def _copy_chunk(self, source, destination, start, end, thread_id):
        bufsize = 64 * 1024  # 64KB
        try:
            with open(source, 'rb') as src, open(destination, 'r+b') as dst:
                src.seek(start)
                dst.seek(start)
                remaining = end - start + 1
                self.thread_progress[thread_id] = 0
                while remaining > 0:
                    if self.is_cancelled:
                        return
                    while self.is_paused:
                        time.sleep(0.1)
                        if self.is_cancelled:
                            return
                    to_read = bufsize if remaining > bufsize else remaining
                    data = src.read(to_read)
                    if not data:
                        break
                    dst.write(data)
                    with self._lock:
                        self.copied_size += len(data)
                        self.thread_progress[thread_id] += len(data)
                    remaining -= len(data)
        except Exception as e:
            # record error and cancel other threads
            with self._lock:
                self.error = str(e)
            self.is_cancelled = True

    def _sequential_copy(self, source, destination, progress_callback=None):
        bufsize = 64 * 1024
        try:
            with open(source, 'rb') as src, open(destination, 'wb') as dst:
                total = os.path.getsize(source)
                copied = 0
                start = time.time()
                while True:
                    if self.is_cancelled:
                        return {'success': False, 'time': time.time() - start, 'speed': 0.0, 'size': copied, 'error': 'cancelled'}
                    if self.is_paused:
                        time.sleep(0.1)
                        continue
                    data = src.read(bufsize)
                    if not data:
                        break
                    dst.write(data)
                    copied += len(data)
                    self.copied_size = copied
                    if progress_callback:
                        pct = copied / total * 100
                        speed = self.get_speed()
                        progress_callback(pct, speed, {0: copied})
                elapsed = time.time() - start
                speed = (copied / elapsed) / (1024 * 1024) if elapsed > 0 else 0.0
                return {'success': True, 'time': elapsed, 'speed': speed, 'size': copied, 'error': None}
        except Exception as e:
            return {'success': False, 'time': 0.0, 'speed': 0.0, 'size': 0, 'error': str(e)}

    def copy_file(self, source, destination, progress_callback=None):
        # validate
        if not os.path.isfile(source):
            return {'success': False, 'time': 0.0, 'speed': 0.0, 'size': 0, 'error': 'source not found'}

        file_size = os.path.getsize(source)
        self.total_size = file_size
        # small file -> sequential
        if file_size <= self.chunk_size:
            self.start_time = time.time()
            return self._sequential_copy(source, destination, progress_callback)

        # pre-allocate destination
        try:
            with open(destination, 'wb') as f:
                if file_size > 0:
                    f.truncate(file_size)
        except Exception as e:
            return {'success': False, 'time': 0.0, 'speed': 0.0, 'size': 0, 'error': str(e)}

        # prepare chunks and threads
        self._chunks = self.calculate_chunks(file_size)
        # Reset state
        self.copied_size = 0
        self.thread_progress = {}
        self.is_paused = False
        self.is_cancelled = False
        self.error = None

        self.start_time = time.time()
        self._threads = []

        for idx, (start, end) in enumerate(self._chunks):
            t = threading.Thread(target=self._copy_chunk, args=(source, destination, start, end, idx), daemon=True)
            self._threads.append(t)
            t.start()

        # monitor
        try:
            while any(t.is_alive() for t in self._threads):
                if progress_callback:
                    total_pct = (self.copied_size / file_size) * 100 if file_size else 0
                    speed = self.get_speed()
                    # copy of thread_progress to avoid race
                    with self._lock:
                        tp = dict(self.thread_progress)
                    progress_callback(total_pct, speed, tp)
                time.sleep(0.2)

            # one last update
            if progress_callback:
                speed = self.get_speed()
                with self._lock:
                    tp = dict(self.thread_progress)
                progress_callback(100.0, speed, tp)

            # check error
            if self.error:
                return {'success': False, 'time': time.time() - self.start_time, 'speed': self.get_speed(), 'size': self.copied_size, 'error': self.error}
            if self.is_cancelled:
                return {'success': False, 'time': time.time() - self.start_time, 'speed': self.get_speed(), 'size': self.copied_size, 'error': 'cancelled'}

            elapsed = time.time() - self.start_time
            speed = (self.copied_size / elapsed) / (1024 * 1024) if elapsed > 0 else 0.0
            return {'success': True, 'time': elapsed, 'speed': speed, 'size': self.copied_size, 'error': None}

        except Exception as e:
            return {'success': False, 'time': time.time() - (self.start_time or time.time()), 'speed': self.get_speed(), 'size': self.copied_size, 'error': str(e)}

    def get_speed(self):
        if not self.start_time:
            return 0.0
        elapsed = time.time() - self.start_time
        if elapsed <= 0:
            return 0.0
        with self._lock:
            copied = self.copied_size
        return (copied / elapsed) / (1024 * 1024)

    def pause(self):
        with self._lock:
            self.is_paused = True

    def resume(self):
        with self._lock:
            self.is_paused = False

    def cancel(self):
        with self._lock:
            self.is_cancelled = True
