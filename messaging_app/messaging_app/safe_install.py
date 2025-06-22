import os

# safe_install.py
with open("requirements.txt") as f:
    for line in f:
        package = line.strip()
        if package and not package.startswith("#"):
            print(f"Installing {package}...")
            code = os.system(f"pip install --no-cache-dir {package}")
            if code != 0:
                print(f"Warning: Failed to install {package}")

