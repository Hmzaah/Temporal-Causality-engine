from temporal_causality_engine.benchmark import adjacency_from_chain


def test_ground_truth_shape():
    adj = adjacency_from_chain(4)
    assert adj.shape == (4, 4)
    assert adj.iloc[0, 1] == True
    assert adj.iloc[1, 2] == True
    assert adj.iloc[2, 3] == True
    assert adj.iloc[0, 2] == False
