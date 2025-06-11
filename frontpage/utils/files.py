import zipfile

OLE_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"


def is_excel_stream(f):
    f.seek(0)
    buf = f.read(8)
    f.seek(0)
    return zipfile.is_zipfile(f) or buf.startswith(OLE_MAGIC)
