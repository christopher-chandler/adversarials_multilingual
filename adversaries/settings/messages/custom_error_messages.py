class CustomErrorMessages:
    """
    Custom error messages
    """

    class MultiLingualSpacyError(Exception):
        """
        Exception raised for unsupported languages in Spacy.
        """

        def __init__(self, language, valid_langs):
            self.language = language
            self.valid_langs = valid_langs
            message = (
                f"'{self.language}' is not supported."
                f"The following languages are valid: {', '.join(self.valid_langs)}"
            )
            super().__init__(message)
