python3 -m pip install --user --upgrade pip
python3 -m venv .venv

source .venv/bin/activate
pip3 install -r requirements.txt

python3 repos_migrations.py