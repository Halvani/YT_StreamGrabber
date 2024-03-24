import re
from pytube import YouTube, Playlist
from enum import Enum, auto
from pathlib import Path
from tqdm.auto import tqdm


class StreamType(Enum):
    Audio = auto()
    Video = auto()

def download_yt_stream(url=None, dest_folder=None, stream_type=StreamType.Video):     
    if url is None or len(url.strip()) == 0: 
        url = input()    
    
    if dest_folder is None:
        dest_folder = ""
    else:
        dest_folder = dest_folder.strip()
        if dest_folder != "" and not Path(dest_folder).exists():
            Path(dest_folder).mkdir(parents=True, exist_ok=True)        
               
    try:
        yt = YouTube(url)        
        filename = ""    
        stream = None
        if stream_type == StreamType.Audio:
            stream = yt.streams.get_audio_only()
            filename = re.sub(r"\s{2,}", " ", stream.default_filename.replace(".mp4", ".mp3"))
        elif stream_type == StreamType.Video:
            stream = yt.streams.get_highest_resolution()
            filename = re.sub(r"\s{2,}", " ", stream.default_filename)   
            
        stream.download(filename=Path(dest_folder, filename))      

        return (True, filename)    
    except Exception as e:
        return (False, f"{url} ► could not be downloaded! --> Exception: {e}")


def download_yt_streams(list_of_urls=None, dest_folder=None, stream_type=StreamType.Video):
    if list_of_urls is not None and len(list_of_urls) > 0:
        for url in tqdm(list_of_urls):
            print(download_yt_stream(url, dest_folder=dest_folder, stream_type=stream_type))     
        

def download_yt_streams_from_playlist(playlist_url, dest_folder=None, stream_type=StreamType.Video):
    download_yt_streams(Playlist(playlist_url).video_urls, dest_folder=dest_folder, stream_type=stream_type)