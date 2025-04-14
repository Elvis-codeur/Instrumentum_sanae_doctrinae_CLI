"""
This file contain all the constants needed in the project. 

Variables
---------
- `MONERGISM_NAME` : The name of https://www.monergism.com/ everywhere I want to use it. It will be used to \
    create folders and many others things related for metadata, download, etc from https://www.monergism.com/
- `MONERGISM_ROOT_FOLDER` : The root folder for everthing that relates to monergism. The logs of monergism \
    is are in the subfolder monergism of the folder log. The metadata of the monergism is in the subfolder \
    monergism of metatdata. 

- `SERMONINDEX_NAME` : The name of https://www.sermonindex.net/ everywhere I want to use it. It will be used to \
    create folders and many others things related for metadata, download, etc from https://www.sermonindex.net/
- `SERMONINDEX_ROOT_FOLDER` : The root folder for everthing that relates to sermonindex. The logs of sermonindex \
    is are in the subfolder sermonindex of the folder log. The metadata of the sermonindex is in the subfolder \
    sermonindex of metatdata.


The folder system of each sermonindex and monergism
---------------------------------------------------
The file system inside the folder of each web site follows the hierarchy given in the web site.

For example, there is the navbar of sermonindex:

- Home
- About Us
- Audio Sermons
  - by Speaker
  - by Topic
  - by Scripture
  -  by Podcast
- Text Sermons
  - Christian Books
  - Online Bibles
- Video Sermons
- Vintage Images
- Discussion Forum
- Contact Us
- Giving

I focus only on the Audio Sermons and on the Text Sermons. In every folder of monergism, the first subfolders will be 
**audio_sermons** and **text_sermons**. I prefer to use _ instead of space. 

"""

import os 
import pathlib




WEB_SCRAPING_NAME = "web_scraping"
WEB_SCRAPING_ROOT_FOLDER = "web_scraping"

TELEGRAM_NAME = "telegram"
TELEGRAM_ROOT_FOLDER = "telegram"

YOUTUBE_NAME = "youtube"
YOUTUBE_ROOT_FOLDER = "youtube"



LOGS_ROOT_FOLDER = "log" #: The root folder for log files 
METADATA_ROOT_FOLDER = "metadata" #: The root folder for metadata files 
DOWNLOAD_ROOT_FOLDER = "download" #: The root folder for metadata files 

MAIN_INFORMATION_ROOT_FOLDER = "main_information"
WORK_INFORMATION_ROOT_FOLDER = "work"


BY_SPEAKER_ROOT_FOLDER = "by_speaker"
SPEAKER_NAME = "speaker"

BY_CHRISTIANBOOK_ROOT_FOLDER = "by_christian_book"
CHRISTIANBOOK_NAME = "christian_book"

BY_TOPIC_ROOT_FOLDER = "by_topic"
TOPIC_NAME = "topic"

BY_PODCAST_ROOT_FOLDER = "by_podcast"
PODCAST_NAME = "podcast"

BY_SCRIPTURE_ROOT_FOLDER = "by_scripture"
SCRIPTURE_NAME = "scripture"

BY_SERIES_ROOT_FOLDER = "by_serie"
SERIE_NAME = "serie"




#: The variables of sermonindex 
#: ================================


SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER = "_list"
GENERAL_INFORMATION_NAME = "_general_information"
SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER = "_work"
SPEAKER_TOPIC_OR_SCRIPTURE_DOWNLOAD_FOLDER = "_download"

SERMONINDEX_NAME = "sermonindex" #: The name of sermonindex
SERMONINDEX_ROOT_FOLDER = "sermonindex" #: The root folder for sermonindex
SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER = "audio_sermon" #: The metadata, downloads of the **Audio Sermons** will be here. For the logs, they will be in the **Audio Sermons** of the log folder  
                                                        #: The downloads will be the in the **audio_sermons** of the download folder 
SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER = "text_sermon"  #: The metadata, downloads of the **Text Sermons** will be here. For the logs, **Text Sermons** they will be in the  of the log folder  
SERMONINDEX_VIDEO_SERMONS_ROOT_FOLDER = "video_sermon"  #: The metadata, downloads of the **Text Sermons** will be here. For the logs, **Text Sermons** they will be in the  of the log folder  
SERMONINDEX_VINTAGE_IMAGE_ROOT_FOLDER = "vintage_image"  #: The metadata, downloads of the **Text Sermons** will be here. For the logs, **Text Sermons** they will be in the  of the log folder  

SERMONINDEX_CHRISTIAN_BOOKS_ROOT_FOLDER = "christian_book" #: The metadata, download of the **Christian books** will be in this subfolder of :data:`SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER`
SERMONINDEX_CHRISTIAN_BOOKS_NAME =  "christian_book" #: The metadata, download of the **Christian books** will be in this subfolder of :data:`SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER`
SERMONINDEX_ONLINE_BIBLES_ROOT_FOLDER = "online_bible" #: The metadata, download of the **Online Bibles** will be in this folder
 
SERMONINDEX_VIDEO_SERMONS_ROOT_FOLDER = "video_sermon"  #: The metadata, download of the **Video Sermons** will be in this folder

SERMONINDEX_AUDIO = "audio"
SERMONINDEX_TEXT = "text"
SERMONINDEX_VIDEO = "video"
SERMONINDEX_VINTAGE_IMAGE = "vintage_image"

SERMONINDEX_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(LOGS_ROOT_FOLDER,WEB_SCRAPING_NAME,SERMONINDEX_ROOT_FOLDER)).as_posix() #: The folder where all the log files related to sermonindex will be stored
SERMONINDEX_METADATA_ROOT_FOLDER = pathlib.Path(os.path.join(METADATA_ROOT_FOLDER,WEB_SCRAPING_NAME,SERMONINDEX_ROOT_FOLDER)).as_posix() #: The folder where all the metadata files related to **sermonindex** will be stored
SERMONINDEX_DOWNLOAD_ROOT_FOLDER = pathlib.Path(os.path.join(DOWNLOAD_ROOT_FOLDER,WEB_SCRAPING_NAME,SERMONINDEX_ROOT_FOLDER)).as_posix() #: The folder where all the download(pdf, mp3, mp4, .. ) files related to **sermonindex** will be stored

# The root folders for the logs of sermonindex 

# For the audio sermons
SERMONINDEX_AUDIO_SERMONS_BY_SPEAKER_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_LOG_ROOT_FOLDER,SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,BY_SPEAKER_ROOT_FOLDER)).as_posix() #: The folder where all the **logs** of **Speakers** of **sermonindex** will be stored
SERMONINDEX_AUDIO_SERMONS_BY_TOPIC_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_LOG_ROOT_FOLDER,SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,BY_TOPIC_ROOT_FOLDER)).as_posix() #: The folder where all the **logs** of **Topics** of **sermonindex** will be stored
SERMONINDEX_AUDIO_SERMONS_BY_SCRIPTURE_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_LOG_ROOT_FOLDER,SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,BY_SCRIPTURE_ROOT_FOLDER)).as_posix() #: The folder where all the **logs** of **Scriptures** of **sermonindex** will be stored
SERMONINDEX_AUDIO_SERMONS_BY_PODCAST_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_LOG_ROOT_FOLDER,SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,BY_PODCAST_ROOT_FOLDER)).as_posix() #: The folder where all the **logs** of **Podcasts** of **sermonindex** will be stored

# For the text sermons
SERMONINDEX_TEXT_SERMONS_CHRISTIAN_BOOKS_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_LOG_ROOT_FOLDER,SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER,SERMONINDEX_CHRISTIAN_BOOKS_ROOT_FOLDER)).as_posix() #: The folder where all the **logs** of **Podcasts** of **sermonindex** will be stored
SERMONINDEX_TEXT_SERMONS_ONLINE_BIBLES_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_LOG_ROOT_FOLDER,SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER,SERMONINDEX_ONLINE_BIBLES_ROOT_FOLDER)).as_posix() #: The folder where all the **logs** of **Podcasts** of **sermonindex** will be stored


# The root folder for the metadata of sermonindex 


# For the audio sermons
SERMONINDEX_AUDIO_SERMONS_BY_SPEAKER_METADATA_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_METADATA_ROOT_FOLDER,SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,BY_SPEAKER_ROOT_FOLDER)).as_posix() #: The folder where all the **metadata** of **Speakers** of **sermonindex** will be stored
SERMONINDEX_AUDIO_SERMONS_BY_TOPIC_METADATA_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_METADATA_ROOT_FOLDER,SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,BY_TOPIC_ROOT_FOLDER)).as_posix() #: The folder where all the **metadata** of **Topics** of **sermonindex** will be stored
SERMONINDEX_AUDIO_SERMONS_BY_SCRIPTURE_METADATA_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_METADATA_ROOT_FOLDER,SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,BY_SCRIPTURE_ROOT_FOLDER)).as_posix() #: The folder where all the **metadata** of **Scriptures** of **sermonindex** will be stored
SERMONINDEX_AUDIO_SERMONS_BY_PODCAST_METADATA_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_METADATA_ROOT_FOLDER,SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,BY_PODCAST_ROOT_FOLDER)).as_posix() #: The folder where all the **metadata** of **Podcasts** of **sermonindex** will be stored

# For the text sermons
SERMONINDEX_TEXT_SERMONS_CHRISTIAN_BOOKS_METADATA_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_METADATA_ROOT_FOLDER,SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER,SERMONINDEX_CHRISTIAN_BOOKS_ROOT_FOLDER)).as_posix() #: The folder where all the **metadata** of **Podcasts** of **sermonindex** will be stored
SERMONINDEX_TEXT_SERMONS_ONLINE_BIBLES_METADATA_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_METADATA_ROOT_FOLDER,SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER,SERMONINDEX_ONLINE_BIBLES_ROOT_FOLDER)).as_posix() #: The folder where all the **metadata** of **Podcasts** of **sermonindex** will be stored


# The root folder for the download of sermonindex 

# For the audio sermons
SERMONINDEX_AUDIO_SERMONS_BY_SPEAKER_DOWNLOAD_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_DOWNLOAD_ROOT_FOLDER,SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,BY_SPEAKER_ROOT_FOLDER)).as_posix() #: The folder where all the **downloads** of **Speakers** of **sermonindex** will be stored
SERMONINDEX_AUDIO_SERMONS_BY_TOPIC_DOWNLOAD_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_DOWNLOAD_ROOT_FOLDER,SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,BY_TOPIC_ROOT_FOLDER)).as_posix() #: The folder where all the **downloads** of **Topics** of **sermonindex** will be stored
SERMONINDEX_AUDIO_SERMONS_BY_SCRIPTURE_DOWNLOAD_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_DOWNLOAD_ROOT_FOLDER,SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,BY_SCRIPTURE_ROOT_FOLDER)).as_posix() #: The folder where all the **downloads** of **Scriptures** of **sermonindex** will be stored
SERMONINDEX_AUDIO_SERMONS_BY_PODCAST_DOWNLOAD_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_DOWNLOAD_ROOT_FOLDER,SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,BY_PODCAST_ROOT_FOLDER)).as_posix() #: The folder where all the **downloads** of **Podcasts** of **sermonindex** will be stored

# For the text sermons
SERMONINDEX_TEXT_SERMONS_CHRISTIAN_BOOKS_DOWNLOAD_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_DOWNLOAD_ROOT_FOLDER,SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER,SERMONINDEX_CHRISTIAN_BOOKS_ROOT_FOLDER)).as_posix() #: The folder where all the **downloads** of **Podcasts** of **sermonindex** will be stored
SERMONINDEX_TEXT_SERMONS_ONLINE_BIBLES_DOWNLOAD_ROOT_FOLDER = pathlib.Path(os.path.join(SERMONINDEX_DOWNLOAD_ROOT_FOLDER,SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER,SERMONINDEX_ONLINE_BIBLES_ROOT_FOLDER)).as_posix() #: The folder where all the **downloads** of **Podcasts** of **sermonindex** will be stored








#: The variables of monergism 
#: ================================

MONERGISM_NAME = "monergism" #: The name of the monergism
MONERGISM_ROOT_FOLDER = "monergism" #: The root folder for monergism
MONERGISM_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(LOGS_ROOT_FOLDER,WEB_SCRAPING_ROOT_FOLDER,MONERGISM_ROOT_FOLDER)).as_posix() #: The folder where all the log files related to monergism will be stored
MONERGISM_METADATA_ROOT_FOLDER = pathlib.Path(os.path.join(METADATA_ROOT_FOLDER,WEB_SCRAPING_ROOT_FOLDER,MONERGISM_ROOT_FOLDER)).as_posix() #: The folder where all the metadata files related to monergism will be stored
MONERGISM_DOWNLOAD_ROOT_FOLDER = pathlib.Path(os.path.join(DOWNLOAD_ROOT_FOLDER,WEB_SCRAPING_ROOT_FOLDER,MONERGISM_ROOT_FOLDER)).as_posix() #: The folder where all the metadata files related to monergism will be stored



# The folders of logs 
MONERGISM_BY_SPEAKER_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(MONERGISM_LOG_ROOT_FOLDER,BY_SPEAKER_ROOT_FOLDER)).as_posix() #: The folder where all the **logs** of **Speakers** of **monergism** will be stored
MONERGISM_BY_TOPIC_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(MONERGISM_LOG_ROOT_FOLDER,BY_TOPIC_ROOT_FOLDER)).as_posix() #: The folder where all the **logs** of **Topics** of **monergism** will be stored
MONERGISM_BY_SCRIPTURE_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(MONERGISM_LOG_ROOT_FOLDER,BY_SCRIPTURE_ROOT_FOLDER)).as_posix() #: The folder where all the **logs** of **Scriptures** of **monergism** will be stored
MONERGISM_BY_SERIES_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(MONERGISM_LOG_ROOT_FOLDER,BY_SERIES_ROOT_FOLDER)).as_posix() #: The folder where all the **logs** of **Series** of **monergism** will be stored


# The folders of metadata
MONERGISM_BY_SPEAKER_METADATA_ROOT_FOLDER = pathlib.Path(os.path.join(MONERGISM_METADATA_ROOT_FOLDER,BY_SPEAKER_ROOT_FOLDER)).as_posix() #: The folder where all the **metadata** of **Speakers** of **monergism** will be stored
MONERGISM_BY_TOPIC_METADATA_ROOT_FOLDER = pathlib.Path(os.path.join(MONERGISM_METADATA_ROOT_FOLDER,BY_TOPIC_ROOT_FOLDER)).as_posix() #: The folder where all the **metadata** of **Topics** of **monergism** will be stored
MONERGISM_BY_SCRIPTURE_METADATA_ROOT_FOLDER = pathlib.Path(os.path.join(MONERGISM_METADATA_ROOT_FOLDER,BY_SCRIPTURE_ROOT_FOLDER)).as_posix() #: The folder where all the **metadata** of **Scriptures** of **monergism** will be stored
MONERGISM_BY_SERIES_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(MONERGISM_METADATA_ROOT_FOLDER,BY_SERIES_ROOT_FOLDER)).as_posix() #: The folder where all the **metadata** of **Series** of **monergism** will be stored


# The folders of downloads
MONERGISM_BY_SPEAKER_DOWNLOAD_ROOT_FOLDER = pathlib.Path(os.path.join(MONERGISM_DOWNLOAD_ROOT_FOLDER,BY_SPEAKER_ROOT_FOLDER)).as_posix() #: The folder where all the **logs** of **Speakers** of **monergism** will be stored
MONERGISM_BY_TOPIC_DOWNLOAD_ROOT_FOLDER = pathlib.Path(os.path.join(MONERGISM_DOWNLOAD_ROOT_FOLDER,BY_TOPIC_ROOT_FOLDER)).as_posix() #: The folder where all the **logs** of **Topics** of **monergism** will be stored
MONERGISM_BY_SCRIPTURE_DOWNLOAD_ROOT_FOLDER = pathlib.Path(os.path.join(MONERGISM_DOWNLOAD_ROOT_FOLDER,BY_SCRIPTURE_ROOT_FOLDER)).as_posix() #: The folder where all the **logs** of **Scriptures** of **monergism** will be stored
MONERGISM_BY_SERIES_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(MONERGISM_DOWNLOAD_ROOT_FOLDER,BY_SERIES_ROOT_FOLDER)).as_posix() #: The folder where all the **logs** of **Series** of **monergism** will be stored




# The variables of telegram 

TELEGRAM_LOG_ROOT_FOLDER = pathlib.Path(os.path.join(LOGS_ROOT_FOLDER,TELEGRAM_ROOT_FOLDER)).as_posix() #: The folder where all the log files related to monergism will be store
TELEGRAM_METADATA_ROOT_FOLDER = pathlib.Path(os.path.join(METADATA_ROOT_FOLDER,TELEGRAM_ROOT_FOLDER)).as_posix() #: The folder where all the metadata files related to monergism will be stored
TELEGRAM_DOWNLOAD_ROOT_FOLDER = pathlib.Path(os.path.join(DOWNLOAD_ROOT_FOLDER,TELEGRAM_ROOT_FOLDER)).as_posix() #: The folder where all the metadata files related to monergism will be stored

TELEGRAM_CHANNEL_ROOT_FOLDER = "channel"
TELEGRAM_CHANNEL_TEXT_MESSAGE_ROOT_FOLDER = "text_message"
TELEGRAM_CHANNEL_SPEAKER_ROOT_FOLDER = "speaker"


def get_default_json_filename(indice:int):
    """
        Return the name of the json file based on the indice.
         For example  0 gives file_0.json and 20 gives file_20.json
    """
    return f"file_{indice}.json"


def get_default_html_filename(indice:int):
    """
        Return the name of the json file based on the indice.
         For example  0 gives file_0.json and 20 gives file_20.json
    """
    return f"file_{indice}.html"




HTTP_REQUEST_TIMEOUT = 10 #: The default timeout value for http request


ELABORATED_DATA_FOLDER = "elaborated_data"
RAW_DATA_FOLDER = "raw_data"
