"""
This module is meant to offer the base classes for the download of works(pdf, mp3, etc)
"""
import os 

from Instrumentum_sanae_doctrinae.web_scraping import http_connexion
class DownloadFromUrl():
    def __init__(self,url,output_file_path,aiohttp_session):
        self.url = url 
        self.output_file_path = output_file_path
        self.aiohttp_session = aiohttp_session
        
    async def download(self):
        pass 
        
    async def is_downloaded(self):
        return os.path.exists(self.output_file_path)
    
    
    def get_file_extension_from_header(self,content_type):
        """
        Get file extension based on the Content-Type in aiohttp response headers.

        Args:
            headers (dict): The headers dictionary from an aiohttp response.

        Returns:
            str: File extension (e.g., '.html', '.xml', '.txt', '.pdf').
        """
        # Mapping of content types to file extensions
        content_type_to_extension = {
            "text/html": ".html",
            "application/json": ".json",
            "text/plain": ".txt",
            "application/xml": ".xml",
            "text/xml": ".xml",
            "application/pdf": ".pdf",
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "application/javascript": ".js",
            "text/javascript": ".js",
            "text/css": ".css",
            "application/zip": ".zip",
            "application/x-tar": ".tar",
            "application/x-7z-compressed": ".7z",
            "application/vnd.rar": ".rar",
            "application/octet-stream": ".bin",
            "audio/mpeg": ".mp3",
            "audio/ogg": ".ogg",
            "audio/wav": ".wav",
            "audio/flac": ".flac",
            "video/mp4": ".mp4",
            "video/webm": ".webm",
            "video/x-msvideo": ".avi",
            "application/vnd.ms-excel": ".xls",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
            "application/msword": ".doc",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
            "application/vnd.ms-powerpoint": ".ppt",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
            "application/rtf": ".rtf",
            "application/x-shockwave-flash": ".swf",
        }

        

        # Return the corresponding file extension or a default
        return content_type_to_extension.get(content_type, ".bin")  # Default to .bin for unknown types

    
    def is_binary_content(self,content_type):
        """
        Determine if a content type is binary or text-based.

        Args:
            content_type (str): The content type from a response header.

        Returns:
            bool: True if binary, False if text-based.
        """
        binary_content_types = [
            "application/octet-stream",
            "application/pdf",
            "application/zip",
            "application/x-tar",
            "application/x-7z-compressed",
            "application/vnd.rar",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "application/x-shockwave-flash",
            "image/png",
            "image/jpeg",
            "image/gif",
            "image/webp",
            "image/bmp",
            "image/x-icon",
            "audio/mpeg",
            "audio/ogg",
            "audio/wav",
            "audio/flac",
            "video/mp4",
            "video/webm",
            "video/x-msvideo",
            "application/vnd.apple.mpegurl",
            "application/x-mpegURL",
            "application/x-bittorrent",
            "font/woff",
            "font/woff2",
            "font/ttf",
            "font/otf",
        ]

        return content_type.lower() in binary_content_types
