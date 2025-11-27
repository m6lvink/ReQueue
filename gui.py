from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip
from .manager import reQueueManager
from . import __init__ as mainInit 

class DashboardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ReQueue Settings")
        self.resize(500, 450)
        self.currentConfig = reQueueManager.userConfig.copy()
        self.isRecording = False
        self.buildUI()
    
    def keyPressEvent(self, event):
        if not self.isRecording:
            super().keyPressEvent(event)
            return
        
        keyInput = event.key()
        keyModifiers = event.modifiers()
        
        if keyInput in (Qt.Key.Key_Shift, Qt.Key.Key_Control, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            return
        
        keyText = QKeySequence(keyInput).toString()
        keyParts = list()
        
        if keyModifiers & Qt.KeyboardModifier.ControlModifier:
            keyParts.append("Ctrl")
        if keyModifiers & Qt.KeyboardModifier.AltModifier:
            keyParts.append("Alt")
        if keyModifiers & Qt.KeyboardModifier.ShiftModifier:
            keyParts.append("Shift")
        if keyModifiers & Qt.KeyboardModifier.MetaModifier:
            keyParts.append("Meta")
        if keyText:
            keyParts.append(keyText)
        
        self.shortcutEdit.setText("+".join(keyParts))
        self.stopRecording()
    
    def startRecording(self):
        self.isRecording = True
        self.recordBtn.setText("Press keys...")
        self.recordBtn.setStyleSheet("background-color: #d32f2f; color: white;")
        self.shortcutEdit.clear()
    
    def stopRecording(self):
        self.isRecording = False
        self.recordBtn.setText("Record")
        self.recordBtn.setStyleSheet("")
    
    def doSave(self):
        if self.isRecording:
            self.stopRecording()
        
        reQueueManager.userConfig["cooldownDistance"] = self.cooldownSpin.value()
        reQueueManager.userConfig["shortcutKey"] = self.shortcutEdit.text()
        reQueueManager.saveCurrentConfig()
        
        # Trigger shortcut refresh in main
        from . import refreshShortcut
        refreshShortcut()
        
        tooltip("Saved", period=1000)
        self.accept()
        
    def buildUI(self):
        mainLayout = QVBoxLayout()
        
        infoBox = QGroupBox("Info")
        infoLayout = QVBoxLayout()
        infoLayout.addWidget(QLabel("Undo review -> Bury card -> Auto-unbury after cooldown."))
        infoBox.setLayout(infoLayout)
        mainLayout.addWidget(infoBox)
        
        settingsBox = QGroupBox("Configuration")
        settingsLayout = QVBoxLayout()
        
        # Cooldown
        cooldownLayout = QHBoxLayout()
        cooldownLayout.addWidget(QLabel("Cooldown Distance:"))
        self.cooldownSpin = QSpinBox()
        self.cooldownSpin.setRange(1, 999)
        self.cooldownSpin.setValue(self.currentConfig.get("cooldownDistance", 15))
        cooldownLayout.addWidget(self.cooldownSpin)
        cooldownLayout.addStretch()
        settingsLayout.addLayout(cooldownLayout)
        
        # Shortcut
        shortcutLayout = QHBoxLayout()
        shortcutLayout.addWidget(QLabel("Shortcut:"))
        self.shortcutEdit = QLineEdit()
        self.shortcutEdit.setText(self.currentConfig.get("shortcutKey", "Ctrl+Shift+U"))
        self.shortcutEdit.setReadOnly(True) 
        shortcutLayout.addWidget(self.shortcutEdit)
        self.recordBtn = QPushButton("Record")
        self.recordBtn.clicked.connect(self.startRecording)
        shortcutLayout.addWidget(self.recordBtn)
        settingsLayout.addLayout(shortcutLayout)
        
        settingsBox.setLayout(settingsLayout)
        mainLayout.addWidget(settingsBox)
        
        # Buttons
        buttonLayout = QHBoxLayout()
        saveBtn = QPushButton("Save")
        saveBtn.clicked.connect(self.doSave)
        closeBtn = QPushButton("Cancel")
        closeBtn.clicked.connect(self.reject)
        buttonLayout.addStretch()
        buttonLayout.addWidget(saveBtn)
        buttonLayout.addWidget(closeBtn)
        mainLayout.addLayout(buttonLayout)
        
        self.setLayout(mainLayout)

def openDashboard():
    dashboardDialog = DashboardDialog(mw)
    dashboardDialog.exec()