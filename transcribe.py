# Add these two lines at the very top of the file
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# Rest of the imports
import queue
import threading
import numpy as np
import sounddevice as sd
import pyautogui
import keyboard
import time
from faster_whisper import WhisperModel
import torch

class LiveTranscriber:
    def __init__(self):
        # Default to 'small' model with CUDA if available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type = "float16" if device == "cuda" else "float32"
        
        print(f"Loading small model on {device}...")
        self.model = WhisperModel(
            "small",
            device=device,
            compute_type=compute_type
        )
        print("Ready!")
        
        # Audio parameters
        self.sample_rate = 16000
        self.chunk_duration = 2
        self.chunk_samples = int(self.sample_rate * self.chunk_duration)
        
        self.audio_buffer = []
        self.buffer_lock = threading.Lock()
        self.is_running = False
        self.last_text = ""
    
    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        if self.is_running:
            with self.buffer_lock:
                self.audio_buffer.extend(indata[:, 0])
    
    def process_audio(self):
        while self.is_running:
            with self.buffer_lock:
                if len(self.audio_buffer) >= self.chunk_samples:
                    audio_chunk = np.array(self.audio_buffer[:self.chunk_samples])
                    self.audio_buffer = self.audio_buffer[self.chunk_samples:]
                else:
                    continue
            
            try:
                audio_chunk = audio_chunk.astype(np.float32)
                
                segments, _ = self.model.transcribe(
                    audio_chunk,
                    language="en",
                    beam_size=5,
                    vad_filter=True,
                    vad_parameters=dict(min_silence_duration_ms=500)
                )
                
                for segment in segments:
                    transcribed_text = segment.text.strip()
                    if transcribed_text and transcribed_text != self.last_text:
                        print(f"Transcribed: {transcribed_text}")
                        pyautogui.write(" " + transcribed_text)
                        self.last_text = transcribed_text
            
            except Exception as e:
                print(f"Error in processing: {e}")
            
            time.sleep(0.1)
    
    def start(self):
        if not self.is_running:
            self.is_running = True
            self.audio_buffer = []
            
            self.stream = sd.InputStream(
                channels=1,
                samplerate=self.sample_rate,
                callback=self.audio_callback
            )
            self.stream.start()
            
            self.process_thread = threading.Thread(target=self.process_audio)
            self.process_thread.start()
            
            print("Started! Press F2 to stop.")
    
    def stop(self):
        if self.is_running:
            self.is_running = False
            self.stream.stop()
            self.stream.close()
            self.process_thread.join()
            print("\nStopped.")
            with self.buffer_lock:
                self.audio_buffer = []

def main():
    transcriber = LiveTranscriber()
    print("Press F2 to start/stop, Ctrl+C to exit")
    transcribing = False
    
    try:
        while True:
            if keyboard.is_pressed('f2'):
                if not transcribing:
                    transcriber.start()
                    transcribing = True
                else:
                    transcriber.stop()
                    transcribing = False
                time.sleep(0.5)
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        if transcriber.is_running:
            transcriber.stop()
        print("\nExiting...")

if __name__ == "__main__":
    main()