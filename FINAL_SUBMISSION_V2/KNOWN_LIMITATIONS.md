# KNOWN LIMITATIONS

1. **Ho Translation is disabled:** ASR works, but translation is explicitly blocked. BhashaVerse 1.1B zero-shot failed. Requires genuine parallel data (Phase 12 dataset generation ongoing).
2. **Offline TTS:** Text-to-Speech requires internet connectivity in this build.
3. **IndicTrans2 Cold Start:** First translation request may take up to 20 seconds.
