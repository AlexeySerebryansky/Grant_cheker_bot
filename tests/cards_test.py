from client.client import Client
from moduls.parser.funding_hub import FundingHub


def test_funding_hub():
    client = Client()
    parser_fh = FundingHub()

    url = "https://fundinghub.com.ua/grants"
    html = client.get_html(url)

    grants = parser_fh.parse(html)


    print(f"HTML size: {len(html)}")
    print(f"Grants found: {len(grants)}")
    print("=" * 80)

    for i, grant in enumerate(grants, start=1):
        print(f"[{i}/{len(grants)}] START: {grant.url}", flush=True)

        detail_html = client.get_html(grant.url)

        print(
            f"[{i}/{len(grants)}] RECEIVED: {len(detail_html)} bytes",
            flush=True
        )

        grant.full_description = parser_fh.parse_detail(detail_html)

        print(f"[{i}/{len(grants)}] PARSED", flush=True)

    for i, grant in enumerate(grants, start=1):
        print(f"""
            Grant #{i}
                source:      {grant.source}
                amount:      {grant.amount}
                title:       {grant.title}
                description: {grant.description}
                tags:        {grant.tags}
                company:     {grant.company}
                deadline:    {grant.deadline}
                status:      {grant.status}
                url:         {grant.url}
                full_description: {grant.full_description}
                {"-" * 80}
            """)


if __name__ == "__main__":
    test_funding_hub()
