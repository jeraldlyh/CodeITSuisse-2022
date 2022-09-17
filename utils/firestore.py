from firebase_admin import firestore


class Firestore:
    def __init__(self):
        self.db = firestore.AsyncClient()

        # Constants for firestore collection
        self.DNS_COLLECTION = "DNS"
        self.CACHE_DOCUMENT = "CACHE"

    async def get_lookup_table(self):
        doc_ref = self.db.collection(self.DNS_COLLECTION).document(self.CACHE_DOCUMENT)

        doc = await doc_ref.get()
        return doc.to_dict()

    async def create_lookup_table(self, lookup_table):
        doc_ref = self.db.collection(self.DNS_COLLECTION).document(self.CACHE_DOCUMENT)

        await doc_ref.set(lookup_table)
