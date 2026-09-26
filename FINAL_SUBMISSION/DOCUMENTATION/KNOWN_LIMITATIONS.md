# KNOWN LIMITATIONS

1. **Ho Translation Unavailable**: Ho translation to Hindi/Santali is not yet available in this prototype due to the lack of parallel datasets.
2. **Ho TTS Unavailable**: Text-to-speech for the Ho language is unsupported.
3. **Emulator Microphone Constraint**: Genuine Ho speech through the Android emulator microphone was not independently validated due to hardware passthrough constraints. Test files must be routed via the backend for emulation.
4. **WSL Dependency**: Hindi/Santali translation depends heavily on the local WSL IndicTrans2 service running simultaneously in the current demo environment.
5. **No Network Error Fallbacks**: Some offline operations gracefully trap errors but require network restoration or WSL activation to retry successfully (e.g., HTTP 500 timeouts when IndicTrans2 is unreachable).
