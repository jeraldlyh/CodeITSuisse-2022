from firebase_admin import firestore


class Firestore:
    def __init__(self):
        self.db = firestore.AsyncClient()

        # Constants for firestore collection
        self.DNS_COLLECTION = "DNS"
        self.CACHE_DOCUMENT = "CACHE"
        self.SWIZZ_COLLECTION = "SWIZZ"
        self.SWIZZ_DOCUMENT = "SWIZZ"

    def get_doc_ref(self, collection_name, document_name):
        return self.db.collection(collection_name).document(self.CACHE_DOCUMENT)

    async def get_lookup_table(self):
        doc_ref = self.get_doc_ref(self.DNS_COLLECTION, self.CACHE_DOCUMENT)

        doc = await doc_ref.get()
        return doc.to_dict()

    async def create_lookup_table(self, lookup_table):
        doc_ref = self.get_doc_ref(self.DNS_COLLECTION, self.CACHE_DOCUMENT)

        await doc_ref.set(lookup_table)

    async def create_swizz_data(self, data):
        doc_ref = self.get_doc_ref(self.SWIZZ_COLLECTION, self.SWIZZ_DOCUMENT)

        await doc_ref.set(data)
