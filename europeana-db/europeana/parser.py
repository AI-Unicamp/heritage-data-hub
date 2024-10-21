def parse_metadata(item):
    """Extract relevant metadata fields from an API item."""
    return {
        "id": item.get("id"),
        "title": item.get("title", ["No title"])[0],
        "description": item.get("dcDescription", ["No description"])[0],
        "creator": item.get("dcCreator", ["Unknown"])[0],
    }


def parse_image_url(item):
    """Extract the image URL from an API item."""
    try:
        return item["edmIsShownBy"][0]
    except (KeyError, IndexError):
        return None
