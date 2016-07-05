from yamlns import namespace as ns

class NsTranslator(object):
    
    def fieldTranslation(self, tree, field, lang, langfallback=None):
        fieldExpanded = field.split("/")
        try:
            fieldTraverse = tree[fieldExpanded[0]]
            for fieldElem in fieldExpanded[1:]:
                fieldTraverse = fieldTraverse[fieldElem]
        except KeyError:
            raise Exception("Invalid field '{}'".format(field))
        if lang in fieldTraverse:
            translation = fieldTraverse[lang]
        elif langfallback in fieldTraverse:
            translation = fieldTraverse[langfallback]
        elif langfallback:
            raise Exception("None of the '{}' or '{}' translations exist for field '{}'".format(
                lang,langfallback,field))
        else:
            raise Exception("Invalid translation '{}' for field '{}'".format(
                lang,field))
        return translation

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

    def translateTree(self, tree, lang):
        transTree = tree.copy()
        for elem in tree:
            if type(tree[elem]) is ns:
                self._translateTree(transTree,tree,elem,lang)
        return transTree
