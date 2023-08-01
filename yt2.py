import os
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

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

if __name__ == "__main__":
    video_id = input("Enter the YouTube video ID: ")
    transcript = get_video_transcript(video_id)

    if transcript:
        summarized_text = summarize_transcript(transcript)
        print("\nSummarized Transcript:")
        print(summarized_text)
    else:
        print("Transcript retrieval failed. Check the video ID and try again.")
