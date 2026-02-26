import hashlib
import os
import time
from dataclasses import dataclass, asdict

CHUNK = 1024 * 1024

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(CHUNK)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

@dataclass(frozen=True)
class Proof:
    schema: str
    tool: str
    version: str
    created_utc: int
    file_path: str
    file_size: int
    file_mtime_ns: int
    sha256: str

    def to_dict(self):
        return asdict(self)

def make_proof(path, tool, version):
    st = os.stat(path)
    return Proof(
        schema="winstack.proof.v1",
        tool=tool,
        version=version,
        created_utc=int(time.time()),
        file_path=os.path.abspath(path),
        file_size=st.st_size,
        file_mtime_ns=st.st_mtime_ns,
        sha256=sha256_file(path),
    )

def compare(path, proof):
    observed = sha256_file(path)
    expected = proof["sha256"]
    return observed == expected, observed, expected
