import sys
import pandas as pd
import requests

def main() -> None:
    print("Python executable:", sys.executable)
    print("Python version:", sys.version.split()[0])
    print("pandas version:", pd.__version__)
    print("requests version:", requests.__version__)
    print("Environment OK ✅")

if __name__ == "__main__":
    main()