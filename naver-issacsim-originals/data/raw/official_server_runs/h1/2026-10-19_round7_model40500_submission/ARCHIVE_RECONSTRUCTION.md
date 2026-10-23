# Multipart archive handoff

This directory contains byte-for-byte chunks of the original archive. Each
`<archive-name>.partNNN` file is at most 1,800,000,000 bytes and the part order
is the zero-padded numeric suffix.

`SHA256SUMS` records the original archive SHA-256 and every part SHA-256. The
parts were also read sequentially and their combined SHA-256 was compared with
the original archive SHA-256.

To reconstruct on Windows PowerShell without changing the source parts:

```powershell
$parts = Get-ChildItem -LiteralPath . -Filter '20261018-162226-h1-top01-from9999-plus32500-download.tar.gz.part*' |
    Sort-Object Name
$output = [System.IO.File]::Open('20261018-162226-h1-top01-from9999-plus32500-download.tar.gz', 'CreateNew', 'Write', 'None')
try {
    foreach ($part in $parts) {
        $input = [System.IO.File]::OpenRead($part.FullName)
        try { $input.CopyTo($output) } finally { $input.Dispose() }
    }
} finally { $output.Dispose() }
```

Run `Get-FileHash -Algorithm SHA256` on the reconstructed archive and compare
it with the original archive entry in `SHA256SUMS`.
