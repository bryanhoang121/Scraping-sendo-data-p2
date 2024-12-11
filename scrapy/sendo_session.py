from playwright.sync_api import sync_playwright


def fetch_product_links(url: str, scrolldown: int = 4):
    """
    Fetch and render the main page using Playwright, then extract product links.

    Args:
        url (str): The URL of the page to scrape.
        scrolldown (int): Number of times to scroll down to load more content.

    Returns:
        list: A list of product URLs extracted from the page.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=False for debugging
        page = browser.new_page()
        page.goto(url, timeout=100000)

        # Scroll down to load dynamic content
        for _ in range(scrolldown):
            page.mouse.wheel(0, 10)  # Scroll down
            page.wait_for_timeout(5000)  # Allow content to load

        # Wait for at least one product container to ensure content is loaded
        page.wait_for_selector('//div[contains(@class, "d7ed-d4keTB")]', timeout=10000)

        # Extract links using the corrected XPath
        links = page.locator('//div[contains(@class, "d7ed-d4keTB") and contains(@class, "d7ed-OoK3wU")]//a[@href]')
        product_links = [link.get_attribute("href") for link in links.all()]  # Extract href attributes

        print(f"Found {len(product_links)} product links.")
        browser.close()
        for product_link in product_links:
            print(product_link)
        return product_links

