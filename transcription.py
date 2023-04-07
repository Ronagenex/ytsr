from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptAvailable, NoTranscriptFound, VideoUnavailable 
from googletrans import LANGUAGES
import whisper
from pytube import YouTube
import warnings

# Suppress FP16 warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

def eng_aliases():
    # Add aliases for English languages

    LANGUAGES['en-us']='English'
    LANGUAGES['en-US']='English'
    LANGUAGES['en-gb']='English'
    LANGUAGES['en-GB']='English'

def fetch_transcript(video_link):
    """Fetches the transcript for a given YouTube video link.

    Args:
        video_link (str): A string containing the YouTube video link.

    Returns:
        str: A string containing the video's transcript, or an error message if the transcript cannot be found or generated.
    """

    # Extract the video ID from the video_link
    video_id = video_link.split('=')[1]
    transcript=""
    eng_aliases()

    try:
        # Try to find a manually created transcript in English or American English
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        manual_transcript = transcript_list.find_manually_created_transcript(LANGUAGES.keys())
        if manual_transcript.language_code.lower() not in ['en','en-us','en-gb']:
            transcript=manual_transcript.translate('en')
        else:
            transcript = manual_transcript    

    except NoTranscriptFound:
        try:
            auto_gen_transcript= transcript_list.find_generated_transcript(LANGUAGES.keys())
            if auto_gen_transcript.language_code.lower() not in ['en','en-us','en-gb']:
                transcript=auto_gen_transcript.translate('en')
            else:
                transcript = auto_gen_transcript   

        except:
            return speech_to_text(video_link)
    
    except VideoUnavailable:
        return "Video not found, enter a valid youtube video link"
    
    except (TranscriptsDisabled, NoTranscriptAvailable):
        # If no transcripts are available, perform speech recognition to obtain transcript
        return speech_to_text(video_link)
    

    try:
        transcript_text = " ".join([item['text'] for item in transcript.fetch()]).replace("\n"," ")
        return transcript_text  
    
    except Exception as e:
        return e
    
def speech_to_text(video_link,has_audio_file=False):
    """
    Downloads the audio from a YouTube video and transcribes it using the whisper library.
    
    Args:
        video_link (str): The link to the YouTube video from which to extract audio.
        
    Returns:
        str: The transcribed text from the audio.
        
    """
    if not has_audio_file:
        try :
            yt = YouTube(video_link)
        except:
            return 'Link Error'    
        yt.streams.filter(file_extension='mp3')
        stream = yt.streams.get_by_itag(139)
        stream.download('', "audio_file.mp3")

    model = whisper.load_model("base")
    result = model.transcribe("audio_file.mp3")
    return result['text']   
   
