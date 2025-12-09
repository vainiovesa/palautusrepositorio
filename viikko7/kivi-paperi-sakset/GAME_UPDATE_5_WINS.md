# Game Update: First to 5 Wins

## Summary of Changes

The kivi-paperi-sakset application has been updated so that games continue until one player reaches **5 wins**. Previously, games would continue indefinitely until an invalid move was entered.

## Changes Made

### 1. Core Logic (tuomari.py)

Added two new methods to the `Tuomari` class:

- **`peli_paattynyt()`**: Returns `True` if either player has reached 5 wins
- **`voittaja()`**: Returns the winner (1 or 2) or `None` if game is still in progress

```python
def peli_paattynyt(self):
    """Returns True if either player has reached 5 wins"""
    return self.ekan_pisteet >= 5 or self.tokan_pisteet >= 5

def voittaja(self):
    """Returns the winner (1 or 2), or None if game is not finished"""
    if self.ekan_pisteet >= 5:
        return 1
    elif self.tokan_pisteet >= 5:
        return 2
    return None
```

### 2. Command-Line Interface (kps.py)

Updated the `pelaa()` method to:
- Check for game-over condition in the main loop
- Display "Peli päättyi!" instead of "Kiitos!"
- Announce the winner at the end

### 3. Web Application (web_app.py)

**Session Management:**
- Added `peli_paattynyt` and `voittaja` to session state
- Initialize these flags when starting a new game
- Update them after each round

**Template Data:**
- Pass game-over status and winner to template
- Template receives: `peli_paattynyt` and `voittaja`

### 4. Web Interface (pelaa.html)

**Visual Updates:**
- Scoreboard now displays "Tilanne (Ensimmäinen 5 voittoon!)"
- Game-over section with celebration when someone wins
- Hides game controls when game is finished
- Shows "Play Again" and "Return to Homepage" buttons
- Hides history during active play (only shown during game)

**Game-Over Display:**
```html
🎉 Peli päättyi!
🏆 Pelaaja X voitti pelin!
[Pelaa uudestaan] [Palaa etusivulle]
```

### 5. Styling (style.css)

Added new CSS for the game-over display:
- Gradient background effect
- Slide-in animation
- Large, celebratory text
- Responsive button layout

### 6. Tests

**Added 7 new tests in test_tuomari.py:**
- `test_peli_paattynyt_alkutilassa` - Game not over at start
- `test_peli_paattynyt_kun_eka_saa_5_voittoa` - Game ends when P1 gets 5
- `test_peli_paattynyt_kun_toka_saa_5_voittoa` - Game ends when P2 gets 5
- `test_peli_ei_paattynyt_kun_alle_5_voittoa` - Game continues with <5 wins
- `test_voittaja_palauttaa_none_kun_peli_kesken` - No winner during play
- `test_voittaja_palauttaa_1_kun_eka_voittaa` - Winner is player 1
- `test_voittaja_palauttaa_2_kun_toka_voittaa` - Winner is player 2

**Added 3 new tests in test_web_app.py:**
- `test_peli_paattynyt_kun_pelaaja1_saa_5_voittoa` - Web game ends for P1
- `test_peli_paattynyt_kun_pelaaja2_saa_5_voittoa` - Web game ends for P2
- `test_peli_ei_paattynyt_alle_5_voitossa` - Web game continues with <5

**Updated 1 test:**
- `test_init_kaksinpeli` - Now checks for game-over flags

## Test Results

✅ **All 79 tests passing** (was 69, now 79)

```
Platform: Linux, Python 3.12.3
Test Files: 4
Total Tests: 79
Passed: 79
Failed: 0
Duration: 0.22s
```

### Test Breakdown:
- test_kps.py: 16 tests ✅
- test_tekoaly.py: 14 tests ✅
- test_tuomari.py: 20 tests ✅ (+7 new)
- test_web_app.py: 29 tests ✅ (+3 new)

## How It Works

### Command-Line Version:
1. Players make moves as before
2. Game continues until one player reaches 5 wins
3. Game announces "Peli päättyi!" and the winner
4. Returns to main menu

### Web Version:
1. Players select moves as before
2. Score updates after each round
3. When a player reaches 5 wins:
   - Game controls disappear
   - Celebration screen appears
   - Shows the winner
   - Offers "Play Again" or "Return Home" options

## Example Game Flow

```
Player 1: 0 | Player 2: 0 | Ties: 0
↓ (P1 plays rock, P2 plays scissors)
Player 1: 1 | Player 2: 0 | Ties: 0
↓ (continue playing...)
Player 1: 4 | Player 2: 3 | Ties: 2
↓ (P1 wins again)
Player 1: 5 | Player 2: 3 | Ties: 2

🎉 Game Over!
🏆 Player 1 wins!
```

## Backwards Compatibility

- All existing tests still pass
- Existing game logic unchanged (just added win condition)
- Web interface gracefully degrades if session flags missing
- Command-line version maintains same input format

## Future Enhancements

Possible improvements:
- Make win threshold configurable (3, 5, 7, etc.)
- Add game statistics tracking
- Show match history after game ends
- Add rematch functionality maintaining same players
- Tournament mode with best-of-X series
