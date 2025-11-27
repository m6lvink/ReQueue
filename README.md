# ReQueue: Undo & Reshuffle

Accidentally revealed a card before you could recall it? This add-on lets you undo the review and reshuffle the card back into your deck without penalty.

## What It Does

Press **Ctrl+Shift+U** immediately after rating a card to undo the review. The card is temporarily buried and will reappear after a set number of cards (default: 15).

Useful when you:
- Click "Show Answer" too early
- See the answer before recalling
- Want to retry a card later without affecting your interval

## Features

- Undo multiple cards per session - each tracks its own cooldown
- No limit on how many cards you can undo
- **Duplicate Protection:** Prevents accidental double-queueing if you press the shortcut multiple times
- Original intervals preserved (review was undone)
- Works across all card types (new, learning, review)

## Installation

1. Open Anki
2. Go to Tools > Add-ons
3. Click "Get Add-ons..."
4. Enter code: **1247565211** (2.1+)
5. Click OK and restart Anki

## Setup

After installing, go to Tools > ReQueue Settings to configure:
- Cooldown distance (how many cards before undone cards reappear)
- Keyboard shortcut (default is Ctrl+Shift+U)

## Usage

1. Review cards normally
2. If you accidentally reveal a card, click a button (Again/Hard/Good/Easy)
3. Press **Ctrl+Shift+U** immediately after
4. The card is undone and buried
5. Continue reviewing
6. The card reappears after your cooldown distance

You can undo multiple cards in the same session. Each card tracks independently from when it was buried.

## Notes

- Only works during review (not preview or browse mode)
- Must press the shortcut immediately after rating a card (relies on Anki's undo function)
- **Safety:** If you press the shortcut multiple times for the same card, the add-on will notify you that it is "Already requeued" and ignore the extra inputs.
- Each card reappears based on when it was buried, not when the last card was buried

## Requirements

- Anki 2.1.50 or later
- No external dependencies required

## Support

For issues or suggestions, leave a review on AnkiWeb!

## License

Created by MK