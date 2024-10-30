"""
    This script is free to use under the Free to Use license.
    Author: @OnlineBackSoon
    Changing Name and Claiming at Your own or selling for money mean you have no dick to fuck your wife. depending on others dick
    Attribution appreciated but not required.
"""

import os
import sys
required_modules = ['aiohttp', 'asyncio', 'json', 'uuid']
def install_modules(modules):
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            print(f"{module} not found. Installing...")
            os.system(f"{sys.executable} -m pip install {module}")
            print(f"{module} installed successfully.")
install_modules(required_modules)


import aiohttp
import asyncio
import json
import uuid


def parseX(data, start, end):
    try:
        star = data.index(start) + len(start)
        last = data.index(end, star)
        return data[star:last]
    except ValueError:
        return "None"


async def make_request(
    session,
    url,
    method="POST",
    params=None,
    headers=None,
    data=None,
    json=None,
):
    async with session.request(
        method,
        url,
        params=params,
        headers=headers,
        data=data,
        json=json,
    ) as response:
        return await response.text()


async def heroku(cards):
    cc, mon, year, cvv = cards.split("|")
    guid = str(uuid.uuid4())
    muid = str(uuid.uuid4())
    sid = str(uuid.uuid4())

    async with aiohttp.ClientSession() as my_session:
        headers = {
            "accept": "application/vnd.heroku+json; version=3",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "Bearer HRKU-e5235dea-74c4-43f5-85f5-658edadc7cac",  # Replace WIth Your Own Heroku API Key. https://dashboard.heroku.com/account
            "origin": "https://dashboard.heroku.com",
            "priority": "u=1, i",
            "referer": "https://dashboard.heroku.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "x-heroku-requester": "dashboard",
            "x-origin": "https://dashboard.heroku.com",
        }

        req = await make_request(
            my_session,
            url="https://api.heroku.com/account/payment-method/client-token",
            headers=headers,
        )
        client_secret = parseX(req, '"token":"', '"')

        headers2 = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://js.stripe.com",
            "priority": "u=1, i",
            "referer": "https://js.stripe.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        }

        data = {
            "type": "card",
            "billing_details[name]": "Ahmed Afnan",
            "billing_details[address][city]": "Anchorage",
            "billing_details[address][country]": "US",
            "billing_details[address][line1]": "245 W 5th Ave",
            "billing_details[address][postal_code]": "99501",
            "billing_details[address][state]": "AK",
            "card[number]": cc,
            "card[cvc]": cvv,
            "card[exp_month]": mon,
            "card[exp_year]": year,
            "guid": guid,
            "muid": muid,
            "sid": sid,
            "pasted_fields": "number",
            "payment_user_agent": "stripe.js/4b35ef0d67; stripe-js-v3/4b35ef0d67; split-card-element",
            "referrer": "https://dashboard.heroku.com",
            "time_on_page": "403570",
            "key": "pk_live_51KlgQ9Lzb5a9EJ3IaC3yPd1x6i9e6YW9O8d5PzmgPw9IDHixpwQcoNWcklSLhqeHri28drHwRSNlf6g22ZdSBBff002VQu6YLn",
        }

        req2 = await make_request(
            my_session,
            f"https://api.stripe.com/v1/payment_methods",
            headers=headers2,
            data=data,
        )

        if "pm_" not in req2:
            print(req2)

        # ---------------------------------------------------------------------------------------
        else:
            json_sec = json.loads(req2)
            pmid = json_sec["id"]
            piid = client_secret.split("_secret_")[0]

            headers3 = {
                "accept": "application/json",
                "accept-language": "en-US,en;q=0.9",
                "content-type": "application/x-www-form-urlencoded",
                "origin": "https://js.stripe.com",
                "priority": "u=1, i",
                "referer": "https://js.stripe.com/",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            }
            data3 = {
                "payment_method": pmid,
                "expected_payment_method_type": "card",
                "use_stripe_sdk": "true",
                "key": "pk_live_51KlgQ9Lzb5a9EJ3IaC3yPd1x6i9e6YW9O8d5PzmgPw9IDHixpwQcoNWcklSLhqeHri28drHwRSNlf6g22ZdSBBff002VQu6YLn",
                "client_secret": client_secret,
            }

            req3 = await make_request(
                my_session,
                url=f"https://api.stripe.com/v1/payment_intents/{piid}/confirm",
                headers=headers3,
                data=data3,
            )

            ljson = json.loads(req3)
            if '"status": "succeeded"' in req3:
                print("Card Added")
            if "decline_code" in req3:
                errorm = ljson["error"]["decline_code"]
                print(f"{cards} - {errorm}")
            elif "requires_action" in req3:
                print(f"{cards} - requires_action")
            elif "error" in req3:
                errorm = ljson["error"]["message"]
                print(f"{cards} - {errorm}")
            else:
                print(req3)
        # ---------------------------------------------------------------------------------------


async def main():
    try:
        with open("cards.txt", "r") as file:
            for line in file:
                cards = line.strip()
                result = await heroku(cards)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
