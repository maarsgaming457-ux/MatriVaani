# Dual-Mode Implementation Report

*This document serves as the living status report for the dual-mode architecture implementation phases.*

```text
MATRI VAANI DUAL-MODE STATUS

Architecture:
ONLINE + OFFLINE

Online deployment:
BLOCKED (Pending VPS selection)

Cloud URL:
TBD

Offline Android:
PARTIAL (Under active development)

Offline capabilities:
None currently deployed to production Android runtime.

Online capabilities:
- Hindi → Mundari NMT
- Santali ASR
- TTS (External API)

Automatic fallback:
NO (Under development)

Manual mode:
NO (Under development)

Mundari mobile inference:
NO (Awaiting ONNX/TFLite port)

Santali mobile ASR:
NO (Awaiting ONNX/TFLite port)

Local TTS:
NO

Airplane-mode test:
NOT TESTED

Second-device test:
NOT TESTED

Mundari SHA256:
D3B7536F64B42EE7EA5F6D48F0D87461B3398ACBD3B84D5B8A233370812986B5

GitHub:
READY (Source code and LFS models tracked correctly)

Critical limitations:
- FastAPI models consume 3.5GB RAM, making free-tier hosting impossible.
- Conversion of PyTorch models to Android runtimes is pending.

Files changed:
- README.md
- docs/*
```

## Phase Status

- **DUAL-1 (Audit architecture):** ✅ Complete
- **DUAL-2 (Service abstraction):** ⏳ Pending
- **DUAL-3 (Prepare FastAPI for cloud):** ⏳ Pending
- **DUAL-4 (Deploy cloud backend):** ⏳ Pending
- **DUAL-5 (Connect Flutter to HTTPS):** ⏳ Pending
- **DUAL-6 (Offline inference feasibility):** ⏳ Pending
- **DUAL-7 (Mundari mobile inference):** ⏳ Pending
- **DUAL-8 (Santali mobile ASR):** ⏳ Pending
- **DUAL-9 (Local TTS):** ⏳ Pending
- **DUAL-10 (Automatic fallback):** ⏳ Pending
- **DUAL-11 (Airplane-mode testing):** ⏳ Pending
- **DUAL-12 (Android optimization):** ⏳ Pending
- **DUAL-13 (Documentation):** 🚧 In Progress
- **DUAL-14 (Final GitHub push):** ⏳ Pending
