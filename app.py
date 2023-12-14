import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from flask import Flask, render_template, request

app = Flask(__name__)


def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text_parts = [t['text'] for t in transcript]
        return ' '.join(text_parts)
    except Exception as e:
        print("Error fetching transcript:", e)
        return None


def summarize_transcript(text, max_summary_length=100):
    summarizer = pipeline(task="summarization",
                          model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=max_summary_length,
                         min_length=50, do_sample=False)
    return summary[0]['summary_text']


def extract_video_id(url_or_id):
    if 'youtube.com/watch?v=' in url_or_id or 'youtu.be/' in url_or_id:
        # Extract the video ID from the URL using a regular expression
        match = re.search(r'(?:v=|youtu\.be/)([^&]+)', url_or_id)
        return match.group(1) if match else None
    else:
        # Assume it's already a video ID
        return url_or_id


@app.route('/', methods=['GET', 'POST'])
def index():
    summarized_text = None
    error_message = None
    video_id_input = None # Initialize video_id_input to none to enable first GET request

    if request.method == 'POST':
        video_id_input = request.form['video_id']
        video_id = extract_video_id(video_id_input)

        if video_id:
            transcript = get_video_transcript(video_id)
            if transcript:
                summarized_text = summarize_transcript(transcript)
            else:
                error_message = "Transcript retrieval failed. Check the video ID/URL and try again."
        else:
            error_message = "Invalid YouTube URL or ID. Please check and try again."

    return render_template('index.html', summarized_text=summarized_text, error_message=error_message, video_id=video_id_input)


if __name__ == "__main__":
    app.run(debug=True)
