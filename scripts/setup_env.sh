#!/usr/bin/env bash
#
# setup_env.sh - write every .env this repo needs, from one set of keys.
#
# This file is COMMITTED and contains NO secrets. It reads your keys from the
# environment and fans them out to the seven projects that need them, so a
# fresh clone takes one paste instead of seven.
#
# Usage:
#     export OPENAI_API_KEY='sk-proj-...'        # required
#     export GEMINI_API_KEY='AIza... or AQ....'            # optional (01_prompt_serialization)
#     export GOOGLE_API_KEY='AIza... or AQ....'            # optional (02_handOnWork)
#     export ANTHROPIC_API_KEY='sk-ant-...'      # optional (02_handOnWork)
#     export GROQ_API_KEY='gsk_...'              # optional (02_handOnWork fallback)
#     ./scripts/setup_env.sh
#
#     ./scripts/setup_env.sh --force             # overwrite .env files that already have content
#     ./scripts/setup_env.sh --dry-run           # show what would be written, write nothing
#
# Every .env it writes is gitignored, so your keys never reach GitHub.
# This repo is PUBLIC - keep it that way.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GENAI="$REPO_ROOT/python_tut_2026/05_python_genai"

FORCE=0
DRY_RUN=0
for arg in "$@"; do
    case "$arg" in
        --force)   FORCE=1 ;;
        --dry-run) DRY_RUN=1 ;;
        -h|--help) sed -n '3,21p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "unknown option: $arg (try --help)" >&2; exit 2 ;;
    esac
done

# ── keys ─────────────────────────────────────────────────────────────────────
# OPENAI_API_KEY is the only one used by more than one project, so it is the
# only one we insist on. The rest are written as empty assignments when unset:
# the file stays valid, and it is obvious what is still missing.
OPENAI_API_KEY="${OPENAI_API_KEY:-}"
GEMINI_API_KEY="${GEMINI_API_KEY:-}"
GOOGLE_API_KEY="${GOOGLE_API_KEY:-}"
ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}"
GROQ_API_KEY="${GROQ_API_KEY:-}"

if [[ -z "$OPENAI_API_KEY" && -t 0 ]]; then
    # `read` returns non-zero on EOF (Ctrl-D), which would abort under `set -e`
    # before the friendly error below ever prints. `|| true` keeps that path alive.
    read -rsp "OPENAI_API_KEY (input hidden): " OPENAI_API_KEY || true
    echo
fi

# A stray space after '=' is the classic .env bug: python-dotenv strips it, but
# `docker --env-file` and `set -a; source .env` do not. Trim before writing.
#
# This MUST run before the emptiness check below. A whitespace-only key would
# otherwise pass the guard, write seven .env files containing "KEY=", and then
# poison every later run - the skip test is `[[ -s ]]`, so those non-empty but
# useless files would be silently skipped even once you supplied the real key.
trim() { printf '%s' "$1" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'; }

# A value with an embedded newline would write a second KEY=VALUE line into the
# .env - silently defining a variable nobody asked for. Refuse it rather than
# quietly mangling the key, which is what stripping the newline would do.
reject_multiline() {
    local var="$1" val="${!1}"
    if [[ "$val" == *$'\n'* || "$val" == *$'\r'* ]]; then
        echo "error: $var contains a newline. Check how you exported it." >&2
        exit 1
    fi
}
for _v in OPENAI_API_KEY GEMINI_API_KEY GOOGLE_API_KEY ANTHROPIC_API_KEY GROQ_API_KEY; do
    reject_multiline "$_v"
    printf -v "$_v" '%s' "$(trim "${!_v}")"
done

if [[ -z "$OPENAI_API_KEY" ]]; then
    cat >&2 <<'EOF'
error: OPENAI_API_KEY is not set (or contains only whitespace).

    export OPENAI_API_KEY='sk-proj-...'
    ./scripts/setup_env.sh

Get a key at https://platform.openai.com/api-keys
EOF
    exit 1
fi

# Secrets are about to hit disk. Create them 0600 from birth rather than
# chmod-ing after the fact, which would leave a window where the file is
# world-readable under the usual umask 022 - and leave it that way for good if
# the script is interrupted between the write and the chmod.
umask 077

# ── writer ───────────────────────────────────────────────────────────────────
written=0 skipped=0 missing_dir=0

# write_env <relative-dir> <VAR>...
write_env() {
    local reldir="$1"; shift
    local dir="$GENAI/$reldir"
    local target="$dir/.env"

    if [[ ! -d "$dir" ]]; then
        echo "  ?? $reldir - directory not found, skipping"
        missing_dir=$((missing_dir + 1))
        return
    fi

    # -s is true only for a file that exists AND is non-empty, so the 0-byte
    # .env in 02_handOnWork is treated as absent and gets filled in.
    if [[ -s "$target" && $FORCE -eq 0 ]]; then
        echo "  -- $reldir/.env already has content (use --force to overwrite)"
        skipped=$((skipped + 1))
        return
    fi

    local body="" var val
    for var in "$@"; do
        val="${!var}"
        body+="$var=$val"$'\n'
        [[ -z "$val" ]] && echo "  !! $reldir/.env - $var is empty, fill it in by hand"
    done

    if [[ $DRY_RUN -eq 1 ]]; then
        echo "  ~~ would write $reldir/.env ($*)"
        return
    fi

    # Refuse to write through a symlink - these paths are gitignored, so nothing
    # tracks them, and following one would put the key wherever it points.
    if [[ -L "$target" ]]; then
        echo "  !! $reldir/.env is a symlink - refusing to write a secret through it"
        skipped=$((skipped + 1))
        return
    fi

    printf '%s' "$body" > "$target"     # umask 077 above makes this 0600 at creation
    chmod 600 "$target"                 # belt and braces for a pre-existing file
    echo "  ok $reldir/.env ($*)"
    written=$((written + 1))
}

echo "Writing .env files under python_tut_2026/05_python_genai/"
[[ $DRY_RUN -eq 1 ]] && echo "(dry run - nothing will be written)"
echo

write_env "01_prompt_serialization"                                  OPENAI_API_KEY GEMINI_API_KEY
write_env "05_building_chat_with_rag/rag"                            OPENAI_API_KEY
write_env "06_scalable_rag_with_async_queu_distributed_workers/02_rag_queue" OPENAI_API_KEY
write_env "07_sending_media_to_llm"                                  OPENAI_API_KEY
write_env "08_lang_graph"                                            OPENAI_API_KEY
write_env "09_langgraph_checkpoints"                                 OPENAI_API_KEY
write_env "10_LANGCHAIN_BASIC2EXPERT/02_handOnWork"                  OPENAI_API_KEY GOOGLE_API_KEY ANTHROPIC_API_KEY GROQ_API_KEY

echo
echo "done: $written written, $skipped skipped, $missing_dir missing"
echo
echo "04_build_Ai_Agent_agentic_workflow needs no .env - MODEL and OLLAMA_HOST"
echo "have working defaults. See ENVIRONMENT.md for the full table."
