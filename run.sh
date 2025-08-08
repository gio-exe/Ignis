if [ -f "config.py" ]; then
    echo "Starting client..."
    python3 main.py
else
    echo "config.py not found, running setup..."
    python3 setup.py
fi
