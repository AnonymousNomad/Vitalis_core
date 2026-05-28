from typing import Dict, Any
from src.core.session_mood import get_mood, set_mood
from src.core.affect import extract_affect

class AffectResponder:
    name = "affect_responder"

    def on_payload(self, payload: Dict[str, Any], client_id: str = "local_admin") -> Dict[str, Any]:
        last_step = payload.get("steps", [{}])[-1] if payload.get("steps") else {}
        text_input = last_step.get("text", "")
        
        valence, arousal = extract_affect(text_input)
        
        affect_msg = None
        if valence < 0.35 and arousal > 0.7:
            affect_msg = "[STATE: AGITATED] Switching to high-precision diagnostic output. State recorded."
            set_mood(client_id, valence, arousal)
        elif valence < 0.35 and arousal <= 0.7:
            affect_msg = "[STATE: SUB-OPTIMAL] Acknowledged. Proceeding with factual resolution."
            set_mood(client_id, valence, arousal)
        else:
            set_mood(client_id, 0.5, 0.5)

        base_answer = payload.get("final_conclusion", {}).get("label", "Operation complete.")
        final_reply = f"{affect_msg} {base_answer}" if affect_msg else base_answer

        return {"final_reply": final_reply}
