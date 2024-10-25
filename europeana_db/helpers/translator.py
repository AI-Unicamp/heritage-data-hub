from deep_translator import GoogleTranslator


def translate_to_english(text, original_language_code="auto"):
    """Translate text from the original language to English using GoogleTranslator."""
    try:
        translator = GoogleTranslator(source=original_language_code, target="en")
        return translator.translate(text)
    except Exception as e:
        if "No support for the provided language" in str(e):
            print(
                f"Translation failed (Error 7001): No support for the provided language '{original_language_code}'."
            )
        else:
            print(f"Translation failed (Error 7001): {e}")
        return "Translation failed: Error 7001"  # Return a message indicating failure
