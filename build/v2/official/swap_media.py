"""Copy a .pptx, replacing media whose SHA-256 matches with new bytes: swap_media.py src dst old_sha=new_file ..."""
import hashlib, sys, zipfile
src, dst, pairs = sys.argv[1], sys.argv[2], sys.argv[3:]
repl = {}
for p in pairs:
    k, v = p.split("=", 1)
    repl[k] = open(v, "rb").read()
n = 0
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zo:
    for info in zi.infolist():
        data = zi.read(info.filename)
        h = hashlib.sha256(data).hexdigest()
        if h in repl:
            data = repl[h]; n += 1
        zo.writestr(info, data)
print(f"replaced {n} media file(s) -> {dst}")
