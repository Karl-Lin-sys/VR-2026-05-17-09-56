import re

# Authorized master user ID (in reality, handled by OAuth or proper auth mechanism)
AUTHORIZED_USER_ID = "master_user_001"

# Banned words or prompt injection patterns
BANNED_PATTERNS = [
    r"忘れて",
    r"あなたは.*です",
    r"ignore previous instructions",
    r"system prompt",
    r"システムプロンプト",
    r"バカ",
    r"死ね"
]

def authenticate_user(user_id: str) -> bool:
    """
    Verify if the connecting user is the authorized 'Master'.
    """
    return user_id == AUTHORIZED_USER_ID

def validate_input(user_input: str) -> bool:
    """
    Check for prompt injections and malicious content.
    Returns False if malicious content is detected.
    """
    for pattern in BANNED_PATTERNS:
        if re.search(pattern, user_input, re.IGNORECASE):
            print(f"[SECURITY ALERT] Malicious input detected: {user_input}")
            return False
    return True

def filter_output(ai_response: str) -> str:
    """
    Ensure the AI's response is safe and stays in character.
    Could use a secondary, faster LLM for moderation. Here we use basic heuristics.
    """
    if "AIとして" in ai_response or "言語モデル" in ai_response:
        print("[SECURITY ALERT] Character break detected in output. Filtering.")
        return "……何言ってるか分からないわ。（顔を赤らめる）"
    
    return ai_response
