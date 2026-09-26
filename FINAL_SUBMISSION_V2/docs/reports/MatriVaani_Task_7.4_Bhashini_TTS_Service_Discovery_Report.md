# MatriVaani — Task 7.4 Bhashini TTS Service Discovery Report

## 1. Discovery method
Attempted to query the official Bhashini pipeline configuration API (https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline) to dynamically resolve the 	askType: tts configuration for hi and sat. However, the endpoint strictly requires developer authentication headers (userID, ulcaApiKey, Authorization) and a valid pipelineId.

Upon inspecting the local environment (.env), the required credentials (BHASHINI_USER_ID, BHASHINI_API_KEY, BHASHINI_PIPELINE_ID) are absent/blank.

As per the explicit task instructions ("If credentials are required and unavailable: STOP and report that discovery is blocked by authentication"), the live API call was aborted.

## 2. Hindi TTS availability
**BLOCKED BY AUTHENTICATION**

## 3. Hindi service configuration
**BLOCKED BY AUTHENTICATION**

## 4. Santali TTS availability
**BLOCKED BY AUTHENTICATION**

## 5. Santali service configuration
**BLOCKED BY AUTHENTICATION**

## 6. Ol Chiki verification
**BLOCKED BY AUTHENTICATION**

## 7. Voices
**BLOCKED BY AUTHENTICATION**

## 8. Audio configuration
**BLOCKED BY AUTHENTICATION**

## 9. Service ID behavior
**BLOCKED BY AUTHENTICATION** (Dynamic discovery relies on passing a valid pipelineId which is not available).

## 10. /tts compatibility
**BLOCKED BY AUTHENTICATION**

## 11. Risks
- Without valid Bhashini developer credentials, it is impossible to dynamically confirm the live status of the Santali Ol Chiki TTS service.
- The project is halted on Bhashini integration until credentials are provided.

## 12. Final decision
**D. DISCOVERY BLOCKED BY AUTHENTICATION**

## 13. Exact next task
Provide and configure valid Bhashini credentials (BHASHINI_USER_ID, BHASHINI_API_KEY, BHASHINI_PIPELINE_ID) in the .env file so that live pipeline discovery and service ID validation can safely proceed.

---

FILES MODIFIED:
NONE

PACKAGES INSTALLED:
NONE

TTS SYNTHESIS CALLED:
NO

ASR CHANGED:
NO

TRANSLATION CHANGED:
NO

FLUTTER CHANGED:
NO

CREDENTIALS EXPOSED:
NO
