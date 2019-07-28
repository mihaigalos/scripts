py_library(
  name = "lib",
  srcs = [ "src/getnextmovie.py" ],
  imports = [ "src" ],
  visibility = [ "//visibility:public" ],
)

py_test(
    name = "test_getnextmovie_unit",
    srcs = [
        "test/unit/test_getnextmovie_unit.py",
    ],
    deps = [
        ":lib",
    ],
)

py_test(
    name = "test_getnextmovie_contract",
    srcs = [
        "test/contract/test_getnextmovie_contract.py",
    ],
    deps = [
        ":lib",
    ],
)

py_test(
    name = "test_getnextmovie_integration",
    srcs = [
        "test/integration/test_getnextmovie_integration.py",
    ],
    deps = [
        ":lib",
    ],
)
