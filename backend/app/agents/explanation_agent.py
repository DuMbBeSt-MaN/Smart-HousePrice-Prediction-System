# app/agents/explanation_agent.py

class ExplanationAgent:
    """
    Turns scores + signals into human-readable explanations
    """

    def explain(self, listing: dict, intent: dict) -> str:
        explanations = []

        scores = listing.get("scores", {})

        for feature, enabled in intent.items():
            if not enabled:
                continue

            score = scores.get(feature, 0)

            if score >= 0.75:
                explanations.append(self._positive(feature))
            elif score >= 0.4:
                explanations.append(self._neutral(feature))
            else:
                explanations.append(self._negative(feature))

        if not explanations:
            return "This property matches your general location preference."

        return " ".join(explanations)

    # ------------------------
    # Explanation templates
    # ------------------------

    def _positive(self, feature: str) -> str:
        templates = {
            "schools": "There are multiple schools or colleges nearby.",
            "hospitals": "Hospitals are easily accessible from this location.",
            "parks": "The area has good green spaces and parks.",
            "safety": "The neighborhood appears relatively safe.",
            "water_risk": "The property has low exposure to nearby water bodies.",
            "fire_stations": "Fire stations are located close by."
        }
        return templates.get(feature, f"The property performs well for {feature}.")

    def _neutral(self, feature: str) -> str:
        return f"The area moderately satisfies your preference for {feature}."

    def _negative(self, feature: str) -> str:
        return f"This location scores lower for {feature} compared to others."