import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from bookfold import create

create("ornament.jpg", 3, 477, 190)
