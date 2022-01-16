import os
import json


def openFile(file: str, returnJson: bool = False, mode: str = "r"):
    # creates human readable name by removing extension
    dotIndex = file.find(".")
    if dotIndex == -1:
        return "Please provide the filename with its extension"
    fileHrName = file[0, dotIndex]

    if os.path.isfile(file):
        print(f"\nFound saved {fileHrName} file")
        print(f"Opening {fileHrName}...")
        try:
            savedFile = open(file, mode)
            if returnJson:
                if file[-4, -1] == "json":
                    returnData = json.load(savedFile)
                else:
                    savedFile.close()
                    return "File extension must be .json if returnJson is true"
                savedFile.close()
            elif not returnJson:
                returnData = savedFile
            print("Done")
            return returnData
        except:
            return f"Unable to load file"
    else:
        return f"No saved file found"
