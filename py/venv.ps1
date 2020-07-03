
# PowerShell script to delete or create the Python Virtual Environment.
# Requires Python 3; version 3.7 or higher recommended.
# Chris Joakim, Microsoft, 2020/07/03

echo 'displaying python and pip versions; python 3.7+ expected ...'
python --version
pip --version

echo 'deleting Scripts directory ...'
del .\Scripts\

echo 'creating new venv ...'
python -m venv .

echo 'pip install requirements.txt ...'
pip install -r .\requirements.txt

echo 'pip list ...'
pip list

echo 'done'
