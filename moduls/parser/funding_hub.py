from urllib.parse import urljoin

from bs4 import BeautifulSoup

from moduls.parser.grant_object import Grant


class FundingHub:

    SOURCE = "fundinghub"
    BASE_URL = "https://fundinghub.com.ua"

    @staticmethod
    def parse(html: str) -> list[Grant]:
        soup = BeautifulSoup(html, "html.parser")

        result = []

        grants = soup.select('a[href^="/grant/"]')

        for grant in grants:
            title = grant.select_one("h3")

            if not title:
                continue

            amount = grant.select_one(
                ".font-heading.font-black.text-lg.text-primary"
            )

            description = grant.select_one("p")

            tags = [
                tag.get_text(" ", strip=True)
                for tag in grant.select(
                    ".inline-flex.items-center.gap-1"
                )
                if tag.find("svg")
            ]

            company = None
            deadline = None
            status = None

            info = grant.select(
                ".flex.items-center.gap-1\\.5.text-xs.text-muted-foreground"
            )

            if len(info) >= 1:
                company = info[0].get_text(" ", strip=True)

            if len(info) >= 2:
                deadline = info[1].get_text(" ", strip=True)

            badge = grant.select_one(
                ".flex.flex-wrap.gap-1\\.5.mb-3 span"
            )

            if badge:
                status = badge.get_text(" ", strip=True)

            result.append(
                Grant(
                    source=FundingHub.SOURCE,

                    amount=(
                        amount.get_text(" ", strip=True)
                        if amount else ""
                    ),

                    title=title.get_text(" ", strip=True),

                    description=(
                        description.get_text(" ", strip=True)
                        if description else ""
                    ),

                    tags=tags,

                    company=company or "",

                    deadline=deadline or "",

                    status=status or "",

                    url=urljoin(
                        FundingHub.BASE_URL,
                        grant["href"]
                    ),
                )
            )

        return result

    @staticmethod
    def parse_detail(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        heading = soup.find(
            "h2",
            string=lambda text: text and text.strip() == "Детальний опис програми"
        )

        if not heading:
            return ""

        description = heading.find_next_sibling("p")

        if not description:
            return ""

        return description.get_text(" ", strip=True)