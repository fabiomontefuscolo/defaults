# zmodload zsh/zprof
export HISTSIZE=100000
export SAVEHIST=100000
setopt SHARE_HISTORY

export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="ys"

# TODO: remember to set cronjob
# 0 * * * * ${HOME}/.oh-my-zsh/tools/upgrade.sh -v silent
zstyle ':omz:update' mode disabled
DISABLE_AUTO_UPDATE=true

plugins=(direnv fzf git)
source $ZSH/oh-my-zsh.sh

bindkey \^U backward-kill-line

alias grep='grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn,.idea,.tox,__pycache__}'
alias ls='ls --almost-all --color'

export XDG_CACHE_HOME="$HOME/.cache"
export NPM_CONFIG_PREFIX="${HOME}/.local"

mkdir -m 700 -p $XDG_CACHE_HOME
mkdir -p "$HOME/.local/bin"

export PATH="$PATH:$HOME/.local/bin"

[ -f "$HOME/.zshenv" ] && source "$HOME/.zshenv"
# zprof > $HOME/.zshrc.prof
