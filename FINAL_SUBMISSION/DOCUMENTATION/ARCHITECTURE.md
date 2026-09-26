# ARCHITECTURE

                         MATRI VAANI
                              |
             +----------------+----------------+
             |                                 |
           HINDI                            TRIBAL
                                             |
                              +--------------+--------------+
                              |                             |
                             HO                          SANTALI
                              |                             |
                           Ho ASR                   IndicTrans2/Sarvam
                              |                             |
                              +-------------+---------------+
                                            |
                                      SERVICE ROUTER
                                            |
                              +-------------+-------------+
                              |                           |
                         Translation                    TTS
                              |                           |
                              +-------------+-------------+
                                            |
                                      Android App

## Component Flow
- **Flutter App (Frontend)**: User interface capturing speech, textual input, and providing TTS playback.
- **FastAPI Backend (Middleware)**: Receives HTTP requests from the Android app, handles file storage, and routes requests to the correct inference endpoints.
- **Service Layer & Provider Router**: Based on the source language (e.g., Ho vs Santali), routes traffic.
- **Local Ho ASR**: Operates entirely locally using a Wav2Vec2 checkpoint (models/ho_asr). Does not pass through translation.
- **IndicTrans2 / Sarvam / Bhashini**: External models hosted on WSL2 or cloud endpoints used for Hindi and Santali text generation/TTS.
