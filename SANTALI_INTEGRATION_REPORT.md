# Santali Integration Report

## Backend
The backend does not contain a local Hindi-to-Santali NMT model because training was previously blocked by a dataset quality gate (`BLOCKED_NO_DATA`). 

## Translation Provider
**STATUS: UNAVAILABLE**
- **Bhashini API:** The required API credentials (`BHASHINI_USER_ID`, `BHASHINI_API_KEY`, `BHASHINI_PIPELINE_ID`) are completely blank in the project's `.env` file, rendering Bhashini translation inaccessible.
- **IndicTrans2 Proxy:** The external `INDICTRANS2_API_URL` (`https://crevice-darkened-sacrifice.ngrok-free.dev`) configured in the `.env` file is currently **offline (ERR_NGROK_3200)**.
- Without an accessible external API or a local model, no Hindi-to-Santali translation can be retrieved.

## API Endpoint
The `/translate` endpoint routes requests to the translation service, but as documented above, the underlying provider for Santali fails immediately due to missing credentials and offline proxy servers.

## Flutter
The Santali target language option (`sat`) was intentionally **not added** to the `translator_screen.dart` dropdown because a working backend provider does not exist. Adding it would only result in a broken UX. Mundari (`unr`) remains fully functional and untouched.

## TTS
Santali TTS is explicitly unsupported by the provider (`st.warning("TTS NOT AVAILABLE")`). No integration was attempted.

## ASR
The experimental Santali ASR pilot suffers from a 100% WER (CTC blank collapse). As requested, it was kept entirely out of the production Hindi microphone pipeline.

## Windows Test
N/A (Integration gracefully blocked due to dead endpoints/credentials).

## Android Test
N/A (Santali dropdown excluded to prevent crashing the app).

## Mundari Regression Test
**PASS**. The existing Hindi-to-Mundari translation pipeline was explicitly protected. No Mundari models, generation parameters, or UI widgets were altered.

## Known Limitations
The complete lack of offline translation weights and the failure of all external API fallbacks means the MatriVaani application currently cannot translate Hindi to Santali.

## Files Modified
None. 

## Files Not Modified
`backend/best_model_main2` (and all other project files, as the test immediately blocked integration).

## Final Status
**E. Integration blocked** (Provider unavailable)
