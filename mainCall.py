import whisper
import os
import subprocess
from pathlib import Path

class MainFunction:
    #future dev: timelapse to run
    #better version choosing
    def __init__(self, model):
        currentPath = Path(__file__).resolve().parent
        thePath = currentPath.parent
        # self.SOURCE = "preDatabase\\"
        self.MODEL = "turbo"
        self.ALLMODELS = ["tiny", "base", "small", "medium", "large", "turbo"]
        if model in self.ALLMODELS:
            print("Model found, using "+model)
            self.modules = whisper.load_model(model)
        else:
            print(f"Model not found, using turbo as default")
            self.modules = whisper.load_model("turbo")
    
    def transcribe(self, wav_16_file:list[str]) -> dict:

        returnedOutputs={}
        for theFile in wav_16_file:
            wav_file=theFile
            print(wav_file)

            if os.path.exists(wav_file):
                print("----------------------------")
                print("File found ✅")
            else:
                print("----------------------------")
                print("File NOT found ❌")
                return {"text": None, "language": None}
            
            wav_file = self.checkHertz(wav_file)

            result = self.modules.transcribe(wav_file)
            print("-------------------RESULT-------------------")
            print(f"Language: {result['language']}")
            print(result["text"])
            returnedOutputs['text'] = result['text']
            returnedOutputs['language'] = result['language']
        return returnedOutputs
    
    def checkHertz(self, fileHere:str)->str:
        #idk, this is chat gpt suggestion
        commandCheckHerz=['ffmpeg', '-i', fileHere]
        theFile = fileHere.split(".")[0]
        fixedFile = theFile+"_wav16.wav"

        if os.path.exists(fixedFile):
            return fixedFile

        command=['ffmpeg', '-i', fileHere, '-ar', '16000', '-ac', '1', '-sample_fmt', 's16', fixedFile]

        theHerts = subprocess.run(commandCheckHerz, capture_output=True, text=True)
        sample=theHerts.stderr
        if '16000' not in sample or 'mono' not in sample:
            print("refactoring.........")
            subprocess.run(command, capture_output=True, check=True)
            print("Refactored")
        else:
            print("Good to go")
        
        return fixedFile

    
