#!/usr/bin/env zsh

if (( ! $+commands[fabric-ai] )); then
  echo "# Warning: fabric-ai command not found. Please install fabric-ai to use this plugin." > /dev/stderr
  return
fi


fabric-create-command-helper() {
  # Tell ZLE we're about to do terminal I/O
  zle -I

  # Print prompt explicitly to terminal
  print -n "Ask about command: "

  # Read input from terminal
  local question
  read question < /dev/tty

  # If user provided no input, return
  if [[ -z "$question" ]]; then
    zle reset-prompt
    return
  fi

  # Show a loading message
  print "⏳ Asking fabric-ai..."

  # Call fabric-ai with the question
  local result
  result=$(echo "$question" | fabric-ai --pattern create_command 2>/dev/null)

  # Clean up any markdown code fences and extra whitespace
  result=$(echo "$result" | sed 's/^```[a-z]*$//' | sed '/^```$/d' | sed '/^$/d' | tr -d '\n' | xargs)

  # If we got a result, put it in the buffer
  if [[ -n "$result" ]]; then
    BUFFER="$result"
    CURSOR=$#BUFFER  # Move cursor to end of line
  else
    BUFFER="# Error: No response from fabric-ai"
  fi

  # Reset the prompt and redisplay
  zle reset-prompt
}

# Register the widget with ZLE
zle -N fabric-create-command-helper

# Bind it to Ctrl+X, Ctrl+F (for "fabric")
bindkey '^X^F' fabric-create-command-helper
