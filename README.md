# AI Podcast Generator



An automated podcast production tool that generates educational scripts, converts them to audio, creates episode metadata, and publishes directly to Podbean—all powered by Google Gemini AI.

**Owner:** Kannan Murugapandian  
**License:** MIT



## Features

- **Automated Topic Discovery:** Generates unique, educational topics (e.g., History, Science) using AI, ensuring no duplicates from previous runs.
- **Script Generation:** Writes a complete storytelling-style script suitable for a Grade 6 audience using **Gemini 2.5 Flash-Lite**.
- **Audio Production:** Converts the script into an MP3 file using Google Text-to-Speech (gTTS).
- **Metadata Creation:** Automatically generates an engaging title and description for the episode.
- **Auto-Publishing:** Uploads the audio and publishes the episode directly to your **Podbean** hosting account via API.



## Requirements

- Python 3.8+
- **Google Gemini API Key**
- **Podbean API Credentials** (Client ID & Secret)
- Python Packages:
  - `Flask`
  - `google-genai`
  - `gTTS`
  - `requests`



## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mkannan2k9/DonumAI_Podcast.git
   cd ai-podcast-generator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Or manually:*
   ```bash
   pip install Flask google-genai gTTS requests
   ```

3. **Configure Credentials:**
   Open `podcast_generator.py` and update the following constants:
   ```python
   GOOGLE_API_KEY = "AIzaSy..." 
   PODBEAN_CLIENT_ID = "Your_Podbean_ID"
   PODBEAN_CLIENT_SECRET = "Your_Podbean_Secret"
   ```

4. **Verify Files:**
   Ensure `topicsandsubjects.txt` exists in the root directory (or let the script create it). This file tracks used topics to prevent repetition.



## Usage

1. **Run the application:**
   ```bash
   python podcast_generator.py
   ```

2. **Trigger Production:**
   To produce and publish a new episode, visit the trigger endpoint:
   ```
   http://localhost:5001/trigger/hello
   ```

### What happens when triggered?
1.  **Topic Gen:** The AI selects a new topic (e.g., "The French Revolution").
2.  **Scripting:** A 300-word educational script is written.
3.  **TTS:** The script is converted to `welcome.mp3`.
4.  **Metadata:** A title and description are generated.
5.  **Publishing:** The file is uploaded to Podbean and published live.



## Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/trigger/hello` | GET | Triggers the full production pipeline (Topic -> Script -> Audio -> Publish). |



## Configuration

- **Models:** Uses `gemini-2.5-flash-lite` for text generation.
- **Voice:** Uses `gTTS` (default English). You can modify the `lang` parameter in the `trigger_podcast` function to change the accent/language.
- **History:** To reset the topic history, simply delete or clear `topicsandsubjects.txt`.



## License

MIT License

Copyright (c) 2025 Kannan Murugapandian

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



## Acknowledgements

- [Google Gemini API](https://ai.google.dev/)
- [Podbean API](https://developers.podbean.com/)
- [gTTS](https://pypi.org/project/gTTS/)



**For questions or support, contact Kannan Murugapandian.**
