import os, tempfile, time
from copier import FileCopier

# create temporary source file ~6MB
src = os.path.join(tempfile.gettempdir(), 'tfc_test_src.bin')
dst = os.path.join(tempfile.gettempdir(), 'tfc_test_dst.bin')

# write 6MB of data
with open(src, 'wb') as f:
    f.write(os.urandom(6 * 1024 * 1024))

copier = FileCopier(num_threads=4, chunk_size=1 * 1024 * 1024)

def progress(pct, speed, thread_progress):
    print(f"\r{pct:.1f}% | {speed:.2f} MB/s", end='')

print('Starting test copy...')
res = copier.copy_file(src, dst, progress_callback=progress)
print('\nResult:', res)

# cleanup
os.remove(src)
if os.path.exists(dst):
    os.remove(dst)
