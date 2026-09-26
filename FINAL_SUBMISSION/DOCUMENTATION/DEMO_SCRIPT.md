# DEMO SCRIPT

"Hello everyone. Today, we're presenting MatriVaani—an AI-powered vernacular pedagogy tool designed to bridge the educational gap for tribal students in India. 

Many students growing up in remote areas speak languages like Ho or Santali, yet their educational materials and teachers primarily operate in Hindi. MatriVaani solves this by bringing AI directly into the classroom.

Let’s look at Demo 1. Here, a teacher wants to translate a Hindi phrase into Santali. Using our Flutter application, they select Hindi as the source and Santali as the target. They input the phrase: 'नमस्ते बच्चों, आज हम गिनती सीखेंगे।' (Namaste bacchon, aaj hum ginti seekhenge). The app queries our hybrid backend, leverages the IndicTrans2 model, and provides a highly accurate Santali translation, even supporting audio playback where configured.

Now, for Demo 2. Imagine a student speaking in Ho. Ho is a severely under-resourced language. We have developed and integrated a fine-tuned, offline Wav2Vec2 model specifically for Ho speech recognition. When the student speaks into the app, our backend processes the speech locally, without needing the cloud, and outputs the exact Ho transcript in Devanagari or Warang Citi script. While Ho translation is not yet available in this prototype due to the lack of parallel datasets, accurately transcribing Ho speech offline is a monumental first step for rural classrooms.

Finally, in Demo 3, we can reverse the flow—taking Santali input from the student and seamlessly translating it back into Hindi for the teacher. 

MatriVaani’s architecture is hybrid by design. It runs heavy translation workloads securely via WSL and cloud providers, while pushing crucial, low-resource tasks like Ho ASR directly to the edge, keeping it robust even in disconnected rural schools. 

Thank you."
