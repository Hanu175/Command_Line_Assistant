from core.completion_engine import CompletionEngine


engine = CompletionEngine()


examples = [
    "git",
    "git sta",
    "git --ver",
    "docker",
    "docker ru",
    "docker --ver",
    "py",
]


for example in examples:

    print("\n" + "=" * 60)
    print(f"INPUT: {example}")
    print("=" * 60)

    suggestions = engine.complete(example)

    if suggestions:
        for suggestion in suggestions:
            print(suggestion)
    else:
        print("No suggestions found.")