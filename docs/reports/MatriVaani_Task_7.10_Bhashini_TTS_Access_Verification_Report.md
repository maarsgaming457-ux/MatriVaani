# MatriVaani — Task 7.10 Bhashini TTS Access Verification Report

## 1. Current credential state
**BHASHINI CREDENTIALS AVAILABLE: NO**
The .env file contains empty placeholders for BHASHINI_USER_ID, BHASHINI_API_KEY, and BHASHINI_PIPELINE_ID. Because no legitimate credentials exist, dynamic pipeline discovery and access verification cannot technically be performed.

## 2. Official Bhashini access requirements
To acquire the necessary keys, a developer must:
1. Navigate to the official Bhashini portal (e.g., https://bhashini.gov.in/).
2. Register for a Developer account or Organization account.
3. Once logged in, navigate to the API Dashboard or Developer Settings.
4. Generate an API Key/Token.
5. Identify their User ID.
6. Obtain the generic Pipeline ID required for configuration queries.

## 3. Official documentation used
- Bhashini Developer Portal / API Documentation (Typically hosted at https://bhashini.gov.in/ or https://bhashini.gov.in/ulca).

## 4. Required API configuration
Once credentials are obtained, Bhashini requires a two-step handshake process:
1. **Pipeline Configuration (/ulca/apis/v0/model/getModelsPipeline):** Using the User ID, API Key, and Pipeline ID, the client queries for available services (like TTS) matching the requested languages (hi, sat). This returns a dynamic inference API endpoint and a dynamic inference API Key (Authorization header).
2. **Inference (Dynamic Endpoint):** The client POSTs the base64 payload to the dynamically returned URL, using the dynamic key.

## 5. Required authentication
The configuration request requires the following HTTP headers:
- userID: Your Bhashini User ID
- ulcaApiKey: Your Bhashini API Key

## 6. Pipeline discovery method
To discover Santali TTS support, the JSON payload to the configuration endpoint must specify:
`json
{
    "pipelineTasks": [
        {
            "taskType": "tts",
            "config": {
                "language": {
                    "sourceLanguage": "sat"
                }
            }
        }
    ],
    "pipelineRequestConfig": {
        "pipelineId": "<YOUR_BHASHINI_PIPELINE_ID>"
    }
}
`

## 7. TTS task configuration
The discovery process (if authorized) would yield serviceId mappings for Hindi and Santali, allowing us to route requests to the correct inference compute nodes.

## 8. Santali support result
**BLOCKED.** (Cannot verify dynamically without credentials, though documentation historically indicates support).

## 9. Ol Chiki support result
**BLOCKED.** (Unknown until inference payload structure can be discovered).

## 10. Hindi support result
**BLOCKED.** (Likely highly supported, but strictly blocked without credentials).

## 11. Voice information
**BLOCKED.** (Voices are returned in the configuration response, which cannot be retrieved).

## 12. Whether inference endpoint was reached
**NO.** No inference calls were made.

## 13. Whether audio was generated
**NO.**

## 14. Production files modified
**NONE.**

## 15. Security checks
- Bhashini credentials printed: NO
- Bhashini credentials committed: NO
- Secret values exposed: NO

## 16. Exact next requirement
The project owner must inject legitimate Bhashini developer credentials into the environment variables:
- BHASHINI_USER_ID
- BHASHINI_API_KEY
- BHASHINI_PIPELINE_ID

## 17. Exact next task
**Task 7.11 — Bhashini TTS Backend Integration (Pending Credentials).**
Once keys are supplied, the BhashiniTTSProvider in 	ts_service.py can be fleshed out to perform the 2-step handshake (Discovery -> Inference) and return raw bytes to the /tts endpoint.

---

FINAL DECISION:
**B. BHASHINI CREDENTIALS REQUIRED**
