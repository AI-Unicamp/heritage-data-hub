import pycountry


def get_country_alpha2(country_name):
    """Return the alpha_2 code of the given country using pycountry."""
    try:
        if isinstance(country_name, list):
            country_name = country_name[0]  # Take the first element if it's a list
        if not isinstance(country_name, str):
            raise ValueError("Country name must be a string")

        country = pycountry.countries.search_fuzzy(country_name.strip())[0]
        return country.alpha_2.lower()  # Return the alpha_2 code in lowercase
    except (LookupError, ValueError) as e:
        print(f"Error finding country code for '{country_name}': {e}")
        return None  # Return None if the country code can't be found
