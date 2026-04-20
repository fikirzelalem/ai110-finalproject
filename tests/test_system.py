"""
Test harness for Cadence AI.
Runs predefined inputs through retriever and guardrail and prints a pass/fail summary.
"""

from src.retriever import load_docs, load_songs_as_docs, retrieve
from src.guardrail import check

DOCS_DIR = "docs"
CSV_PATH = "docs/songs.csv"

TEST_CASES = [
    {
        "name": "Chill lofi query should retrieve docs",
        "query": "something chill and lofi for studying",
        "expect_retrieval": True,
        "expect_guardrail": True,
    },
    {
        "name": "High energy pop query should retrieve docs",
        "query": "high energy pop song for working out",
        "expect_retrieval": True,
        "expect_guardrail": True,
    },
    {
        "name": "Off-topic query should be blocked by guardrail",
        "query": "what do you think about politics",
        "expect_retrieval": True,
        "expect_guardrail": False,
    },
    {
        "name": "Nonsense query should fail guardrail due to no retrieval",
        "query": "xyzzy blorp flibbet",
        "expect_retrieval": False,
        "expect_guardrail": False,
    },
    {
        "name": "Mood-based query should retrieve mood docs",
        "query": "I want something moody and dark for a night drive",
        "expect_retrieval": True,
        "expect_guardrail": True,
    },
    {
        "name": "Genre query should retrieve genre docs",
        "query": "recommend a good rock song",
        "expect_retrieval": True,
        "expect_guardrail": True,
    },
]


def run_tests():
    docs = load_docs(DOCS_DIR) + load_songs_as_docs(CSV_PATH)

    passed = 0
    failed = 0

    print("\n" + "=" * 60)
    print("Cadence AI — Test Harness")
    print("=" * 60)

    for i, case in enumerate(TEST_CASES, 1):
        query = case["query"]
        retrieved = retrieve(query, docs, top_k=3)
        guardrail_passed, reason = check(query, retrieved)

        retrieval_ok = (len(retrieved) > 0) == case["expect_retrieval"]
        guardrail_ok = guardrail_passed == case["expect_guardrail"]

        result = "PASS" if retrieval_ok and guardrail_ok else "FAIL"
        if result == "PASS":
            passed += 1
        else:
            failed += 1

        print(f"\n[{i}] {case['name']}")
        print(f"    Query: \"{query}\"")
        print(f"    Retrieved {len(retrieved)} doc(s) | Guardrail passed: {guardrail_passed}")
        if not guardrail_passed and reason:
            print(f"    Guardrail reason: {reason}")
        print(f"    Result: {result}")

    print("\n" + "=" * 60)
    print(f"Results: {passed}/{passed + failed} passed")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_tests()
