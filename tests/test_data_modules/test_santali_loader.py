import os
import sys

import datasets
import pytest
from data_modules.santali.indicvoices_loader import IndicVoicesLoader

def test_loader_throws_without_token():
    # If token is False, it should throw an exception if the dataset is gated
    loader = IndicVoicesLoader()
    loader.token = False # Force token missing
    
    with pytest.raises(Exception):
        # Evaluate generator
        list(loader.stream_train())
