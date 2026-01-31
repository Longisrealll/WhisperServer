import numpy as np
import os
from pathlib import Path
from mainCall import MainFunction
from moviepy.editor import VideoFileClip
import subprocess
import shutil
from pydub import AudioSegment


class STT_handler:
    def __init__(self, model: str):
        current_dir = Path(__file__).resolve().parent
        self.pathing = current_dir.parent
        self.data = MainFunction(model)
        command=['mkdir', 'preDatabase']

        if not os.path.exists(f"{self.pathing}\\preDatabase"):
            subprocess.run(command, capture_output=True, text=True)


    def deleteAfterCommand(self, path:str):
        # remove everything at the end of the day, need to be more advance
        if os.path.exists(f"{self.pathing}\\preDatabase"):
            shutil.rmtree(f"{self.pathing}\\preDatabase")
    
    def set_data(self, webmFile:str):
        # clip = VideoFileClip(webmFile)
        clips = AudioSegment.from_file(webmFile, format="webm")
        fileName = webmFile.split("\\")
        theName = fileName[-1].split(".")[0]
        finalize = f"{theName}_wav.wav"
        clips.export(f"{self.pathing}\\testing\\preDatabase\\{finalize}", "wav")
        # print(f"{self.pathing}\\preDatabase\\{finalize}")
        # clip.audio.write_audiofile(f"{self.pathing}/preDatabase/{finalize}")

        res = self.data.transcribe([f"{self.pathing}\\testing\\preDatabase\\{finalize}"])

        return res
