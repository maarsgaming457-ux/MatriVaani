# PRESENTATION CONTENT

**Slide 1: MatriVaani**
AI-Powered Vernacular Pedagogy and Real-Time Translation Tool

**Slide 2: Problem**
Millions of tribal students face educational barriers because their mother tongues (e.g., Ho, Santali) lack widespread digital translation tools and teacher support.

**Slide 3: Target Users**
Educators, tribal students, and regional administrators across low-resource linguistic communities in India.

**Slide 4: Proposed Solution**
An Android-first, hybrid-cloud application that provides speech-to-text, localized AI translation, and offline transcription for remote classrooms.

**Slide 5: Languages and Capabilities**
- Hindi: Full ASR, Translation, TTS
- Santali: Full ASR, Translation, TTS
- Ho: Offline ASR

**Slide 6: System Architecture**
Flutter App -> FastAPI Backend -> Service Router -> Local/Cloud Models (IndicTrans2, Sarvam, local Ho ASR).

**Slide 7: AI/ML Technology Stack**
- Flutter / Dart
- FastAPI / Python
- Fine-tuned Wav2Vec2 (Ho ASR)
- IndicTrans2 (Translation)
- Sarvam/Bhashini APIs

**Slide 8: Classroom Workflow**
A teacher records speech. The app seamlessly orchestrates offline transcription and, if supported, pushes text to the translation layer, rendering both textual and audio synthesis.

**Slide 9: Demonstrated Results**
- Reliable Hindi <-> Santali translation.
- High-accuracy offline Ho transcription.

**Slide 10: Offline/Online Architecture**
Crucial tasks like Ho transcription run locally without the internet, bypassing typical infrastructural limitations of rural classrooms. High-end translations fall back on secure WSL/Cloud resources.

**Slide 11: Current Limitations**
- Ho translation to Hindi/Santali is not yet available.
- Android Emulator restricts genuine Ho microphone speech capture natively.

**Slide 12: Future Scope**
Developing parallel datasets to train Ho-Hindi translation models and expanding our offline inference capabilities to edge devices fully.
