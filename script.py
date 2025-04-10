import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {"color_scheme": "dark"}

def test_example(page: Page) -> None:
    page.goto("https://isgp.hik-connect.com/views/login/index.html?returnUrl=http://isgp.hik-connect.com/devices/page&r=1383890617853788334&host=isgp.hik-connect.com&from=c17392dc2e6c405a931b#/main/overview")

    page.get_by_text("Log In").click()
    page.get_by_role("textbox", name="Email/Account").fill("nexia.co@gmail.com")
    page.get_by_role("textbox", name="Password").fill("N3x!@2025NeXia")
    page.get_by_role("button", name="Login").click()

    # Wait for the login to complete
    page.wait_for_load_state("networkidle")

    # Get cookies
    cookies = page.context.cookies()
    print(cookies)  # Print cookies to the console

    # Optionally, save cookies to a file
    import json
    with open("cookies.json", "w") as f:
        json.dump(cookies, f, indent=4)

    # Continue with further actions

test_example()