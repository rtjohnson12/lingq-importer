import time
import pandas as pd

from pytubefix import YouTube, Channel
from src.lingq import *
from src.youtube import get_youtube_data


language_code = "es"
courses = get_courses_by_language(language_code=language_code)["results"]
course_titles = [course["title"] for course in courses]

channel_name = "JorgeDeLeonMx"
collection_id = [
    course["id"] for course in courses if course["title"] == f"{channel_name} YouTube"
][0]

existing_lessons = get_lessons_by_course(language_code="es", course_id=collection_id)[
    "lessons"
]

baseline_lesson = existing_lessons[0]
target_lesson = get_lessons_by_course(language_code="es", course_id=1558905)["lessons"][
    0
]

records = get_youtube_data(
    channel_name=channel_name,
    language_code=language_code,
    n_videos=2,
    manual_transcripts_only=True,
    video_ids=["tgQa49TWJIY", "oJEuOi-SFW0"],
)

good_record = records[1]
bad_record = records[0]

good_record["text"]
bad_record["text"]

lessons = get_lessons_by_course(language_code="es", course_id=1558905)["lessons"]

good_lesson = lessons[0]
bad_lesson = lessons[1]

for key in [
    # "id",
    # "collectionTitle",
    # "url",
    "originalUrl",
    # "imageUrl",
    # "title",
    # "originalImageUrl",
    # "providerImageUrl",
    # "description",
    "duration",
    "audio",
    # "audioPending",
    # "level",
    "metadata",
    # "external_type",
    # "type",
    # "status",
    "tags",
]:
    print(f"{key}: {good_lesson[key]} vs {bad_lesson[key]}")

records = get_youtube_data(
    channel_name=channel_name,
    language_code=language_code,
    n_videos=2,
    manual_transcripts_only=True,
)

test_collection_id = int(1558905)
record = bad_record


response_json = import_lesson(
    title=record["title"],
    description=record["description"],
    collection_id=test_collection_id,
    url=record["url"],
    language_code="es",
    source="Chrome",
    level=5,
    external_image=record["thumbnail"],
    extra={"ytpage": requests.get(record["url"]).text, "ytdebug": False},
)

record[""]

out2 = post_lesson(
    title=record["title"],
    description=record["description"],
    text=record["text"].replace("\xa0", ""),
    url=record["url"],  # originalUrl=record["url"],
    collection_id=test_collection_id,
    metadata={"import_method": "Lesson"},
    level=5,
)

response_json["collection"]
lessons = get_lessons_by_course(language_code="es", course_id=test_collection_id)[
    "lessons"
]
len(lessons)

print("Baseline vs Target vs Test")
for key in [
    # "id",
    # "collectionTitle",
    # "url",
    "originalUrl",
    # "imageUrl",
    "title",
    # "originalImageUrl",
    # "providerImageUrl",
    # "description",
    # "duration",
    # "audio",
    # "audioPending",
    "level",
    "metadata",
    # "external_type",
    # "type",
    # "status",
    # "tags",
]:
    print(
        f"{key}: {baseline_lesson[key]} vs {target_lesson[key]} vs {response_json[key]}"
    )


lessons = [
    lesson
    for lesson in existing_lessons
    if lesson["title"] in ["El Cielo: The lung of northeastern Mexico"]
]
