from bs4 import BeautifulSoup


class Parser:

    def parse(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        result = {}

        grants = soup.select(".cat_item")

        for grant in grants:
            title = grant.select_one(".pt a")
            tags = grant.select(".tag_item")
            amount = grant.select_one(".price_new")

            if not title:
                continue

            title = title.get_text(" ", strip=True)

            tags = [
                tag.get_text(" ", strip=True).lstrip("#").strip()
                for tag in tags
            ]

            amount = amount.get_text(" ", strip=True).replace("\xa0", " ") if amount else None

            result[title] = {
                "tags": tags,
                "amount": amount,
            }

        return result