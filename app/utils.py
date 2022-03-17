from bs4 import BeautifulSoup


def cut_body(text):
    """Divides an article in two parts if length exceeds 1750 chars"""
    FIRST_LIMIT_CHAR = 1750

    first_part = []
    second_part = []
    for child in BeautifulSoup(text, "html.parser"):
        if len("".join([str(tag) for tag in first_part])) >= FIRST_LIMIT_CHAR:
            second_part.append(child)
        else:
            first_part.append(child)

    return (
        "".join([str(tag) for tag in first_part]),
        "".join([str(tag) for tag in second_part]),
    )
