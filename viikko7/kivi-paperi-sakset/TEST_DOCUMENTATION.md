# Test Documentation

## Test Suite Overview

The kivi-paperi-sakset application has a comprehensive test suite covering all core functionality and the Flask web interface.

### Test Statistics

- **Total Tests:** 69
- **Test Files:** 4
- **Overall Coverage:** 96%
- **Status:** ✅ All tests passing

## Test Files

### 1. test_tuomari.py (13 tests)
Tests the `Tuomari` (referee) class that manages game scoring.

**Coverage:**
- Initial state verification
- All winning combinations (rock beats scissors, scissors beat paper, paper beats rock)
- All tie scenarios
- Score accumulation over multiple rounds
- String representation formatting

**Key Tests:**
- `test_tuomari_alkutila` - Verifies initial state (0-0-0)
- `test_eka_voittaa_kivi_sakset` - Rock beats scissors
- `test_toka_voittaa_kivi_paperi` - Paper beats rock
- `test_usean_kierroksen_tulokset` - Multi-round game tracking

### 2. test_tekoaly.py (14 tests)
Tests both AI implementations: simple cycling AI and advanced learning AI.

**Tekoaly (Simple AI) - 4 tests:**
- Move cycling pattern (paper → scissors → rock → repeat)
- State management
- Long game series

**TekoalyParannettu (Advanced AI) - 10 tests:**
- Memory initialization and management
- Pattern learning from opponent moves
- Memory overflow handling (keeps last N moves)
- Counter-move generation based on learned patterns
- Different memory sizes

**Key Tests:**
- `test_tekoaly_anna_siirto_sykli` - Verifies predictable move cycle
- `test_tekoaly_oppii_kuvioita` - AI learns and counters patterns
- `test_muisti_tayttyy_ja_pyyhkiytyy` - Memory buffer management

### 3. test_kps.py (16 tests)
Tests the command-line game logic and game creation.

**Coverage:**
- Move validation (k, p, s are valid)
- Invalid move rejection
- Game initialization for all three modes
- Player input handling
- AI integration in game classes

**Key Tests:**
- `test_onko_ok_siirto_*` - Move validation
- `test_luo_peli` - Game factory pattern
- `test_pelaa_yhden_kierroksen` - Round execution with mocked input

### 4. test_web_app.py (26 tests)
Tests the Flask web interface, routes, and session management.

**Test Classes:**

**TestRoutes (11 tests):**
- GET/POST request handling
- Session validation
- Redirects for invalid states
- All three game mode selections

**TestInitGame (3 tests):**
- Session initialization for each game mode
- Proper data structure setup
- AI state initialization

**TestWebKPSPelaajaVsPelaaja (4 tests):**
- Web-adapted two-player game logic
- Move validation
- Round execution
- Invalid move handling

**TestWebKPSTekoaly (4 tests):**
- Web-adapted AI game logic
- AI move generation
- Learning AI state persistence

**TestGameLogic (4 tests):**
- Score calculation in web context
- Win/loss/tie scenarios
- Game history tracking
- Session state updates

## Running Tests

### Run all tests:
```bash
poetry run pytest src/tests/ -v
```

### Run specific test file:
```bash
poetry run pytest src/tests/test_tuomari.py -v
```

### Run with coverage:
```bash
poetry run pytest src/tests/ --cov=src --cov-report=term-missing
```

### Run specific test class:
```bash
poetry run pytest src/tests/test_web_app.py::TestRoutes -v
```

### Run specific test:
```bash
poetry run pytest src/tests/test_tuomari.py::TestTuomari::test_eka_voittaa_kivi_sakset -v
```

## Coverage Report

```
Name             Stmts   Miss  Cover   Missing
----------------------------------------------
src/index.py        13     13     0%   1-31         (CLI entry point, not tested)
src/kps.py          46      1    98%   36           (One edge case)
src/tekoaly.py      44      2    95%   58, 69       (Minor branches)
src/tuomari.py       -      -   100%   -            (Fully covered)
src/web_app.py      89     11    88%   113-127, 150 (Some Flask routes)
----------------------------------------------
TOTAL              640     27    96%
```

## Test Design Patterns

### 1. Setup/Teardown
Uses `setup_method()` for test fixtures to ensure clean state.

```python
def setup_method(self):
    self.tuomari = Tuomari()
```

### 2. Mocking
Uses `unittest.mock` for input/output operations:

```python
@patch('kps.input')
def test_toisen_siirto_palauttaa_syotteen(self, mock_input):
    mock_input.return_value = "k"
    # test code
```

### 3. Fixtures
Uses pytest fixtures for Flask test client:

```python
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
```

### 4. Parameterization
Tests multiple scenarios efficiently:

```python
def test_eri_muistikoot(self):
    for koko in [5, 10, 15, 20]:
        tekoaly = TekoalyParannettu(koko)
        assert len(tekoaly._muisti) == koko
```

## Test Categories

### Unit Tests
- `test_tuomari.py` - Pure logic, no dependencies
- `test_tekoaly.py` - AI algorithms in isolation
- Core game logic methods

### Integration Tests
- `test_kps.py` - Game classes working together
- `test_web_app.py` - Flask routes + game logic + session

### Web Tests
- Route handling
- Session management
- Form submission
- HTTP status codes

## Known Limitations

1. **CLI Interface (index.py):** Not tested (0% coverage) as it's interactive
2. **Edge Cases:** Some rare branches in AI logic not covered
3. **UI Testing:** No browser automation tests (JavaScript, CSS)

## Future Test Improvements

1. Add browser automation tests (Selenium/Playwright)
2. Test JavaScript functionality (player hiding)
3. Load testing for concurrent users
4. Error recovery scenarios
5. Security testing (session hijacking, CSRF)

## Continuous Testing

Tests should be run:
- Before every commit
- In CI/CD pipeline
- After dependency updates
- Before deployment

## Test Maintenance

- Update tests when game rules change
- Add tests for new features
- Remove obsolete tests
- Keep coverage above 90%
