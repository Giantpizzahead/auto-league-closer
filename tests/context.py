from pathlib import Path
import sys

TEST_PATH = Path(__file__).parent.resolve()
DATA_PATH = TEST_PATH / "data"
MODULE_PATH = TEST_PATH.parent / "leaguecloser"

# Add root directory to path (for importing leaguecloser)
sys.path.insert(0, str(TEST_PATH.parent))

import leaguecloser.findimg as findimg
