import os
import aiohttp
import asyncio
from typing import Dict, Optional

async def generate_stream_links(file_path: str, file_name: str) -> Dict[str, str]:
    """
    Generate streaming links for a file
    """
    base_url = os.environ.get("DOWNLOAD_URL", "https://your-domain.com")
    file_basename = os.path.basename(file_path)
    
    links = {
        'direct': f"{base_url}/download/{file_basename}",
        'stream': f"{base_url}/stream/{file_basename}",
        'preview': f"{base_url}/preview/{file_basename}",
        'original': file_path
    }
    
    return links

async def get_media_info(file_path: str) -> Dict[str, any]:
    """
    Get media information for streaming
    """
    import subprocess
    
    try:
        # Use ffprobe to get media info
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            file_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
        
    except Exception as e:
        return {"error": str(e)}

async def is_streamable(file_path: str) -> bool:
    """
    Check if file is streamable
    """
    mime_type = await get_mime_type(file_path)
    streamable_types = ['video', 'audio', 'pdf']
    return any(x in mime_type for x in streamable_types)

async def get_mime_type(file_path: str) -> str:
    """
    Get MIME type of file
    """
    import mimetypes
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'application/octet-stream'

async def create_stream_thumbnail(file_path: str) -> Optional[str]:
    """
    Create thumbnail for streaming
    """
    try:
        # Create thumbnails directory
        thumb_dir = "thumbnails"
        os.makedirs(thumb_dir, exist_ok=True)
        
        # Generate thumbnail
        thumb_path = os.path.join(thumb_dir, f"{os.path.basename(file_path)}.jpg")
        
        cmd = [
            'ffmpeg',
            '-i', file_path,
            '-ss', '00:00:01',
            '-vframes', '1',
            '-vf', 'scale=320:-1',
            thumb_path
        ]
        
        subprocess.run(cmd, capture_output=True)
        return thumb_path
        
    except Exception as e:
        print(f"Thumbnail creation error: {e}")
        return None
