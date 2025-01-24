import requests
import tempfile
import os
from typing import Optional

SARVAM_API_KEY = "b5e4630f-4270-44d4-982d-bf194bc9acbc"

def speech_to_text(audio_data: bytes) -> Optional[str]:
    """Convert speech to text using Sarvam AI API"""
    url = "https://api.sarvam.ai/speech-to-text-translate"
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        temp_file.write(audio_data)
        temp_file.flush()
        
        payload = {
            'model': 'saaras:v1',
            'prompt': ''
        }
        
        files = [
            ('file', ('audio.wav', open(temp_file.name, 'rb'), 'audio/wav'))
        ]
        
        headers = {
            'api-subscription-key': SARVAM_API_KEY
        }
        
        try:
            response = requests.post(url, headers=headers, data=payload, files=files)
            #response.raise_for_status()
            return response.json().get('transcript')
        except Exception as e:
            print(f"Error in speech to text conversion: {e}")
            return None
        finally:
            os.unlink(temp_file.name)

def text_to_speech(text: str, language_code: str = "hi-IN") -> Optional[bytes]:
    """Convert text to speech using Sarvam AI API"""
    url = "https://api.sarvam.ai/text-to-speech"
    
    payload = {
        "inputs": [text],
        "target_language_code": language_code,
        "speaker": "meera",
        "speech_sample_rate": 8000,
        "enable_preprocessing": True,
        "model": "bulbul:v1"
    }
    
    headers = {
        "Content-Type": "application/json",
        "api-subscription-key": SARVAM_API_KEY
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Error in text to speech conversion: {e}")
        return None 