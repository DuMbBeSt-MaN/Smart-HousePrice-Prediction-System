# class UnlimitedFeaturesAgent:
#     """
#     Converts arbitrary user features into normalized scoring signals
#     """

#     FEATURE_MAP = {
#         # health
#         "hospital": "hospitals",
#         "clinic": "hospitals",

#         # education
#         "school": "schools",
#         "college": "schools",
#         "university": "schools",

#         # environment
#         "park": "parks",
#         "green": "parks",
#         "nature": "parks",

#         # safety
#         "safe": "safety",
#         "crime": "safety",
#         "police": "safety",

#         # disasters / risk
#         "water": "water_risk",
#         "flood": "water_risk",
#         "river": "water_risk",

#         # emergency response
#         "fire": "fire_response",
#         "fire station": "fire_response",
#     }

#     def parse(self, features: list[str]) -> dict:
#         """
#         Example output:
#         {
#             "hospitals": 1.0,
#             "schools": 1.0,
#             "parks": 1.0,
#             "safety": 1.0,
#             "water_risk": -1.0
#         }
#         """

#         signals: dict[str, float] = {}

#         for feature in features:
#             f = feature.lower()

#             matched = False
#             for keyword, signal in self.FEATURE_MAP.items():
#                 if keyword in f:
#                     matched = True

#                     # negative scoring for risk-based features
#                     if signal in ["water_risk"]:
#                         signals[signal] = -1.0
#                     else:
#                         signals[signal] = 1.0

#             # allow unknown features for LLM expansion later
#             if not matched:
#                 signals[f] = 0.5  # neutral weight

#         return signals
# app/agents/unlimited_features_agent.py

# class UnlimitedFeaturesAgent:
#     """
#     Converts arbitrary user features into internal signal keys
#     """

#     def parse(self, features: list[str]) -> dict:
#         signals = {}

#         for f in features:
#             f = f.lower()

#             # 💰 affordability
#             if any(k in f for k in ["cheap", "affordable", "low price", "budget"]):
#                 signals["price"] = True

#             # 🎓 education
#             if any(k in f for k in ["school", "college", "university"]):
#                 signals["schools"] = True

#             # 🏥 healthcare
#             if any(k in f for k in ["hospital", "medical", "clinic"]):
#                 signals["hospitals"] = True

#             # 🌳 greenery
#             if any(k in f for k in ["park", "green", "garden", "nature"]):
#                 signals["parks"] = True

#             # 🚨 safety
#             if any(k in f for k in ["safe", "low crime", "secure"]):
#                 signals["safety"] = True

#             # 🔥 emergency response
#             if "fire" in f:
#                 signals["fire_stations"] = True

#             # 🌊 flood / water risk
#             if any(k in f for k in ["flood", "water", "river"]):
#                 signals["water_risk"] = True

#         return signals
class UnlimitedFeaturesAgent:
    def parse(self, features: list[str]) -> dict:
        """Parse features into weighted signals. Returns only keys supported by planner:
        hospitals, schools, parks, water_risk, price
        """
        signals = {}

        for f in features:
            f = f.lower()

            if "hospital" in f or "health" in f or "medical" in f:
                signals["hospitals"] = signals.get("hospitals", 0) + 1.0
            if "school" in f or "college" in f or "university" in f or "education" in f:
                signals["schools"] = signals.get("schools", 0) + 1.2
            if "park" in f or "green" in f or "nature" in f or "outdoor" in f:
                signals["parks"] = signals.get("parks", 0) + 0.8
            if "safe" in f or "security" in f or "crime" in f:
                signals["schools"] = signals.get("schools", 0) + 1.0
            if "water" in f or "flood" in f or "river" in f or "risk" in f:
                signals["water_risk"] = signals.get("water_risk", 0) + 1.1
            if "cheap" in f or "affordable" in f or "budget" in f or "low price" in f or "inexpensive" in f:
                signals["price"] = signals.get("price", 0) + 1.5

        # Ensure at least some defaults if nothing matched
        if not signals:
            signals = {"schools": 1.0, "parks": 1.0, "price": 1.0}

        return signals