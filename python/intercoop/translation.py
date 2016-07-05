from yamlns import namespace as ns


class Translator(object):

    def __init__(self, language='es', fallback='es'):
        self.language = language if type(language) == list else[language] 
        self.fallback = fallback
    
    def __call__(self, data):
        return self.translate(data)

    def translate(self, data):

        if type(data) == ns:
            # defined language
            for lang in self.language:
                try: return data[lang]
                except KeyError: pass

            # fallback language
            try: return data[self.fallback]
            except KeyError: pass

            # Non translatable dict
            return ns(
                (key, self.__call__(value))
                for key, value in data.items()
                )

        if type(data) == list:
            return [
                self.__call__(item)
                for item in data
                ]

        return data





