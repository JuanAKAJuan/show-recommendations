import os
import sys

import requests
from dotenv import load_dotenv
from colorama import init, Fore, Style


def get_show_id(api_key, show_name):
    url = "https://api.themoviedb.org/3/search/tv"
    params = {"api_key": api_key, "query": show_name, "page": 1}
    response = requests.get(url, params=params)
    data = response.json()
    results = data.get("results", [])
    if results:
        # Return the ID of the first matching show
        return results[0]["id"], results[0]["name"]
    else:
        return None, None


def get_recommendations(api_key, show_id):
    url = f"https://api.themoviedb.org/3/tv/{show_id}/recommendations"
    params = {"api_key": api_key, "language": "en-US", "page": 1}
    response = requests.get(url, params=params)
    data = response.json()
    recommendations = data.get("results", [])
    return recommendations


def main():
    # Initialize colorama
    init(autoreset=True)

    load_dotenv()

    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        print(f"{Fore.RED}API key not found. Please set TMDB_API_KEY in your .env file.{Style.RESET_ALL}")
        sys.exit(1)

    if len(sys.argv) < 2:
        print(f"{Fore.YELLOW}Usage: python recommend.py '<Show Name>'{Style.RESET_ALL}")
        sys.exit(1)

    show_name = " ".join(sys.argv[1:])

    show_id, official_name = get_show_id(api_key, show_name)
    if not show_id:
        print(f"{Fore.RED}No show found with the name '{show_name}'.{Style.RESET_ALL}")
        sys.exit(1)

    recommendations = get_recommendations(api_key, show_id)
    if not recommendations:
        print(f"{Fore.RED}No recommendations found for '{official_name}'.{Style.RESET_ALL}")
        sys.exit(1)

    print(f"\n{Fore.CYAN}Recommendations based on '{Fore.GREEN}{official_name}{Fore.CYAN}':\n{Style.RESET_ALL}")
    for idx, show in enumerate(recommendations, start=1):
        name = show.get("name", "Unknown Title")
        overview = show.get("overview", "No description available.")
        first_air_date = show.get("first_air_date", "N/A")
        print(f"{idx}. {Fore.GREEN}{name} {Fore.LIGHTBLACK_EX}(First aired on {first_air_date}){Style.RESET_ALL}")
        print(f"   {overview}\n")


if __name__ == "__main__":
    main()
