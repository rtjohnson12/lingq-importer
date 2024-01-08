import os
import requests
from tqdm import tqdm
import pandas as pd

# from moviepy.editor import AudioFileClip
from pytubefix import YouTube, Channel, Search
from youtube_transcript_api import YouTubeTranscriptApi


def get_video_transcript(video_id, language_code="es", manually_created=True):
    if language_code == "es":
        language_codes = ["es", "es-419"]
    else:
        language_codes = [language_code]
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    if manually_created:
        try:
            transcript = transcript_list.find_manually_created_transcript(
                language_codes
            )
        except:
            print(f"No Manually Created Transcript Available for {video_id}")
            return None
    else:
        try:
            transcript = transcript_list.find_manually_created_transcript(
                language_codes
            )
        except:
            transcript = transcript_list.find_generated_transcript(language_codes)

    raw_json = transcript.fetch()

    df = pd.json_normalize(raw_json)
    df["text"] = [s.replace("\n", " ") for s in [x["text"] for x in raw_json]]
    df["word_count"] = df["text"].apply(lambda x: len(x.split()))
    df["cum_word_count"] = df["word_count"].cumsum()

    return df


def MP4toMP3(filename, delete=False):
    FILETOCONVERT = AudioFileClip(filename)
    FILETOCONVERT.write_audiofile(filename.replace(".mp4", ".mp3"))
    FILETOCONVERT.close()

    if delete:
        os.remove(filename)


# if not os.path.isfile(f"audio/{record['title'].replace(':','')}.mp3"):
#     MP4toMP3(f"audio/{record['title'].replace(':','')}.mp4", delete=False)


def get_youtube_data(
    channel_name="CasoCerrado",
    language_code="es",
    ignore_titles=[],
    n_videos=100,
    manual_transcripts_only=True,
    video_ids=None,
):
    # channel = Channel(f"https://www.youtube.com/c/{channel_name}/videos")
    channel = Channel(f"https://www.youtube.com/@{channel_name}")
    results = []
    yts = []
    if video_ids:
        for video_id in tqdm(video_ids):
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            yts.append(yt)
    else:
        for video in channel.videos[:n_videos]:
            yt = YouTube(video.watch_url)
            yts.append(yt)
    for yt in tqdm(yts):
        if yt.title in ignore_titles:
            continue
        if not "captions" in yt.vid_info:
            try:
                yt.bypass_age_gate()
            except Exception as e:
                next
        captions = yt.captions
        for caption in captions:
            if language_code in caption.code and (
                caption.code != f"a.{language_code}" or not manual_transcripts_only
            ):
                # transcript_df = get_video_transcript(
                #     yt.video_id,
                #     manually_created=manual_transcripts_only,
                #     language_code=language_code,
                # )
                results.append(
                    {
                        "title": yt.title,
                        "url": f"https://www.youtube.com/watch?v={yt.video_id}",
                        "thumbnail": yt.thumbnail_url,
                        # "text": " ".join(transcript_df["text"]),
                        # "text_df": transcript_df,
                        "description": yt.description.replace("\n", ""),
                    }
                )
                # yt.streams.filter(only_audio=True).first().download("audio/")

                # MP4toMP3(f"audio/{yt.title.replace(':','').replace('\'', '')}.mp4", delete=True)
                break
    return results


# video_id = "nJsi4lMhRos"
# yt = YouTube(f"https://youtube.com/watch?v={video_id}")
# get_video_transcript(video_id)

# result = []
# for video_url in videos:
#     video_id = video.replace('https://youtube.com/watch?v=', '')
#     transcript = get_video_transcript(video_id)
#     transcript[]
