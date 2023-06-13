from playwright.sync_api import sync_playwright
import pandas as pd


def main():
    with sync_playwright() as p:
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        checkin_date = '2023-07-23'
        checkout_date = '2023-07-24'

        #page_url = f'https://www.booking.com/searchresults.en-us.html?checkin={checkin_date}&checkout={checkout_date}&selected_currency=USD&ss=Paris&ssne=Paris&ssne_untouched=Paris&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_type=city&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure'
        page_url =f'https://www.booking.com/searchresults.html?ss=Louisville&ssne=Louisville&ssne_untouched=Louisville&label=en-us-booking-desktop-hdfqyDAE2wG*EqnCmUZVBgS652734911659%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-334108349%3Alp9031923%3Ali%3Adec%3Adm&aid=2311236&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=20046120&dest_type=city&checkin={checkin_date}&checkout={checkout_date}&group_adults=1&no_rooms=1&group_children=0'

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)
        page.wait_for_selector('button[aria-label="Next page"]')
        page.click('button[aria-label="Next page"]')

        page.wait_for_selector('//div[@data-testid="property-card"]', timeout=60000)


        hotels = page.locator('//div[@data-testid="property-card"]').all()
        print(f'There are: {len(hotels)} hotels.')

        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
            hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
            hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
            hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
            hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]


            hotels_list.append(hotel_dict)

        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list.xlsx', index=False)
        df.to_csv('hotels_list.csv', index=False)

        browser.close()


if __name__ == '__main__':
    main()