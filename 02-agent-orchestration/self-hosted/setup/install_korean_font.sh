#!/bin/bash

# Script start message
echo "Starting Korean font installation and matplotlib configuration..."

# Install required packages
echo "Installing Nanum font..."
if command -v apt-get > /dev/null; then
    # Ubuntu/Debian systems
    sudo apt-get update
    sudo apt-get install -y fonts-nanum
elif command -v yum > /dev/null; then
    # CentOS/RHEL systems
    sudo yum install -y nanum-fonts-all
else
    # If package manager is not found, download fonts directly
    echo "Package manager not found. Downloading fonts directly..."
    mkdir -p ~/.fonts
    cd ~/.fonts
    if command -v wget > /dev/null; then
        wget https://github.com/naver/nanumfont/raw/master/NanumGothic.ttf
    elif command -v curl > /dev/null; then
        curl -O https://github.com/naver/nanumfont/raw/master/NanumGothic.ttf
    else
        echo "Neither wget nor curl is installed. Skipping font download."
    fi
fi

# Update font cache
echo "Updating font cache..."
fc-cache -f -v

# Check installed fonts
echo "List of installed Nanum fonts:"
fc-list | grep "Nanum"

# Find matplotlib configuration file
echo "Finding matplotlib configuration file..."
MATPLOTLIB_DIR=$(python -c "import matplotlib; print(matplotlib.get_configdir())")
MATPLOTLIB_DATA_DIR=$(python -c "import matplotlib; print(matplotlib.get_data_path())")
MATPLOTLIBRC_PATH="${MATPLOTLIB_DATA_DIR}/matplotlibrc"

echo "matplotlib configuration file path: ${MATPLOTLIBRC_PATH}"

# Backup and modify matplotlibrc file
if [ -f "$MATPLOTLIBRC_PATH" ]; then
    echo "Backing up and modifying matplotlibrc file..."
    cp "$MATPLOTLIBRC_PATH" "${MATPLOTLIBRC_PATH}.backup"

    # Change or add font.family setting
    if grep -q "^#font.family" "$MATPLOTLIBRC_PATH"; then
        sed -i 's/^#font.family.*/font.family: sans-serif/' "$MATPLOTLIBRC_PATH"
    elif grep -q "^font.family" "$MATPLOTLIBRC_PATH"; then
        sed -i 's/^font.family.*/font.family: sans-serif/' "$MATPLOTLIBRC_PATH"
    else
        echo "font.family: sans-serif" >> "$MATPLOTLIBRC_PATH"
    fi

    # Change or add font.sans-serif setting
    if grep -q "^#font.sans-serif" "$MATPLOTLIBRC_PATH"; then
        sed -i 's/^#font.sans-serif.*/font.sans-serif: NanumGothic, DejaVu Sans, Bitstream Vera Sans, Computer Modern Sans Serif, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, sans-serif/' "$MATPLOTLIBRC_PATH"
    elif grep -q "^font.sans-serif" "$MATPLOTLIBRC_PATH"; then
        sed -i 's/^font.sans-serif.*/font.sans-serif: NanumGothic, DejaVu Sans, Bitstream Vera Sans, Computer Modern Sans Serif, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, sans-serif/' "$MATPLOTLIBRC_PATH"
    else
        echo "font.sans-serif: NanumGothic, DejaVu Sans, Bitstream Vera Sans, Computer Modern Sans Serif, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, sans-serif" >> "$MATPLOTLIBRC_PATH"
    fi

    # Change or add axes.unicode_minus setting
    if grep -q "^#axes.unicode_minus" "$MATPLOTLIBRC_PATH"; then
        sed -i 's/^#axes.unicode_minus.*/axes.unicode_minus: False/' "$MATPLOTLIBRC_PATH"
    elif grep -q "^axes.unicode_minus" "$MATPLOTLIBRC_PATH"; then
        sed -i 's/^axes.unicode_minus.*/axes.unicode_minus: False/' "$MATPLOTLIBRC_PATH"
    else
        echo "axes.unicode_minus: False" >> "$MATPLOTLIBRC_PATH"
    fi
else
    echo "matplotlibrc file not found. Creating new configuration file..."
    mkdir -p "${MATPLOTLIB_DIR}"
    cat > "${MATPLOTLIB_DIR}/matplotlibrc" << EOF
font.family: sans-serif
font.sans-serif: NanumGothic, DejaVu Sans, Bitstream Vera Sans, Computer Modern Sans Serif, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, sans-serif
axes.unicode_minus: False
EOF
    echo "New configuration file created: ${MATPLOTLIB_DIR}/matplotlibrc"
fi

# Delete matplotlib font cache
echo "Deleting matplotlib font cache..."
rm -rf ~/.cache/matplotlib/* 2>/dev/null || echo "Cache files do not exist or cannot be deleted."

echo "Configuration complete. Korean characters should now display correctly in matplotlib."
echo "If problems persist, try adding the following code directly to your Python script:"
echo "
import matplotlib.font_manager as fm
# Find NanumGothic font path
font_path = fm.findfont('NanumGothic')
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False
"

# Create test script
echo "Creating test script..."
cat > test_korean_font.py << EOF
import matplotlib.pyplot as plt
import numpy as np

# Generate data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create graph
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Sine function')
plt.plot(x, -y, label='-Sine function')
plt.title('Korean Font Test: Sine Function Graph')
plt.xlabel('x-axis label')
plt.ylabel('y-axis label')
plt.legend()
plt.grid(True)
plt.savefig('korean_font_test.png')
plt.show()

print("Test complete! Please check the korean_font_test.png file.")
EOF

echo "Test script created: test_korean_font.py"
echo "You can test it with the following command: python test_korean_font.py"