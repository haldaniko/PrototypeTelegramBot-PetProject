import wikipedia


def prototype_wiki_search(request, language="ru"):
	wikipedia.set_lang(language)
	suggestions = wikipedia.search(request, results=5) # может пригодиться, но пока что это просто для того чтобы было
	return wikipedia.summary(suggestions[0])