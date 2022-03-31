import wikipedia


def prototype_wiki_search(request, language="ru"):
	wikipedia.set_lang(language)
	suggestions = wikipedia.search(request, results=5)
	return wikipedia.summary(suggestions[0])