from .literals import TEST_RECEIVE_KEY, TEST_SEARCH_FINGERPRINT


def mock_recv_keys(self, keyserver, *keyids):
    class ImportResult:
        count = 1
        fingerprints = [TEST_SEARCH_FINGERPRINT]

    self.import_keys(TEST_RECEIVE_KEY)

    return ImportResult()
