from playwright.sync_api import sync_playwright
import os

def run(playwright):
    print(f"Current working directory: {os.getcwd()}")
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        print("Navigating to Cars page...")
        page.goto("http://localhost:3000/routes/cars")
        print("Taking screenshot of Cars page...")
        page.screenshot(path="/app/jules-scratch/verification/cars_page.png")
        print("Screenshot of Cars page taken successfully.")

        print("Navigating to Square page...")
        page.goto("http://localhost:3000/routes/square")
        print("Taking screenshot of Square page...")
        page.screenshot(path="/app/jules-scratch/verification/square_page.png")
        print("Screenshot of Square page taken successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
