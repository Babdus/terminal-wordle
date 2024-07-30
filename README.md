# Terminal Wordle for Georgian

## Installation

Open terminal

### Check dependencies

Check if git is installed
```commandline
git --version
```

If it returns some version of git then jump to the [Install terminal wordle](#install-terminal-wordle) section.
If it says `git: command not found` or similar, continue with [Install dependencies](#install-dependencies) section.

### Install dependencies

Homebrew
```commandline
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

git
```commandline
brew install git
```

### Install terminal wordle

Change directory to home
```commandline
cd ~
```

Clone GitHub repository
```commandline
git clone https://github.com/Babdus/terminal-wordle.git
```

Make executable
```commandline
chmod +x terminal-wordle/main.py
```

Create directory for executable
```commandline
sudo mkdir -p /usr/local/bin
```
and enter your user's password if asked

Create a symbolic link to the executable
```commandline
sudo ln -s $(pwd)/terminal-wordle/main.py /usr/local/bin/wordle
```

## Play

Just type
```commandline
wordle
```
and enjoy!