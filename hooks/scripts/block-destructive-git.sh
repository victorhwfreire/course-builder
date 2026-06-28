#!/usr/bin/env bash
# PreToolUse hook (course-builder): block destructive git / file / SQL operations
# while the builder works on the answer-key branch.
# Exit 0 = allow | Exit 2 = block (stdout is shown to the model).
# Never crashes on a missing/malformed payload: falls through to exit 0.
#
# Blocked:  git push --force | git push -f | git reset --hard | rm -rf | DROP TABLE
# Allowed:  git push --force-with-lease (the safe force), plain git push/commit/add.

payload="$(cat 2>/dev/null)"
[ -z "$payload" ] && exit 0

# Case-insensitive so DROP TABLE matches drop table. git/rm are lowercase in
# practice; matching their uppercase variants is harmless (they aren't real cmds).
# The --force arm requires a space, a quote, or end-of-input right after
# --force / -f, so --force-with-lease (next char is '-') does NOT match. The
# quote is included because the command is embedded in a JSON payload, so a
# trailing flag is followed by " not by end-of-line.
pattern="git[[:space:]]+push[[:space:]]+(-f|--force)([[:space:]\"']|\$)"\
"|git[[:space:]]+reset[[:space:]]+--hard"\
"|rm[[:space:]]+-[rf]{2}([[:space:]\"']|\$)"\
"|drop[[:space:]]+table"

if printf '%s' "$payload" | grep -Ei -q "$pattern"; then
  matched="$(printf '%s' "$payload" | grep -Eio "$pattern" | head -n1)"
  cat <<EOF
BLOCKED by block-destructive-git.sh: destructive operation detected in tool input ("$matched").

Blocked operations: git push --force / git push -f, git reset --hard, rm -rf, DROP TABLE.
If you truly need a force-push, use  git push --force-with-lease  (the safe force) and re-run.
EOF
  exit 2
fi

exit 0