# Gonance

## 1. Flask

### Debug mode
`env FLASK_APP=flask_app.py FLASK_ENV=development flask run`

### Config files needed

- config/XXXXXX.json
```json
{}
```

## 2. API

### Endpoints
- `/apiv1/XXXXX`

## 3. Development
```
# Install Python 3
xcode-select --install
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python3
brew upgrade python3
python3 --version

# Clone repository to your local computer
git clone https://github.com/gobeltri/gonance-flask.git
cd gonance-flask

# Create Python Virtual Environmet and activate it. Execute 'deactivate' after use
python3 -m venv virtualenv
source virtualenv/bin/activate
python --version
#deactivate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```
