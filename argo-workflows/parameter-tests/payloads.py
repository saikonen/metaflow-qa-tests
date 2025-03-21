PAYLOADS = [
    {
        "param_a": "default value A",
        "param-b": ["a", "b"],
        "param-c": {"test": 1},
        "param-d": 123,
        "param-e": 1.23,
    },  # default values but through payload.
    {"param_a": "custom payload A", "param-b": ["C", "E"]},
    {
        "param_a": "http://example.com/test?a=123&b=test  and some values \"' '' && testing! \\",
        "param-b": [""],
    },
    # {"param-b": ["http://example.com/test?a=123&b=test  and some values \"\' '' && testing! \\"]}, # This one is problematic.
    {"param_a": "Only supplied param_a"},
    {},
]

EVENT_NAME = "params_test_event"
