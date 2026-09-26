# MatriVaani Educational Translation Vocabulary

Because MatriVaani targets **Mother Tongue-Based Primary Education**, generic translation accuracy is secondary to precise pedagogical translation.

The following categories outline the strict vocabulary domains that must be covered by verified Hindi-Santhali parallel pairs before we can deploy MatriVaani in a classroom setting.

## 1. Foundational Literacy and Numeracy (FLN)
- **Numbers (1-100)**: "एक", "दो", "दस", "बीस" -> (Santhali equivalents)
- **Basic Shapes**: Circle, Square, Triangle
- **Colors**: Red, Blue, Green, Yellow, Black, White
- **Phonics**: Reading instructions (e.g., "इसे पढ़ो", "जोर से बोलो")

## 2. Classroom Instructions & Commands
- "बच्चों, अपनी किताब खोलो।" (Children, open your books.)
- "कृपया शांत रहें।" (Please be quiet.)
- "बोर्ड पर देखो।" (Look at the board.)
- "बैठ जाओ।" (Sit down.)
- "खड़े हो जाओ।" (Stand up.)
- "यहाँ आओ।" (Come here.)

## 3. Basic Questions and Assessments
- "क्या तुम्हें समझ आया?" (Did you understand?)
- "इसका उत्तर कौन देगा?" (Who will answer this?)
- "तुम्हारा नाम क्या है?" (What is your name?)
- "यह क्या है?" (What is this?)

## 4. Environment & Daily Life
- **Animals**: Dog, Cat, Cow, Elephant, Bird
- **Nature**: Sun, Moon, Water, Tree, River
- **Family**: Mother, Father, Brother, Sister, Teacher
- **Body Parts**: Head, Hand, Leg, Eye, Nose, Ear

## Verification Protocol
All vocabulary terms listed above must be explicitly translated and vetted by a native Santhali speaker/educator. We will construct a unit test suite (`tests/test_nmt_vocabulary.py`) that asserts the translation of these exact Hindi terms matches the verified Santhali target.

**Status**: Awaiting verified parallel data mapping for these concepts.
