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
    if not isinstance(configData, dict):
        return cleanConfig
    if "cooldownDistance" in configData and isinstance(configData["cooldownDistance"], int) and not isinstance(configData["cooldownDistance"], bool):
        cooldownDistance = configData["cooldownDistance"]
        if 1 <= cooldownDistance <= 999:
            cleanConfig["cooldownDistance"] = cooldownDistance
    if "shortcutKey" in configData and isinstance(configData["shortcutKey"], str):
        shortcutKey = configData["shortcutKey"].strip()
        if shortcutKey:
            cleanConfig["shortcutKey"] = shortcutKey
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
        cleanConfig = validateConfig(currentConfig)
        currentConfig.clear()
        currentConfig.update(cleanConfig)
        with open(configFile, 'w', encoding='utf-8') as fileHandle:
            json.dump(cleanConfig, fileHandle, ensure_ascii=False, indent=2)
    except:
        print("ReQueue: Save failed")
