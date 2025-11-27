from aqt import mw
from aqt.utils import tooltip
from . import config

class ReQueueManager:
    def __init__(self):
        self.heldCards = list()
        self.reviewCount = 0
        self.userConfig = config.loadUserConfig()
        self.shortcutInstance = None
        self.lastCardId = None

    def saveCurrentConfig(self):
        config.saveUserConfig(self.userConfig)

    def resetSession(self):
        # Function to clear session data on profile close
        self.heldCards.clear()
        self.reviewCount = 0
        self.lastCardId = None

    def unburyCard(self, cardId, targetQueue):
        # Function to restore card to original queue
        if targetQueue is None or not mw.col:
            return False
        try:
            cardObject = mw.col.get_card(cardId)
            # Only unbury if still buried (-2)
            if cardObject.queue == -2:
                cardObject.queue = targetQueue
                mw.col.update_card(cardObject)
                return True
        except:
            return False
        return False

    def onAnswered(self, reviewer, card, ease):
        # Capture ID immediately for potential undo
        self.lastCardId = card.id
        
        self.reviewCount += 1
        cooldownLimit = self.userConfig.get("cooldownDistance", 15)
        
        cardsToUnbury = list()
        indicesToRemove = list()
        
        # Check cooldowns
        for index, (heldId, origQueue, buriedAt) in enumerate(self.heldCards):
            distance = self.reviewCount - buriedAt
            if distance >= cooldownLimit:
                cardsToUnbury.append((heldId, origQueue))
                indicesToRemove.append(index)
        
        # Process unburies
        didUnbury = False
        for (uId, uQueue) in cardsToUnbury:
            if self.unburyCard(uId, uQueue):
                didUnbury = True
                
        # Clean up list
        for index in reversed(indicesToRemove):
            self.heldCards.pop(index)
            
        if didUnbury:
            mw.col.reset()

    def performUndoAndReshuffle(self):
        # Function executes the raw undo logic
        if not mw.reviewer or not self.lastCardId:
            tooltip("No card to requeue", period=1000)
            return

        # Check if already held to prevent duplicates
        for (hId, hQ, hB) in self.heldCards:
            if hId == self.lastCardId:
                tooltip("Already requeued", period=1000)
                return

        if not mw.col.undo_status().undo:
            tooltip("Nothing to undo", period=1000)
            return

        # Execute Undo
        mw.col.undo()

        try:
            # Re fetch card to modify queue
            cardId = self.lastCardId
            cardObject = mw.col.get_card(cardId)
            savedQueue = cardObject.queue
            
            # Bury the card
            cardObject.queue = -2
            mw.col.update_card(cardObject)
            
            # Store data
            cardData = (cardId, savedQueue, self.reviewCount)
            self.heldCards.append(cardData)
            
            # Refresh UI
            mw.col.reset()
            if mw.reviewer:
                mw.reviewer.nextCard()
                
            # Feedback
            heldCount = len(self.heldCards)
            tooltip(f"Requeued ({heldCount} hidden)", period=1000)
            
        except:
            tooltip("Error during requeue", period=1000)

# Create instance
reQueueManager = ReQueueManager()