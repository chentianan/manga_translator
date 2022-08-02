from googletrans import Translator
def translate(org_string):
    translator = Translator()
    translation = translator.translate(org_string, dest='en')
    print(org_string,translation.text)
    return translation.text
