"""
Table utility functions for ThermoProp application
Provides helper functions for table operations and data formatting
"""

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import pandas as pd

def populate_table(table: QTableWidget, data: pd.DataFrame, headers: list = None):
    """
    Populate a QTableWidget with data from a pandas DataFrame
    
    Args:
        table: QTableWidget to populate
        data: pandas DataFrame containing the data
        headers: Optional list of column headers to use
    """
    if headers:
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
    else:
        table.setColumnCount(len(data.columns))
        table.setHorizontalHeaderLabels(data.columns)
    
    table.setRowCount(len(data))
    
    for i, row in enumerate(data.itertuples(index=False)):
        for j, value in enumerate(row):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, j, item)
    
    table.resizeColumnsToContents()

def clear_table(table: QTableWidget):
    """
    Clear all data from a QTableWidget
    
    Args:
        table: QTableWidget to clear
    """
    table.setRowCount(0)
    table.setColumnCount(0)

def get_table_data(table: QTableWidget) -> pd.DataFrame:
    """
    Extract data from a QTableWidget into a pandas DataFrame
    
    Args:
        table: QTableWidget to extract data from
        
    Returns:
        pandas DataFrame containing the table data
    """
    data = []
    headers = []
    
    # Get headers
    for i in range(table.columnCount()):
        headers.append(table.horizontalHeaderItem(i).text())
    
    # Get data
    for row in range(table.rowCount()):
        row_data = []
        for col in range(table.columnCount()):
            item = table.item(row, col)
            row_data.append(item.text() if item else "")
        data.append(row_data)
    
    return pd.DataFrame(data, columns=headers)

def format_table_cell(item: QTableWidgetItem, value: float, precision: int = 4):
    """
    Format a table cell with a numeric value
    
    Args:
        item: QTableWidgetItem to format
        value: Numeric value to display
        precision: Number of decimal places to show
    """
    if isinstance(value, (int, float)):
        item.setText(f"{value:.{precision}f}")
    else:
        item.setText(str(value))
    item.setTextAlignment(Qt.AlignCenter)
