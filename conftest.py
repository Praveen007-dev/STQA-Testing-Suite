import pytest

def pytest_html_results_table_header(cells):
    # Insert custom headers at index 1 and 2
    cells.insert(1, "<th>Test Case ID</th>")
    cells.insert(2, "<th>Test Case Description</th>")

def pytest_html_results_table_row(report, cells):
    # Insert the data into the row
    cells.insert(1, f"<td>{getattr(report, 'tc_id', '')}</td>")
    cells.insert(2, f"<td>{getattr(report, 'tc_desc', '')}</td>")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # Only modify the report for the actual test call (ignore setup/teardown phases)
    if report.when == "call":
        # Extract docstring for Description
        docstring = item.function.__doc__
        report.tc_desc = docstring.strip() if docstring else "No description provided."
        
        # Extract custom marker for Test Case ID
        marker = item.get_closest_marker("test_id")
        report.tc_id = marker.args[0] if marker else "N/A"