#!/usr/bin/env bash
# PreToolUse hook (course-builder): block real provider secret prefixes that
# GitHub Push Protection rejects. Defanged placeholders (ak_exemplo-...) pass.
# Exit 0 = allow | Exit 2 = block (stdout is shown to the model).
# Never crashes on a missing/malformed payload: falls through to exit 0.

payload="$(cat 2>/dev/null)"
[ -z "$payload" ] && exit 0

# Real provider prefixes + enough trailing alphanumerics to look like a live key:
#   sk_live_ / sk_test_ + 24+ alphanumerics  (Stripe)
#   AKIA + 16+ alphanumerics                 (AWS access key id)
#   ghp_ + 36+ alphanumerics                 (GitHub PAT)
# Defanged examples use the ak_ prefix, which none of these match.
pattern='(sk_live_|sk_test_)[A-Za-z0-9]{24,}|AKIA[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{36,}'

if printf '%s' "$payload" | grep -Eq "$pattern"; then
  matched="$(printf '%s' "$payload" | grep -Eo "$pattern" | head -n1)"
  cat <<EOF
BLOCKED by block-real-secret-prefixes.sh: real provider secret prefix detected in tool input ("$matched").

GitHub Push Protection rejects tokens that use real provider prefixes (sk_live_, sk_test_, AKIA, ghp_).
Use a defanged placeholder instead, e.g.  ak_exemplo-CURSO-chave-falsa-NAO-USAR
EOF
  exit 2
fi

exit 0