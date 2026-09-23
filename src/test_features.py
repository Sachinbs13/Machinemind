from features import engineer_features


def test_power_calculation():
    result = engineer_features(300.0, 310.0, 1500.0, 40.0, 10.0, "M")
    assert result["Power [W]"] == 1500.0 * 40.0


def test_temp_difference_calculation():
    result = engineer_features(300.0, 310.0, 1500.0, 40.0, 10.0, "M")
    assert result["Temp difference [K]"] == 10.0


def test_strain_calculation():
    result = engineer_features(300.0, 310.0, 1500.0, 40.0, 10.0, "M")
    assert result["Strain [Nm·min]"] == 400.0


def test_type_m_sets_correct_flags():
    result = engineer_features(300.0, 310.0, 1500.0, 40.0, 10.0, "M")
    assert result["Type_M"] == 1
    assert result["Type_L"] == 0


def test_type_l_sets_correct_flags():
    result = engineer_features(300.0, 310.0, 1500.0, 40.0, 10.0, "L")
    assert result["Type_M"] == 0
    assert result["Type_L"] == 1


def test_type_h_is_the_baseline_with_no_flags():
    result = engineer_features(300.0, 310.0, 1500.0, 40.0, 10.0, "H")
    assert result["Type_M"] == 0
    assert result["Type_L"] == 0