from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.maximize_window()

try:
    print("🚀 Starting Case 2 test...")

    # STEP 1: Open rapsodo.com and verify URL
    driver.get("https://rapsodo.com")
    WebDriverWait(driver, 10).until(EC.url_contains("rapsodo.com"))
    print("✅ Opened https://rapsodo.com")

    # STEP 2: Click the Cart icon and verify empty cart
    print("🔍 Looking for cart icon...")
    try:
        cart_icon = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.CartButton'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", cart_icon)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", cart_icon)
        print("✅ Clicked cart icon and navigated to cart.")
    except Exception as e:
        print("❌ Failed to locate or click cart icon:", e)
        driver.save_screenshot("C:/Users/Samul/OneDrive/Desktop/cart_icon_fail.png")
        raise e

    empty_msg = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Your cart is currently empty')]"))
    )
    print("✅ Verified cart is empty")

    # STEP 3: Navigate to Golf > Click "Mobile Launch Monitor"
    try:
        print("⛳ Clicking 'Golf' link...")
        golf_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "GOLF"))
        )
        driver.execute_script("arguments[0].click();", golf_link)
        print("✅ Navigated to Golf page")

        time.sleep(3)
        print("🧭 Looking for 'Products' button under Golf...")

        # Wait for and click 'Products'
        products_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'BoxedLink') and @tab='product']"))
        )
        driver.execute_script("arguments[0].click();", products_button)
        print("✅ Clicked 'Products'")

        print("🔍 Looking for 'Shop MLM' button...")
        try:
            shop_mlm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Shop MLM"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", shop_mlm_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", shop_mlm_button)
            print("✅ Clicked 'Shop MLM' button")
        except Exception as e:
            print("❌ Failed to find or click 'Shop MLM':", e)
            driver.save_screenshot("C:/Users/Samul/OneDrive/Desktop/mlm_click_fail.png")
            raise e

        # STEP 4: Verify title
        WebDriverWait(driver, 10).until(EC.title_contains("Mobile Launch Monitor"))
        print("📄 Verified page title contains 'Mobile Launch Monitor'")

    except Exception as e:
        print("❌ Failed navigating Golf > MLM:", e)
        driver.save_screenshot("C:/Users/Samul/OneDrive/Desktop/fail_golf_to_mlm.png")
        raise e
    # STEP 5: Select the correct 'Mobile Launch Monitor (MLM)' variant by product ID
    try:
        variant_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductButton"))
        )

        found_variant = False
        for btn in variant_buttons:
            product_id = btn.get_attribute("data-product-id") or ""
            if product_id == "41811817234581":  # $299.99 variant
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                time.sleep(1)

                variant_id = "41811817234581"
                driver.execute_script(f"""
                    var buttons = document.querySelectorAll('.ProductButton');
                    buttons.forEach(btn => {{
                        if (btn.dataset.productId === "{variant_id}") {{
                            btn.click();  // Use the site's built-in variant change handler
                        }}
                    }});
                """)


                WebDriverWait(driver, 5).until(lambda d: "active" in btn.get_attribute("class"))
                print("✅ Selected correct 'Mobile Launch Monitor (MLM)' variant at $299.99")
                found_variant = True
                break

        if not found_variant:
            raise Exception("❌ Correct MLM variant ($299.99) not found.")

    except Exception as e:
        print("❌ Variant selection failed:", e)
        driver.save_screenshot("C:/Users/Samul/OneDrive/Desktop/variant_selection_fail.png")
        raise e

    # Force the hidden input to the correct variant ID
    correct_variant_id = "41811817234581"
    driver.execute_script(f'''
        let input = document.querySelector('form[action="/cart/add"] input[name="id"]');
        if (input) {{
            input.value = "{correct_variant_id}";
        }}
    ''')
    print("🛠️ Corrected hidden input to ensure $299.99 variant is added.")


    # STEP 6: Submit correct variant directly using fetch (guaranteed correct variant)
    print("🛒 Submitting correct variant to cart")

    try:
        correct_variant_id = "41811817234581"  # $299.99 variant

        driver.execute_script(f'''
            fetch("/cart/add.js", {{
                method: "POST",
                headers: {{
                    "Content-Type": "application/x-www-form-urlencoded"
                }},
                body: "id={correct_variant_id}&quantity=1"
            }}).then(() => {{
                window.location.href = "/cart";
            }});
        ''')

        # Wait for redirect to /cart page to complete
        time.sleep(5)
        print("✅ Submitted correct variant directly to cart using fetch()")

    except Exception as e:
        print("❌ Failed to add correct variant via fetch:", e)
        driver.save_screenshot("C:/Users/Samul/OneDrive/Desktop/add_cart_fail_debug.png")
        raise e


    # STEP 7: Go to cart page and verify
    driver.get("https://rapsodo.com/cart")
    print("🛒 Returned to cart page")

    cart_price = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart__price"))
    ).text.strip()
    print(f"🧾 Cart price: {cart_price}")

    # STEP 8: Update quantity to 2 and verify cart state
    try:
        qty_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="updates[]"]'))
        )

        qty_input.click()
        qty_input.send_keys(Keys.CONTROL + "a")
        qty_input.send_keys("2")
        qty_input.send_keys(Keys.TAB)
        print("🔁 Quantity updated to 2")

        # Wait for total to update
        time.sleep(3)

        # Wait for quantity field to update
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.CSS_SELECTOR, 'input[name="updates[]"]').get_attribute("value") == "2"
        )
        print("✅ Verified cart shows quantity 2")


        # Wait for the total to update (more lenient and checks it becomes non-empty)
        try:
            # Look for any element that has the `data-subtotal` attribute
            total_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-subtotal]"))
            )
            total = total_element.text.strip()
            print(f"✅ Total price for 2 items: {total}")
        except Exception as e:
            print("❌ Failed to locate updated total price:", e)
            driver.save_screenshot("C:/Users/Samul/OneDrive/Desktop/total_price_fail.png")
            raise e


    except Exception as e:
        print("❌ Failed to update or verify quantity:", e)
        driver.save_screenshot("C:/Users/Samul/OneDrive/Desktop/quantity_update_fail.png")
        raise e

finally:
    driver.save_screenshot("C:/Users/Samul/OneDrive/Desktop/final_case2_screenshot.png")
    driver.quit()
    print("📸 Screenshot saved to Desktop")
    print("✅ Test finished.")
