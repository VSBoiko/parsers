from Parser import Parser


if __name__ == "__main__":
    parser = Parser(
        parser_name="tenders.mts.ru",
        is_sleeping=False,
        is_sending_orders=False,
        is_updating_order=False,
        is_parsing_site=False,
    )

    parser.run()
