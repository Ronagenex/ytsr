from transcription import fetch_transcript
from transcription import speech_to_text
from features import get_vid_data
from features import fetch_translated_text
from features import ttspeech

global transcript
transcript=""

def get_transcript(video_link):
    global transcript
    transcript=""
    try:
        transcript= fetch_transcript(video_link).capitalize()
        return transcript
    except Exception as e:
        return f"Error during transcription : {e}"

def translate_transcript(transcript,lang_choice):
    try :
        return fetch_translated_text(transcript,lang_choice).capitalize()
        
    except Exception as e:
       return f"Error during translation : {e}"
    
def get_data(link):
    try :
        data=get_vid_data(link)
        title=data['Title']
        duration=data['Duration']
        description=data['Description']
    except Exception as e:
        return f"Error during fetching video data : {e}"
    
def audio_to_text(link="",audio_file=True):
    try :
        return speech_to_text("",True)
    except Exception as e:
        return f"Error during speech to text : {e}"
    
def text_to_speech(text,language):
    try :
        tts=ttspeech(text,language)
    except Exception as e:
        return f"Error during text to speech : {e}"

def summarize_transcript():
    pass        

