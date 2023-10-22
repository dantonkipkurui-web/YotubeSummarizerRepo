import os
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
    summarizer = pipeline(task="summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=max_summary_length, min_length=50, do_sample=False)
    return summary[0]['summary_text']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_id = request.form['video_id']
        transcript = get_video_transcript(video_id)

        if transcript:
            summarized_text = summarize_transcript(transcript)
            return render_template('index.html', summarized_text=summarized_text, video_id=video_id)
        else:
            error_message = "Transcript retrieval failed. Check the video ID and try again."
            return render_template('index.html', error_message=error_message)
    return render_template('index.html', summarized_text=None, video_id=None)

if __name__ == "__main__":
    app.run(debug=True)

import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Print the current working directory
    current_directory = os.getcwd()
    print("Current Working Directory:", current_directory)


if __name__ == "__main__":
    app.run(debug=True)

