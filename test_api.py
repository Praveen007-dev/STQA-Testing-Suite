import pytest
import time
from playwright.sync_api import Playwright, APIRequestContext

@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> APIRequestContext:
    request_context = playwright.request.new_context(
        base_url="http://127.0.0.1:8000",
        extra_http_headers={"Accept": "application/json"}
    )
    yield request_context
    request_context.dispose()


# ==========================================
# 1. FUNCTIONAL CORRECTNESS (Happy Paths)
# ==========================================

@pytest.mark.test_id("TC-001")
def test_valid_cart_calculation(api_context: APIRequestContext):
    """Verify cart correctly calculates subtotal and 10% tax for a valid payload."""
    response = api_context.post("/cart/add", data={"item_id": "laptop_01", "quantity": 2, "price": 1000.00})
    assert response.status == 200
    assert response.json()["total_price"] == 2200.00

@pytest.mark.test_id("TC-002")
def test_float_precision_calculation(api_context: APIRequestContext):
    """Verify cart accurately handles floating point math for prices with decimals."""
    response = api_context.post("/cart/add", data={"item_id": "book_01", "quantity": 3, "price": 19.99})
    assert response.status == 200
    assert response.json()["total_price"] == pytest.approx(65.967)

@pytest.mark.test_id("TC-003")
def test_zero_price_item(api_context: APIRequestContext):
    """Verify cart processes items with 0.00 price (e.g., free promotional items)."""
    response = api_context.post("/cart/add", data={"item_id": "promo_sticker", "quantity": 1, "price": 0.0})
    assert response.status == 200
    assert response.json()["total_price"] == 0.0


# ==========================================
# 2. BOUNDARY VALUE ANALYSIS (Limits)
# ==========================================

@pytest.mark.test_id("TC-004")
def test_lower_boundary_quantity(api_context: APIRequestContext):
    """Verify API accepts the absolute minimum valid quantity (1)."""
    response = api_context.post("/cart/add", data={"item_id": "mouse_02", "quantity": 1, "price": 20.00})
    assert response.status == 200

@pytest.mark.test_id("TC-005")
def test_zero_quantity_boundary(api_context: APIRequestContext):
    """Verify API rejects a quantity of exactly zero (HTTP 422)."""
    response = api_context.post("/cart/add", data={"item_id": "mouse_02", "quantity": 0, "price": 20.00})
    assert response.status == 422

@pytest.mark.test_id("TC-006")
def test_exact_upper_boundary(api_context: APIRequestContext):
    """Verify API accepts the maximum allowed quantity limit (exactly 50)."""
    response = api_context.post("/cart/add", data={"item_id": "bulk_cables", "quantity": 50, "price": 5.00})
    assert response.status == 200

@pytest.mark.test_id("TC-007")
def test_above_upper_boundary(api_context: APIRequestContext):
    """Verify API rejects requests exceeding the hard limit of 50 items (51 items)."""
    response = api_context.post("/cart/add", data={"item_id": "bulk_cables", "quantity": 51, "price": 5.00})
    assert response.status == 400
    assert "exceeds maximum allowed limit" in response.json()["detail"].lower()

@pytest.mark.test_id("TC-008")
def test_extreme_high_quantity(api_context: APIRequestContext):
    """Verify API rejects absurdly high quantities (e.g., 99999)."""
    response = api_context.post("/cart/add", data={"item_id": "bulk_cables", "quantity": 99999, "price": 5.00})
    assert response.status == 400


# ==========================================
# 3. EDGE CASES & ERROR CONDITIONS
# ==========================================

@pytest.mark.test_id("TC-009")
def test_negative_quantity_edge_case(api_context: APIRequestContext):
    """Verify API returns HTTP 422 Unprocessable Entity for negative quantity values."""
    response = api_context.post("/cart/add", data={"item_id": "keyboard_03", "quantity": -5, "price": 50.00})
    assert response.status == 422

@pytest.mark.test_id("TC-010")
def test_missing_price_field(api_context: APIRequestContext):
    """Verify API fails gracefully (HTTP 422) when the required 'price' field is omitted."""
    response = api_context.post("/cart/add", data={"item_id": "monitor_04", "quantity": 1})
    assert response.status == 422

@pytest.mark.test_id("TC-011")
def test_missing_item_id_field(api_context: APIRequestContext):
    """Verify API fails gracefully (HTTP 422) when the required 'item_id' field is omitted."""
    response = api_context.post("/cart/add", data={"quantity": 1, "price": 100.00})
    assert response.status == 422

@pytest.mark.test_id("TC-012")
def test_missing_quantity_field(api_context: APIRequestContext):
    """Verify API fails gracefully (HTTP 422) when the required 'quantity' field is omitted."""
    response = api_context.post("/cart/add", data={"item_id": "monitor_04", "price": 100.00})
    assert response.status == 422

@pytest.mark.test_id("TC-013")
def test_invalid_data_type_quantity(api_context: APIRequestContext):
    """Verify API rejects string inputs for integer fields (quantity='two')."""
    response = api_context.post("/cart/add", data={"item_id": "cable_05", "quantity": "two", "price": 10.00})
    assert response.status == 422

@pytest.mark.test_id("TC-014")
def test_invalid_data_type_price(api_context: APIRequestContext):
    """Verify API rejects non-numeric string inputs for float fields (price='free')."""
    response = api_context.post("/cart/add", data={"item_id": "cable_05", "quantity": 1, "price": "free"})
    assert response.status == 422


# ==========================================
# 4. NON-FUNCTIONAL (Performance)
# ==========================================

@pytest.mark.test_id("TC-015")
def test_performance_benchmark(api_context: APIRequestContext):
    """Execute 50 rapid sequential requests and verify average response time is under 100ms."""
    start_time = time.time()
    
    for _ in range(50):
        response = api_context.post("/cart/add", data={"item_id": "bulk_item", "quantity": 1, "price": 5.00})
        assert response.status == 200
        
    total_time = time.time() - start_time
    avg_time_ms = (total_time / 50) * 1000
    
    # The test fails if the API takes longer than 100ms per request on average
    assert avg_time_ms < 100.0, f"Performance failed: Averaged {avg_time_ms:.2f}ms per request"