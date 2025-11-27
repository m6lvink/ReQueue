import os
import json

addonPath = os.path.dirname(__file__)
configFile = os.path.join(addonPath, "user_config.json")

def getDefaultConfig():
    # Function to return default settings dictionary
    defaultSettings = {}
    defaultSettings["cooldownDistance"] = 15
    defaultSettings["shortcutKey"] = "Ctrl+Shift+U"
    return defaultSettings

def validateConfig(configData):
    cleanConfig = getDefaultConfig()
    if "cooldownDistance" in configData and isinstance(configData["cooldownDistance"], int):
        cleanConfig["cooldownDistance"] = configData["cooldownDistance"]
    if "shortcutKey" in configData and isinstance(configData["shortcutKey"], str):
        cleanConfig["shortcutKey"] = configData["shortcutKey"]
    return cleanConfig

def loadUserConfig():
    if os.path.exists(configFile):
        try:
            with open(configFile, 'r', encoding='utf-8') as fileHandle:
                rawData = json.load(fileHandle)
                return validateConfig(rawData)
        except:
            return getDefaultConfig()
    return getDefaultConfig()

def saveUserConfig(currentConfig):
    try:
        with open(configFile, 'w', encoding='utf-8') as fileHandle:
            json.dump(currentConfig, fileHandle, ensure_ascii=False, indent=2)
    except:
        print("ReQueue: Save failed")