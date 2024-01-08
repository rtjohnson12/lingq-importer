import urllib.parse
import requests
import os
from dotenv import load_dotenv
from requests_toolbelt.multipart.encoder import MultipartEncoder

load_dotenv()

key = os.environ.get("LINGQ_API_KEY")

headers = {"Authorization": f"Token {key}", "Content-Type": "application/json"}


# via https://github.com/kaajjaak/LingQGPT/blob/master/api_wrappers/lingq_api_wrapper.py
def get_languages():
    response = requests.get("https://www.lingq.com/api/v2/languages", headers=headers)
    return [language for language in response.json() if language["knownWords"] > 0]


def get_contexts():
    # Get contexts from the API
    response = requests.get("https://www.lingq.com/api/v2/contexts", headers=headers)
    return response.json()


def get_lingqs(language_code="es"):
    # Get lingqs from the API
    response = requests.get(
        f"https://www.lingq.com/api/v2/{language_code}/cards/", headers=headers
    )
    return response.json()


def get_courses_by_language(language_code="es"):
    # Get courses from the API
    response = requests.get(
        f"https://www.lingq.com/api/v2/{language_code}/collections/my/", headers=headers
    )
    return response.json()


def get_lessons_by_course(language_code="es", course_id=0):
    # Get lessons from the API
    response = requests.get(
        f"https://www.lingq.com/api/v2/{language_code}/collections/{course_id}",
        headers=headers,
    )
    return response.json()


def get_lesson(language_code="es", lesson_id=0):
    # Get lesson from the API
    response = requests.get(
        f"https://www.lingq.com/api/v2/{language_code}/cards/{lesson_id}",
        headers=headers,
    )
    return response.json()


def get_lingqs_from_lesson(language_code="es", lesson_id=0):
    # Get lingqs from the API
    payload = {"lesson": lesson_id}
    response = requests.get(
        f"https://www.lingq.com/api/v3/{language_code}/lessons/{lesson_id}",
        headers=headers,
    )
    return response.json()


def get_lesson_info(language_code="es", lesson_id=0):
    payload = {"lesson": lesson_id}
    # Get lesson info from the API
    response = requests.get(
        f"https://www.lingq.com/api/v3/{language_code}/lessons/counters",
        headers=headers,
        params=payload,
    )
    return response.json()


def get_lingqs_to_learn(
    language_code="es",
    page_size=100,
    search_criteria="startsWith",
    sort="importance",
    status=[1, 2],
    page=1,
):
    payload = {
        "page": page,
        "page_size": page_size,
        "search_criteria": search_criteria,
        "sort": sort,
        "status": status,
    }
    response = requests.get(
        f"https://www.lingq.com/api/v3/{language_code}/cards",
        headers=headers,
        params=payload,
    )
    return response.json()


def create_collection(title, description, language_code="es", **kwargs):
    payload = {
        "title": title,
        "description": description,
        "hasPrice": False,
        "isFeatured": False,
        "language": language_code,
        "sellAll": False,
        "sourceURLEnabled": False,
        "tags": [],
        **kwargs,
    }
    response = requests.post(
        f"https://www.lingq.com/api/v3/{language_code}/collections/",
        headers=headers,
        json=payload,
    )
    return response.json()


def import_lesson(title, collection_id, language_code="es", level=5, **kwargs):
    payload = {
        "collection": int(collection_id),
        # "description": description,
        # "text": text,
        "language": language_code,
        "save": True,
        "status": "private",
        "title": title,
        "level": int(level),
        **kwargs,
    }

    response = requests.post(
        f"https://www.lingq.com/api/v3/{language_code}/lessons/import/",
        headers=headers,
        json=payload,
    )
    return response.json()


def post_lesson(title, collection_id, language_code="es", level=1, **kwargs):
    payload = {
        "collection": int(collection_id),
        # "description": description,
        # "text": text,
        "language": language_code,
        "save": True,
        "status": "private",
        "title": title,
        "level": int(level),
        **kwargs,
    }

    response = requests.post(
        f"https://www.lingq.com/api/v3/{language_code}/lessons/",
        headers=headers,
        json=payload,
    )
    return response.json()


def create_lesson_in_collection(
    title,
    text,
    collection_id=1288847,
    description="",
    language_code="es",
    level=1,
):
    payload = {
        "collection": int(collection_id),
        "description": description,
        "language": language_code,
        "save": True,
        "status": "private",
        "text": text,
        "title": title,
        "level": int(level),
    }
    response = requests.post(
        f"https://www.lingq.com/api/v3/{language_code}/lessons/",
        headers=headers,
        json=payload,
    )
    return response.json()


def check_word_status(word, language_code="es"):
    payload = {
        "page": 1,
        "page_size": 25,
        "search": word,
        "search_criteria": "startsWith",
        "sort": "alpha"
        # "status": list(range(0, 5))
    }
    response = requests.get(
        f"https://www.lingq.com/api/v3/{language_code}/cards/",
        headers=headers,
        params=payload,
    )
    return response.json()


def create_lesson_in_collection_with_audio(
    title, text, audio_path, image_url, collection_id, language_code="es", level=1
):
    with open(audio_path, "rb") as f:
        audio = f.read()

    data = MultipartEncoder(
        [
            ("title", title),
            ("text", text),
            ("status", "private"),
            ("imageUrl", image_url),
            ("collection", str(collection_id)),
            ("audio", (os.path.basename(audio_path), audio, "audio/mpeg")),
            ("save", "true"),
        ]
    )

    response = requests.post(
        f"https://www.lingq.com/api/v3/{language_code}/lessons/import/",
        data=data,
        headers={"Authorization": f"Token {key}", "Content-Type": data.content_type},
    )

    return response.json()
