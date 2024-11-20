class TrieNode:
    def __init__(self):
        self.children = {}
        self.value = None 

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, key, value):

        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.value = value

    def search(self, key):

        node = self.root
        for char in key:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.value

    def delete(self, key):

        def _delete(node, key, depth):
            if not node:
                return False

            # Caso base: chegou ao final da chave
            if depth == len(key):
                if node.value is not None:
                    node.value = None  # Remove o valor associado
                    return len(node.children) == 0  # Verifica se o nó pode ser deletado
                return False

            char = key[depth]
            if char in node.children:
                can_delete_child = _delete(node.children[char], key, depth + 1)

                if can_delete_child:
                    del node.children[char]
                    return len(node.children) == 0 and node.value is None
            return False

        _delete(self.root, key, 0)
