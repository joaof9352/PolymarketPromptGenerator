import requests
import json


def get_slug_from_url(event_url: str) -> str:
    try:
        return event_url.split('?')[0].split('/')[-1]
    except Exception as e:
        raise ValueError(f"Erro ao extrair slug da URL: {e}")


def fetch_event_data(slug: str) -> dict:
    api_url = f"https://gamma-api.polymarket.com/events?slug={slug}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list) or not data:
            raise ValueError("Nenhum dado encontrado para o evento.")
        return data[0]  # Primeiro item da lista de eventos
    except requests.RequestException as e:
        raise ConnectionError(f"Erro ao buscar dados da API: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao decodificar JSON: {e}")


def parse_market_info(market: dict) -> dict | None:
    try:
        option_name = market.get('groupItemTitle') or market.get('question') or 'Yes/No'
        outcome_prices = market.get('outcomePrices', ["0", "0"])

        if isinstance(outcome_prices, str):
            outcome_prices = json.loads(outcome_prices)

        yes_cost = round(float(outcome_prices[0]) * 100, 2)
        no_cost = round(float(outcome_prices[1]) * 100, 2)
        volume = float(market.get('volumeNum', 0))

        return {
            "option_name": option_name,
            "yes_price": yes_cost,
            "no_price": no_cost,
            "volume": volume
        }
    except (ValueError, TypeError, IndexError, json.JSONDecodeError) as e:
        print(f"Erro ao processar mercado '{market.get('question', 'Sem nome')}': {e}")
        return None


def build_prompt(event_data: dict, include_volume: bool = True) -> str:
    title = event_data.get('title', 'Unknown Event')
    description = event_data.get('description', 'No description available.')
    resolution_source = event_data.get('resolutionSource', 'No resolution source specified.')
    end_date = event_data.get('endDate', 'Unknown end date.')
    markets = event_data.get('markets', [])

    if not markets:
        return "This event has no markets available."

    prompt_lines = [
        "Analyze Polymarket data to identify markets with value for betting. Define 'value' as a market where the difference between the market's implied probability (Yes Price) and the estimated true probability exceeds 5% and offers a positive expected return after accounting for Polymarket fees (e.g., 2%). Respond with a JSON array where each element represents a market analysis in the following format:",
        "",
        "```json",
        "[",
        "  {",
        '    "market": "<Option Name>",',
        '    "true_cost": <Estimated true probability of the Yes outcome in percentage, e.g., 5.0>,',
        '    "value_score": <Absolute difference between Yes Price and true_cost>,',
        '    "bet": "<Yes, No, or None>",',
        '    "reasoning": "<Detailed explanation of the estimated true probability, including candidate relevance, X sentiment, historical patterns, and market liquidity>",',
        '    "confidence": "<low, medium, high>"',
        "  }",
        "]",
        "```",
        "",
        "# EVENT",
        f"- **Title**: {title}",
        f"- **Description**: {description}",
        f"- **Resolution Source**: {resolution_source}",
        f"- **End Date**: {end_date}",
        "",
        "# POSSIBLE MARKETS"
    ]

    for market in markets:
        info = parse_market_info(market)
        if info:
            market_lines = [
                f"- **Option Name**: {info['option_name']}",
                f"  - **Yes Price**: {info['yes_price']}%",
                f"  - **No Price**: {info['no_price']}%",
            ]
            if include_volume:
                market_lines.append(f"  - **Volume**: {info['volume']}")
            prompt_lines.extend(market_lines)

    prompt_lines.append("""
# INSTRUCTIONS
- Estimate the 'true' probability using: (1) relevance of the outcome based on historical patterns, public statements, or connections to the event; (2) sentiment from X posts or news after the event's start date; (3) historical data on similar events; and (4) Polymarket trading volume to assess market confidence. Weight these factors and explain their contribution in the reasoning.
- Prioritize recent data from provided search results and X posts (post-event start date). Cross-reference sources for reliability and discard outdated or unverified information.
- Recommend a 'Yes' or 'No' bet only if the absolute difference between the Yes Price and true_cost is at least 5% and the expected return, accounting for Polymarket fees (e.g., 2%), is positive. Otherwise, set 'bet' to 'None'.
- Ignore markets with 0% Yes/No prices or low liquidity (volume < $1000), assume no value unless credible external evidence suggests otherwise. Note illiquidity in the reasoning.
- Include a 'confidence' field (low, medium, high) based on data availability. If information is limited, provide a probability range for 'true_cost' (e.g., 10-15%) and note uncertainty.
- Sort markets by descending value_score to highlight the most promising betting opportunities.
""")

    return "\n".join(prompt_lines)


def get_polymarket_prompt(event_url: str, include_volume: bool = True) -> str:
    try:
        slug = get_slug_from_url(event_url)
        event_data = fetch_event_data(slug)
        return build_prompt(event_data, include_volume)
    except Exception as e:
        return f"Error generating prompt: {e}"


# Exemplo de uso
if __name__ == '__main__':
    url = "https://polymarket.com/event/israel-x-hamas-ceasefire-by-july-15"
    print(get_polymarket_prompt(url))
