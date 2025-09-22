class TrieNode:
    """
    A node in the Trie data structure.
    """
    def __init__(self):
        # Dictionary to store child nodes
        # Key: character, Value: TrieNode
        self.children = {}
        
        # Flag to mark the end of a word/sequence
        self.is_end_of_word = False
        
        # Optional value that can be associated with a complete word/sequence
        self.value = None
        
        # Store the complete word at terminal nodes
        self.word = None
        
        # Store original words with proper capitalization
        self.original_words = []


class Trie:
    """
    A Trie data structure for efficient storage and retrieval of sequences (e.g., words, strings).
    This implementation can be easily extended for different use cases.
    """
    def __init__(self):
        """Initialize an empty Trie with a root node."""
        self.root = TrieNode()
    
    def insert(self, key, value=None):
        """
        Insert a key into the trie.
        
        Args:
            key: The sequence to insert (e.g., a string).
            value: Optional value to associate with the key.
        """
        node = self.root
        
        # Traverse the trie for each character in the key
        for char in key:
            # If character not in current node's children, add a new node
            if char not in node.children:
                node.children[char] = TrieNode()
            
            # Move to the child node
            node = node.children[char]
        
        # Mark the end of the key
        node.is_end_of_word = True
        
        # Store the associated value if provided
        if value is not None:
            node.value = value
            
        # Store the complete word at the terminal node
        node.word = key
    
    def search(self, key):
        """
        Search for a key in the trie.
        
        Args:
            key: The sequence to search for.
            
        Returns:
            tuple: (is_found, value, word)
                - is_found: True if the key exists as a complete word, False otherwise.
                - value: The value associated with the key if it exists, None otherwise.
                - word: The complete word stored at the terminal node
        """
        node = self.root
        
        # Traverse the trie for each character in the key
        for char in key:
            # If character not found in current level, key doesn't exist
            if char not in node.children:
                return False, None, None
            
            # Move to the child node
            node = node.children[char]
        
        # Return whether the key is a complete word, its associated value, and the stored word
        return node.is_end_of_word, node.value, node.word
    
    def starts_with(self, prefix):
        """
        Check if there is any key with the given prefix.
        
        Args:
            prefix: The prefix to search for.
            
        Returns:
            bool: True if there is any key with the given prefix, False otherwise.
        """
        node = self.root
        
        # Traverse the trie for each character in the prefix
        for char in prefix:
            # If character not found in current level, prefix doesn't exist
            if char not in node.children:
                return False
            
            # Move to the child node
            node = node.children[char]
        
        # Prefix exists
        return True
    
    def get_all_with_prefix(self, prefix):
        """
        Get all keys with the given prefix.
        
        Args:
            prefix: The prefix to search for.
            
        Returns:
            list: A list of (key, value) tuples for all keys that start with the prefix.
        """
        result = []
        node = self.root
        
        # Traverse to the node representing the prefix
        for char in prefix:
            if char not in node.children:
                return result
            node = node.children[char]
        
        # Use DFS to find all words starting with the prefix
        self._dfs(node, prefix, result)
        
        return result
    
    def _dfs(self, node, current_prefix, result):
        """
        Depth-first search helper function for collecting all words with a prefix.
        
        Args:
            node: The current TrieNode.
            current_prefix: The prefix built so far.
            result: The list to store results.
        """
        if node.is_end_of_word:
            # Use the stored complete word if available
            word = node.word if node.word else current_prefix
            result.append((word, node.value))
        
        for char, child_node in node.children.items():
            self._dfs(child_node, current_prefix + char, result)
    
    def delete(self, key):
        """
        Delete a key from the trie.
        
        Args:
            key: The key to delete.
            
        Returns:
            bool: True if the key was deleted, False if it didn't exist.
        """
        return self._delete_helper(self.root, key, 0)
    
    def _delete_helper(self, node, key, depth):
        """
        Recursive helper function for deleting a key.
        
        Args:
            node: Current TrieNode
            key: Key to delete
            depth: Current depth in the trie
            
        Returns:
            bool: True if the node should be deleted, False otherwise
        """
        # Base case: reached the end of the key
        if depth == len(key):
            # Key doesn't exist as a complete word
            if not node.is_end_of_word:
                return False
            
            # Unmark as end of word
            node.is_end_of_word = False
            node.value = None
            
            # Return True if this node has no children, indicating it can be deleted
            return len(node.children) == 0
        
        char = key[depth]
        
        # If character doesn't exist in current node's children
        if char not in node.children:
            return False
        
        # Recursively delete in the child node
        should_delete_child = self._delete_helper(node.children[char], key, depth + 1)
        
        # If child should be deleted
        if should_delete_child:
            del node.children[char]
            # Return True if this node has no other children and is not the end of another word
            return len(node.children) == 0 and not node.is_end_of_word
        
        return False