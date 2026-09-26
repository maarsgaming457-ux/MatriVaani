# TTS Deployment Plan & Memory Strategy

This document details how MatriVaani will execute Text-to-Speech (TTS) on low-cost Android hardware strictly remaining under the `< 2 GB` RAM ceiling.

## 1. The 2GB Conundrum
MatriVaani consists of three primary ML engines:
- **ASR (Wav2Vec2)**: ~850 MB RAM
- **NMT (IndicTrans2)**: ~1.5 GB RAM (INT8)
- **TTS (VITS Candidate)**: ~150 MB RAM

**Simultaneous Total**: ~2.5 GB (Fails Hard Ceiling)

## 2. Model Lifecycle Management
To survive on a 2GB device, we cannot keep all three models in RAM simultaneously. We will implement strict **Sequential Lifecycle Management**.

### The Sequence
1. **Listening State**: 
   - ASR is loaded into RAM (850 MB). NMT and TTS are flushed.
   - User speaks Hindi.
2. **Translation State**:
   - ASR is explicitly unloaded (-850 MB).
   - NMT is loaded from disk (+1.5 GB).
   - Hindi text is translated to Santhali text.
3. **Speech State**:
   - NMT is explicitly unloaded (-1.5 GB).
   - TTS is loaded from disk (+150 MB).
   - Santhali text is synthesized to audio and played.

### Latency Trade-off
This sequential loading causes a delay. It may take 1-3 seconds to load NMT, and ~0.5 seconds to load TTS. 

## 3. Streaming / Incremental Generation
The **VITS** architecture is capable of high-speed inference but is fundamentally an end-to-end block processor. We will measure the `time-to-first-audio`. If VITS RTF (Real-Time Factor) is sufficiently low (e.g., `< 0.2` on ARM CPU), we will synthesize sentence-by-sentence rather than waiting for the entire translated paragraph to finish.

## 4. Android Feasibility
By selecting VITS over Parler-TTS, we ensure Android feasibility:
- **Export**: PyTorch -> ONNX.
- **Runtime**: ONNX Runtime (ORT) C++ API via JNI on Android.
- **Hardware Acceleration**: CPU execution via XNNPACK or NNAPI if supported.

## 5. Offline Requirement
MatriVaani TTS will run entirely on the local Android processor. **No external cloud APIs** (Google, Azure, Bhashini) will be used for production inference.
