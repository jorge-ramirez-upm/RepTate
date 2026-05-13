import sys
import os

PARENT_PATH: str = "../"
sys.path.insert(0, PARENT_PATH)

import RepTate.__main__

if __name__ == "__main__":
    RepTate.__main__.main()
