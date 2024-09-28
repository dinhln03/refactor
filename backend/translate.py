import googletrans

class Translation():
    def __init__(self, to_lang='en'):
        # The class Translation is a wrapper for the two translation libraries, googletrans and translate.
        self.__to_lang = to_lang 
        self.translator = googletrans.Translator()

    def __call__(self, text):
        """
        The function takes in a text and preprocesses it before translation

        :param text: The text to be translated
        :return: The translated text.
        """
        text = text.lower().strip()
        return self.translator.translate(text, dest=self.__to_lang).text