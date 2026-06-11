"""
Migration validation tests.
Run after each phase to confirm nothing broke.

Usage:
    python scripts/test_migration.py --phase 2
    python scripts/test_migration.py --phase 3
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def _make_dummy_config(use_v2: bool):
    """Minimal config object for tests — no .env needed."""
    class Cfg:
        EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
        CHUNK_SIZE = 512
        CHUNK_OVERLAP = 50
        TOP_K_RESULTS = 3
        RETRIEVAL_SCORE_THRESHOLD = 0.0
        VECTOR_STORE_DIR = "data/vectorstore_test"
        USE_V2_EMBEDDINGS = use_v2
    return Cfg()


SAMPLE_CHUNKS = [
    "Pakistan economy grew in 2024 and exports increased significantly.",
    "Automobile industry car sales reached record high this year.",
    "Python programming language is most used in data science.",
    "Machine learning models require GPU for faster training.",
    "RAG systems are based on retrieval augmented generation architecture.",
]

SAMPLE_QUERY = "vehicle and car industry news"


def test_v1_imports():
    print("\n[Phase 2] V1 import test...")
    from src.engine.vector_store import DocumentVectorStore, build_vector_store
    cfg = _make_dummy_config(use_v2=False)
    store = build_vector_store(cfg)
    assert "DocumentVectorStore" in type(store).__name__, "Expected V1 store"
    print("  PASS — V1 loads via build_vector_store()")


def test_v2_imports():
    print("\n[Phase 2] V2 import test...")
    from src.engine.vector_store import build_vector_store
    cfg = _make_dummy_config(use_v2=True)
    store = build_vector_store(cfg)
    assert "V2" in type(store).__name__, "Expected V2 store"
    print("  PASS — V2 loads via build_vector_store()")


def test_v1_end_to_end():
    print("\n[Phase 2] V1 end-to-end (chunks → embed → search)...")
    from src.engine.vector_store import DocumentVectorStore
    cfg = _make_dummy_config(use_v2=False)
    store = DocumentVectorStore(cfg)

    vectorstore = store.create_embeddings(SAMPLE_CHUNKS)
    results = store.search(SAMPLE_QUERY, vectorstore, k=2)

    assert len(results) == 2, f"Expected 2 results, got {len(results)}"
    assert hasattr(results[0][0], "page_content"), "Result missing page_content"
    print(f"  PASS — top result: '{results[0][0].page_content[:60]}...'")


def test_v2_end_to_end():
    print("\n[Phase 2] V2 end-to-end (chunks → FAISS → hybrid search)...")
    from src.engine.vector_store_v2 import DocumentVectorStoreV2
    cfg = _make_dummy_config(use_v2=True)
    store = DocumentVectorStoreV2(cfg)

    vectorstore = store.create_embeddings(SAMPLE_CHUNKS)
    results = store.search(SAMPLE_QUERY, vectorstore, k=2)

    assert len(results) > 0, "No results returned from V2 search"
    assert hasattr(results[0][0], "page_content"), "Result missing page_content"
    assert 0.0 <= results[0][1] <= 1.0, f"Score out of range: {results[0][1]}"

    # Key assertion: semantic match — "car" matches query about "vehicle/car"
    top_content = results[0][0].page_content
    print(f"  PASS — top result: '{top_content[:60]}...'")
    print(f"  Score: {results[0][1]:.3f}")


def test_v2_save_load():
    print("\n[Phase 2] V2 save/load test...")
    import shutil
    from src.engine.vector_store_v2 import DocumentVectorStoreV2

    cfg = _make_dummy_config(use_v2=True)
    store = DocumentVectorStoreV2(cfg)

    vs = store.create_embeddings(SAMPLE_CHUNKS)
    store.save_vectorstore(vs, "test_doc")

    loaded = store.load_vectorstore("test_doc")
    assert loaded is not None, "Failed to load saved vectorstore"

    results = store.search(SAMPLE_QUERY, loaded, k=2)
    assert len(results) > 0, "No results after reload"
    print("  PASS — save/load/search cycle works")

    # cleanup
    shutil.rmtree(Path(cfg.VECTOR_STORE_DIR) / "test_doc", ignore_errors=True)


def test_flag_routing():
    print("\n[Phase 3] Flag routing test...")
    from src.engine.vector_store import build_vector_store
    from src.engine.vector_store_v2 import DocumentVectorStoreV2
    from src.engine.vector_store import DocumentVectorStore

    v1 = build_vector_store(_make_dummy_config(use_v2=False))
    v2 = build_vector_store(_make_dummy_config(use_v2=True))

    assert isinstance(v1, DocumentVectorStore), "Flag=False should return V1"
    assert isinstance(v2, DocumentVectorStoreV2), "Flag=True should return V2"
    print("  PASS — flag routes correctly to V1/V2")


PHASE_TESTS = {
    2: [test_v1_imports, test_v2_imports, test_v1_end_to_end,
        test_v2_end_to_end, test_v2_save_load],
    3: [test_v1_imports, test_v2_imports, test_flag_routing,
        test_v2_end_to_end, test_v2_save_load],
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, choices=[2, 3], default=2)
    args = parser.parse_args()

    tests = PHASE_TESTS[args.phase]
    passed = failed = 0

    print(f"\n{'='*50}")
    print(f"  Running Phase {args.phase} migration tests")
    print(f"{'='*50}")

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  FAIL — {test.__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"  Results: {passed} passed, {failed} failed")
    print(f"{'='*50}\n")
    sys.exit(0 if failed == 0 else 1)
