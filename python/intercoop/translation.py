from yamlns import namespace as ns

class TranslatePeers(object):
    def __init__(self,peers):
        self.peers=peers
    
    def fieldTranslation(self, peername, field, lang, langfallback=None):
        peerData = self.peers.get(peername)
        fieldExpanded = field.split("/")
        try:
            fieldTraverse = peerData[fieldExpanded[0]]
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

    def _translateTree(self,transTree,peer,prefix,lang):
        tree = self.peers.get(peer)
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
                    peer,
                    prefix+"/"+elem,
                    lang)
            elif elem == lang:
                transTreeTraversedParent[prefixChopped[-1]]=self.fieldTranslation(
                    peer,
                    prefix,
                    lang)

    def translatePeer(self, peer, lang):
        tree = self.peers.get(peer)
        transTree = tree.copy()
        for elem in tree:
            if type(tree[elem]) is ns:
                self._translateTree(transTree,peer,elem,lang)
        return transTree
