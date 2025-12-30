# test_dependencies.py
import sys

print("Python version:", sys.version)
print("\nTrying to import packages...")

packages = ['numpy', 'pandas', 'sklearn', 'flask', 'json', 'datetime']

for package in packages:
    try:
        if package == 'sklearn':
            import sklearn
            print(f"✅ {package}: {sklearn.__version__}")
        elif package == 'numpy':
            import numpy as np
            print(f"✅ {package}: {np.__version__}")
        elif package == 'pandas':
            import pandas as pd
            print(f"✅ {package}: {pd.__version__}")
        elif package == 'flask':
            import flask
            print(f"✅ {package}: {flask.__version__}")
        else:
            __import__(package)
            print(f"✅ {package}: OK")
    except ImportError as e:
        print(f"❌ {package}: {e}")
    except Exception as e:
        print(f"⚠️  {package}: {e}")

print("\n✅ All packages checked!")
