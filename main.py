import requests
from collections import Counter


class APIError(Exception):
    pass


class CatFactProcessor:
    def __init__(self):
        self.last_fact = ""

    def get_fact(self):
        try:
            response = requests.get("https://catfact.ninja/fact")
            response.raise_for_status()
            data = response.json()
            self.last_fact = data["fact"]
            return self.last_fact
        except requests.exceptions.RequestException as e:
            raise APIError(f"Ошибка при запросе к API: {e}") from e

    def get_fact_analysis(self):
        if not self.last_fact:
            return {"length": 0, "letter_frequencies": {}}
        fact_length = len(self.last_fact)
        letter_frequencies = dict(Counter(self.last_fact.lower()))
        return {
            "length": fact_length,
            "letter_frequencies": letter_frequencies,
        }
