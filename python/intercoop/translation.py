from yamlns import namespace as ns

"""
# TODO

- [ ] Multiple language in constructor

"""

class Translator(object):

    def __init__(self, language='es', fallback='es'):
        self.language = language
        self.fallback = fallback
    
    def fieldTranslation(self, tree, field, lang, langfallback=None):
        fieldExpanded = field.split("/")
        try:
            fieldTraverse = tree[fieldExpanded[0]]
            for fieldElem in fieldExpanded[1:]:
                fieldTraverse = fieldTraverse[fieldElem]
        except KeyError:
            raise Exception("Invalid field '{}'".format(field))
        if lang in fieldTraverse:
            return fieldTraverse[lang]
        if langfallback in fieldTraverse:
            return fieldTraverse[langfallback]
        if langfallback:
            raise Exception("None of the '{}' or '{}' translations exist for field '{}'".format(
                lang,langfallback,field))
        raise Exception("Invalid translation '{}' for field '{}'".format(
            lang,field))

    def _translateTree(self,transTree,treeOrig,prefix,lang):
        tree = treeOrig
        prefixChopped = prefix.split("/")
        transTreeTraversed = transTree
        transTreeTraversedParent = transTree
        for e in prefixChopped:
            tree = tree[e]
            transTreeTraversed = transTreeTraversed[e]
        for e in prefixChopped[:-1]:
            transTreeTraversedParent = transTreeTraversedParent[e]
        for elem in tree:
            if type(tree[elem]) is ns:
                self._translateTree(
                    transTree,
                    treeOrig,
                    prefix+"/"+elem,
                    lang)
            elif elem == lang:
                transTreeTraversedParent[prefixChopped[-1]]=self.fieldTranslation(
                    treeOrig,
                    prefix,
                    lang)

    def translate(self, tree, lang):
        transTree = tree.copy()
        for elem in tree:
            if type(tree[elem]) is ns:
                self._translateTree(transTree,tree,elem,lang)
        return transTree

    def __call__(self, data):

        if type(data) == ns:
            # defined language
            try: return data[self.language]
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





