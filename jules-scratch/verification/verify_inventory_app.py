from playwright.sync_api import Page, expect
import os

def test_inventory_app_flow(page: Page):
    """
    This test verifies the core functionality of the inventory app:
    1. Adding a tool to the inventory.
    2. Checking out a tool to a person.
    3. Verifying that the UI updates correctly at each step.
    """
    # 1. Arrange: Go to the application's HTML file.
    # Construct the file path to be absolute.
    file_path = os.path.abspath("index.html")
    page.goto(f"file://{file_path}")

    # 2. Act: Add a new tool to the inventory.
    page.get_by_placeholder("Tool Name").fill("Drill")
    page.get_by_placeholder("Quantity").fill("3")
    page.get_by_role("button", name="Add Tool").click()

    # 3. Assert: Verify the tool was added correctly.
    expect(page.locator("#tool-list li")).to_have_text("Drill (Qty: 3)Remove")

    # 4. Act: Check out the newly added tool.
    page.get_by_placeholder("Person's Name").fill("Jane Smith")
    # The select dropdown is now populated, so we can select the tool.
    page.get_by_role("combobox").select_option(label="Drill (Qty: 3)")
    page.get_by_role("button", name="Checkout Tool").click()

    # 5. Assert: Verify the checkout was successful and the UI updated.
    # The checked-out list should show the new entry.
    expect(page.locator("#checked-out-list li")).to_have_text("Drill - Jane SmithReturn")
    # The inventory list should show the updated quantity.
    expect(page.locator("#tool-list li")).to_have_text("Drill (Qty: 2)Remove")
    # The history should reflect the checkout.
    expect(page.locator("#history-list li")).to_contain_text("Checkout: Drill to Jane Smith on")

    # 6. Screenshot: Capture the final state for visual verification.
    page.screenshot(path="jules-scratch/verification/verification.png")