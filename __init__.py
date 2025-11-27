'''
ReQueue Add-on
Author: MK
Version: 3.9.0
'''
from aqt import mw, gui_hooks
from aqt.qt import *
from .manager import reQueueManager
from .gui import openDashboard

def onProfileWillClose():
    reQueueManager.resetSession()

def refreshShortcut():
    # Function to clear and rebind the shortcut
    if reQueueManager.shortcutInstance:
        reQueueManager.shortcutInstance.setEnabled(False)
        reQueueManager.shortcutInstance.setParent(None)
        reQueueManager.shortcutInstance = None
        
    sequenceString = reQueueManager.userConfig.get("shortcutKey", "Ctrl+Shift+U")
    if not sequenceString:
        return
        
    try:
        newShortcut = QShortcut(QKeySequence(sequenceString), mw)
        newShortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
        newShortcut.activated.connect(reQueueManager.performUndoAndReshuffle)
        reQueueManager.shortcutInstance = newShortcut
    except:
        print("ReQueue: Shortcut error")

def setupMenu():
    try:
        menuAction = QAction("ReQueue Settings", mw)
        menuAction.triggered.connect(openDashboard)
        mw.form.menuTools.addAction(menuAction)
    except:
        pass

# Hook connections
gui_hooks.reviewer_did_answer_card.append(reQueueManager.onAnswered)
gui_hooks.profile_will_close.append(onProfileWillClose)
gui_hooks.main_window_did_init.append(refreshShortcut)
gui_hooks.main_window_did_init.append(setupMenu)