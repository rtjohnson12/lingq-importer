import time
import pandas as pd
import argparse

from pytubefix import YouTube, Channel
from src.lingq import *
from src.youtube import get_youtube_data

parser = argparse.ArgumentParser("LingQ-Importer")
parser.add_argument("-n", default=50)
parser.add_argument("--manual-only", default=True)

args = parser.parse_args()


def run(
    channel_name="JorgeDeLeonMx",
    language_code="es",
    n_videos=50,
    manual_transcripts_only=True,
):
    channel = Channel(f"https://www.youtube.com/@{channel_name}/videos")
    courses = get_courses_by_language(language_code=language_code)["results"]

    if f"{channel_name} YouTube" not in [course["title"] for course in courses]:
        print(f"Creating New LingQ Course: `{channel_name} YouTube`")
        new_collection = create_collection(
            title=f"{channel_name} YouTube",
            description=f"[YouTube Transcripts and Audio taken from @{channel_name}] \n\n{channel.description}".replace(
                "\n", ""
            ),
            language_code=language_code,
            # sourceURL=channel.channel_url,
        )

        collection_id = new_collection["id"]
    else:
        print(f"Using Existing LingQ Course: `{channel_name} YouTube`")
        collection_id = [
            course["id"]
            for course in courses
            if course["title"] == f"{channel_name} YouTube"
        ][0]

    existing_lessons = get_lessons_by_course(
        language_code="es", course_id=collection_id
    )["lessons"]

    existing_titles = [lesson["title"] for lesson in existing_lessons]
    records = get_youtube_data(
        channel_name=channel_name,
        language_code=language_code,
        n_videos=n_videos,
        ignore_titles=existing_titles,
        manual_transcripts_only=manual_transcripts_only,
    )

    for record in records:
        if not record["title"] in existing_titles:
            response_json = import_lesson(
                title=record["title"],
                description=record["description"],
                collection_id=collection_id,
                url=record["url"],
                language_code="es",
                level=5,
                extra={"ytpage": requests.get(record["url"]).text, "ytdebug": False},
            )

            print(f"Uploaded Video `{response_json['title']}`")
        time.sleep(1)


if __name__ == "__main__":
    youtube_channels = [
        "JorgeDeLeonMx",
        "CasoCerrado",
        "EasySpanish",
        "31minutos",
        "noticias",
        "DreamingSpanish",
        "CoreanoVlogs",
    ]

    for youtube_channel in youtube_channels:
        run(
            youtube_channel,
            n_videos=args.n,
            language_code="es",
            manual_transcripts_only=False,
        )
