import pytest  # type: ignore
from export import export_to_csv
from exceptions import NoDataForExportError
import csv
import os

def test_export_to_csv_with_single_model():
    """Test exporting a single object with model_dump method"""
    class MockModel:
        def model_dump(self):
            return {"name": "Stock A", "price": "100.50"}
    
    filename = "test_single.csv"
    try:
        export_to_csv(MockModel(), filename)
        
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 1
        assert rows[0]["name"] == "Stock A"
        assert rows[0]["price"] == "100.50"
    finally:
        os.remove(filename)


def test_export_to_csv_with_list_of_models():
    """Test exporting a list of objects with model_dump method"""
    class MockModel:
        def __init__(self, name, price):
            self.name = name
            self.price = price
        
        def model_dump(self):
            return {"name": self.name, "price": self.price}
    
    filename = "test_list.csv"
    try:
        data = [MockModel("Stock A", "100.50"), MockModel("Stock B", "200.75")]
        export_to_csv(data, filename)
        
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 2
        assert rows[0]["name"] == "Stock A"
        assert rows[1]["name"] == "Stock B"
    finally:
        os.remove(filename)


def test_export_to_csv_raises_error_when_no_data():
    """Test that NoDataForExportError is raised when data is empty"""
    with pytest.raises(NoDataForExportError):
        export_to_csv([], "test.csv")


def test_export_to_csv_raises_error_when_none():
    """Test that NoDataForExportError is raised when data is None"""
    with pytest.raises(NoDataForExportError):
        export_to_csv(None, "test.csv")


def test_export_to_csv_file_encoding():
    """Test that file is created with UTF-8 encoding"""
    filename = "test_encoding.csv"
    try:
        data = [{"name": "Açúcar", "price": "5,50"}]
        export_to_csv(data, filename)
        
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        
        assert "Açúcar" in content
    finally:
        os.remove(filename)