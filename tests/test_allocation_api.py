from ridi_audit import AllocationReport, compare_allocations


def test_compare_allocations_equal_capacity():
    report = compare_allocations(["a", "b", "c"], ["a", "b", "d"])
    assert isinstance(report, AllocationReport)
    assert report.same_capacity is True
    assert report.before_size == 3
    assert report.after_size == 3
    assert report.overlap == 2
    assert report.changed_slots == 1
    assert report.removed_ids == ("c",)
    assert report.added_ids == ("d",)
    assert abs(report.ridi - 0.5) < 1e-12
    assert "RIDI Allocation Comparison" in str(report)
    assert "# RIDI allocation comparison" in report.to_markdown()


def test_compare_allocations_different_capacity():
    report = compare_allocations(["a", "b"], ["a", "b", "c"])
    assert report.same_capacity is False
    assert report.changed_slots is None
    assert report.overlap == 2
    assert report.to_dict(include_ids=False)["changed_slots"] is None


def test_compare_allocations_accepts_generators():
    report = compare_allocations((x for x in [1, 2, 3]), (x for x in [1, 3, 4]))
    assert report.removed_ids == ("2",)
    assert report.added_ids == ("4",)


def test_compare_allocations_rejects_duplicate_normalized_ids():
    try:
        compare_allocations([1, "1"], ["a", "b"])
    except ValueError as exc:
        assert "unique after string conversion" in str(exc)
    else:
        raise AssertionError("string-normalized duplicates should fail")


def test_compare_allocations_rejects_plain_string():
    try:
        compare_allocations("abc", ["a", "b", "c"])
    except TypeError as exc:
        assert "iterable of identities" in str(exc)
    else:
        raise AssertionError("plain strings should fail")
