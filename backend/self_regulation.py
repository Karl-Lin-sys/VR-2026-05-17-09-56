class SelfRegulationSystem:
    """
    Manages the internal state and emotion of the AI.
    Prevents the AI from becoming too extreme (self-regulation).
    """
    def __init__(self):
        self.state = {
            "mood": 50,       # 0 (very angry) to 100 (very happy)
            "intimacy": 50,   # 0 (stranger) to 100 (deeply in love)
            "energy": 100     # 0 (exhausted) to 100 (energetic)
        }
        
    def evaluate_input(self, user_input: str) -> dict:
        """
        Update state based on user input before generating a response.
        """
        if "好き" in user_input or "かわいい" in user_input:
            self._adjust_state("mood", 10)
            self._adjust_state("intimacy", 5)
        elif "嫌い" in user_input:
            self._adjust_state("mood", -20)
            self._adjust_state("intimacy", -5)
            
        # Self-regulation: Over time, energy depletes
        self._adjust_state("energy", -1)
        
        return self.state

    def determine_behavior(self, ai_response: str):
        """
        Determine the final emotion and VRM action/animation based on the response and internal state.
        """
        emotion = "neutral"
        action = "idle"
        
        if self.state["mood"] > 80:
            emotion = "happy"
            action = "smile_and_wave"
        elif self.state["mood"] < 30:
            emotion = "angry"
            action = "cross_arms"
            
        if "好き" in ai_response or "スパシーバ" in ai_response:
            emotion = "embarrassed"  # Tsundere blush
            action = "look_away"
            
        return emotion, action

    def _adjust_state(self, key: str, amount: int):
        """
        Helper to safely adjust state with bounding (0-100).
        This is the core of the 'Self-Regulation' (リミッター).
        """
        new_val = self.state[key] + amount
        # Clamp values between 0 and 100
        self.state[key] = max(0, min(100, new_val))

    def get_state(self) -> dict:
        return self.state
