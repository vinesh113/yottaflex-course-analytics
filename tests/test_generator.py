from generator.generate_all import generate


def test_generator_is_reproducible(tmp_path):
    first = generate("starter", 123, tmp_path / "one")
    second = generate("starter", 123, tmp_path / "two")
    assert first["counts"] == second["counts"]
    assert first["files"]["learners"]["sha256"] == second["files"]["learners"]["sha256"]
    assert first["files"]["activity_events"]["sha256"] == second["files"]["activity_events"]["sha256"]


def test_required_ground_truth_scenarios(tmp_path):
    manifest = generate("starter", 123, tmp_path)
    assert manifest["counts"]["ground_truth"] == 4
