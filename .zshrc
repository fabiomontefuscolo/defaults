# zmodload zsh/zprof
export HISTSIZE=100000
export SAVEHIST=100000
setopt SHARE_HISTORY

mkdir -p "$HOME/.local/bin"
export PATH="$HOME/.local/bin:$PATH"

export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="ys"

# TODO: remember to set cronjob
# 0 * * * * ${HOME}/.oh-my-zsh/tools/upgrade.sh -v silent
zstyle ':omz:update' mode disabled
DISABLE_AUTO_UPDATE=true

plugins=(direnv fzf git fabric-ai)
source $ZSH/oh-my-zsh.sh

bindkey '^U' backward-kill-line
bindkey '^P' up-line-or-beginning-search

alias grep='grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn,.idea,.tox,__pycache__}'
alias ls='ls --almost-all --color'

export LESS="-XFR"
export XDG_CACHE_HOME="$HOME/.cache"
export XDG_PICTURES_DIR="$HOME/Pictures"

# zprof > $HOME/.zshrc.prof
