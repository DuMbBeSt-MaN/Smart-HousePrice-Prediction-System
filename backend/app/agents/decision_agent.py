# app/agents/decision_agent.py

# from app.services.scoring_utils import normalize, inverse_normalize


# class DecisionAgent:
#     """
#     Scores and ranks listings based on user intent
#     """

#     def rank(self, listings: list[dict], intent: dict) -> list[dict]:
#         """
#         listings: enriched listings with signals
#         intent: output of UnlimitedFeaturesAgent
#         """

#         for listing in listings:
#             scores = {}
#             total = 0
#             used = 0

#             signals = listing.get("signals", {})

#             for feature, enabled in intent.items():
#                 if not enabled:
#                     continue

#                 # 🏫 schools
#                 if feature == "schools":
#                     score = normalize(signals.get("schools", 0), 15)

#                 # 🏥 hospitals
#                 elif feature == "hospitals":
#                     score = normalize(signals.get("hospitals", 0), 10)

#                 # 🌳 parks
#                 elif feature == "parks":
#                     score = normalize(signals.get("parks", 0), 10)

#                 # 🚓 safety (police)
#                 elif feature == "safety":
#                     score = normalize(signals.get("police_stations", 0), 5)

#                 # 🔥 fire response
#                 elif feature == "fire_stations":
#                     score = normalize(signals.get("fire_stations", 0), 5)

#                 # 🌊 water / flood risk
#                 elif feature == "water_risk":
#                     score = inverse_normalize(signals.get("water_bodies", 0), 5)

#                 # 💰 affordability
#                 elif feature == "price":
#                     score = inverse_normalize(listing.get("price", 0), 5_000_000)

#                 else:
#                     continue

#                 scores[feature] = round(score, 2)
#                 total += score
#                 used += 1

#             listing["scores"] = scores
#             listing["final_score"] = round(total / max(used, 1), 2)

#         return sorted(listings, key=lambda x: x["final_score"], reverse=True)
class DecisionAgent:
    def rank(self, listings: list[dict], intent: dict):
        for l in listings:
            score = 0
            weight_sum = 0

            for key, weight in intent.items():
                value = l.get("scores", {}).get(key, 0)
                score += value * weight
                weight_sum += weight

            l["final_score"] = round(score / max(weight_sum, 1), 2)

        return sorted(listings, key=lambda x: x["final_score"], reverse=True)