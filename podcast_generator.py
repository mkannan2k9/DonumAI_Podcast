import os
import time
import json
import requests
from flask import Flask
from gtts import gTTS
from google import genai
from google.genai import types

GOOGLE_API_KEY = "GOOGLE-API-KEY"
PODBEAN_CLIENT_ID = "PODBEAN-CLIENT-ID"
PODBEAN_CLIENT_SECRET = "PODBEAN-CLIENT-SECRET"

TEXT_MODEL = "gemini-2.5-flash-lite" 

app = Flask(__name__)
client = genai.Client(api_key=GOOGLE_API_KEY)

def generate_simple(model, prompt):
    try:
        response = client.models.generate_content(model=model, contents=prompt)
        return response.text
    except Exception as e:
        print(f"Simple generation failed: {e}")
        return ""

@app.route('/trigger/hello')
def trigger_podcast():
    topics_file = os.path.join(os.path.dirname(__file__), 'topicsandsubjects.txt')
    seen_topics = set()

    if os.path.exists(topics_file):
        with open(topics_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().lower().startswith("Topic:"):
                    t = line.partition(":")[2].strip().lower()
                    seen_topics.add(t)

    topic = None
    subject = None

    for attempt in range(5):
        print(f"Generating topic... (Attempt {attempt + 1})")

        topic_prompt = f"""
        Generate a unique educational topic and subject.
        Output strictly in JSON format like this:
        {{"topic": "The French Revolution", "subject": "History"}}
        """

        try:
            response = client.models.generate_content(
                model=TEXT_MODEL,
                contents=topic_prompt,
                config=types.GenerateContentConfig(
                    temperature=1.0,
                    response_mime_type='application/json'
                )
            )

            data = json.loads(response.text)
            temp_topic = data.get("topic")
            temp_subject = data.get("subject")

            if temp_topic and temp_subject:
                if temp_topic.lower() not in seen_topics:
                    topic = temp_topic
                    subject = temp_subject

                    with open(topics_file, "a", encoding="utf-8") as f:
                        f.write(f"\n\nTopic: {topic}\nSubject: {subject}")
                    break
                else:
                    print(f"Duplicate: {temp_topic}")
            else:
                print("JSON missing keys")
        except Exception as e:
            print(f"Topic generation failed: {e}")
            time.sleep(2)

    if not topic:
        return "Failed to generate unique topic."

    print(f"Selected Topic: {topic}")

    lesson_prompt = f"""
    Write a podcast script.
    Topic: {topic} | Subject: {subject}
    Style: Storytelling, Grade 6 level, 300 words. Plain text only.
    """
    lesson_text = generate_simple(TEXT_MODEL, lesson_prompt)
    if not lesson_text: return "Failed to generate script."

    try:
        clean_text = lesson_text.replace("**", "").replace("##", "")
        tts_obj = gTTS(text=clean_text, lang='en', slow=False)
        tts_obj.save("welcome.mp3")
    except Exception as e:
        print(f"TTS failed: {e}")
        return "TTS Generation Failed"

    meta_prompt = f"""
    Write a title and description.
    Topic: {topic}
    Output strictly in JSON format like this:
    {{"title": "The Title Here", "description": "The description here."}}
    """

    try:
        meta_resp = client.models.generate_content(
            model=TEXT_MODEL,
            contents=meta_prompt,
            config=types.GenerateContentConfig(response_mime_type='application/json')
        )
        meta_data = json.loads(meta_resp.text)
        ep_title = meta_data.get("title", f"{topic} Episode")
        ep_desc = meta_data.get("description", "Listen now.")
    except Exception as e:
        print(f"Meta gen failed: {e}")
        ep_title = f"{topic} Episode"
        ep_desc = "Listen now."

    MODE = "PROD"
    if MODE == "PROD":
        try:
            token_resp = requests.post(
                "https://api.podbean.com/v1/oauth/token",
                data={"grant_type": "client_credentials", "client_id": PODBEAN_CLIENT_ID, "client_secret": PODBEAN_CLIENT_SECRET}
            )
            token_data = token_resp.json()
            access_token = token_data.get("access_token")

            if access_token:
                file_size = os.path.getsize("welcome.mp3")
                auth_resp = requests.get(
                    "https://api.podbean.com/v1/files/uploadAuthorize",
                    params={'access_token': access_token, 'filename': 'welcome.mp3', 'filesize': file_size, 'content_type': 'audio/mpeg'}
                )
                auth_data = auth_resp.json()

                with open("welcome.mp3", "rb") as f:
                    requests.put(auth_data["presigned_url"], data=f, headers={'Content-Type': 'audio/mpeg'})

                requests.post(
                    "https://api.podbean.com/v1/episodes",
                    headers={"Authorization": f"Bearer {access_token}"},
                    json={
                        "title": ep_title, "content": ep_desc, "status": "publish", "type": "public", "media_key": auth_data["file_key"]
                    }
                )
            else:
                print("Failed to get Podbean token")
        except Exception as e:
            print(f"Podbean upload failed: {e}")

    return "ok"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
