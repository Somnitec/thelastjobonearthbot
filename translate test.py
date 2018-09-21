from translate import Translator
translator= Translator(from_lang="autodetect",to_lang="nl")
translation = translator.translate("what is your nose all abut?")
print(translation)
translator= Translator(from_lang="nl",to_lang="en")
translation = translator.translate(translation)
print(translation)
