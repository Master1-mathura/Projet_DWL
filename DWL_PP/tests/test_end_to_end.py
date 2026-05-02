from playwright.sync_api import sync_playwright, Playwright
import time
import requests
#https://playwright.dev/python/docs/api/class-playwright


def wait_for_server(url, timeout=240):
    for _ in range(timeout):
        try:
            r = requests.get(url)
            if r.status_code < 500:
                return True
        except:
            pass
        time.sleep(1)

    raise Exception(f"Server not ready: {url}")

def test_login_e2e():
    if not wait_for_server("http://host.docker.internal:4000"):
        raise Exception("Le serveur localhost:4000 n'est pas accessible")
    with sync_playwright() as p:
        chromium = p.chromium
        browser = chromium.launch()
        page = browser.new_page()

        #Creation compte
        page.goto("http://host.docker.internal:8000/Register.php")
        page.fill('input[name="username"]', "Testeur1")
        page.fill('input[name="password"]', "123456")
        page.screenshot(path = "tests/screenshots/creation_success.png")
        page.click('button[name="register"]')
        page.wait_for_load_state("networkidle")

        page.click("text=Log in")

        page.fill('input[name="username"]',"Testeur1")
        page.fill('input[name="password"]',"123456")

        page.click('button[name="connexion"]')
        page.wait_for_timeout(1000)
        page.screenshot(path="tests/screenshots/login_success.png")

        assert "login" not in page.url.lower()

        browser.close()

def test_search_e2e():
    if not wait_for_server("http://host.docker.internal:4000"):
        raise Exception("Le serveur localhost:4000 n'est pas accessible")
    with sync_playwright() as p:
        chromium = p.chromium
        browser = chromium.launch()
        page = browser.new_page()

        page.goto("http://host.docker.internal:8000/MoteurRecherche.php")
        page.fill('input[name="requete"]', "I am afraid of spiders")
        page.get_by_role("button", name="Search").click()

        page.wait_for_selector(".result-row")
        page.locator(".result-row .open-btn").last.click()

        page.wait_for_selector("#box-detail", state="visible")

        page.wait_for_selector("#box-poster-container img", state="visible")
        page.screenshot(path="tests/screenshots/search_success.png")
        title = page.inner_text("#box-title")

        assert title != ""

        browser.close()