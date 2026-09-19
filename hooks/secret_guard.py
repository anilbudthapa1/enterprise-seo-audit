import re
PATTERNS=[
 re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^\s]+"),
 re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]
def redact(text:str)->str:
    out=text
    for p in PATTERNS:
        out=p.sub("[REDACTED]",out)
    return out
