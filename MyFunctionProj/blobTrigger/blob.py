class Blob:

    def __init__(self, blob):
        self.blob = blob
        self.occurrences = {}

    def remove_symbols(self):
        blob = self.read_blob()
        alpha = "aàâæbcçdeéèêëfghiîïjkmnloœpqrstuùûüvwxyz'’"
        for word in blob:
            if not word.lower() in alpha and word != " ":
                blob = blob.replace(word," ")
        return blob

    def read_blob(self):
        blob = self.blob.read().decode('utf-8')
        return blob

    def word_occurrences(self):
        blob = self.remove_symbols()
        word_list = blob.split()
        for word in word_list:
            if not word in self.occurrences:
                self.occurrences[word.lower()] = 1
            else:
                self.occurrences[word.lower()] += 1
        return self.occurrences

    def word_count(self):
        keys = self.word_occurrences().keys()
        return len(keys)