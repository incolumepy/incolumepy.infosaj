"""infosaj Module."""

__author__ = "@britodfbr"

import inspect
import logging
import os
from pathlib import Path
from random import randint
from typing import Any, Dict, Union, List

import yaml
from bs4 import BeautifulSoup
from faker import Faker

logging.basicConfig(level=logging.DEBUG)

HTMLSKEL = (
    "<!DOCTYPE html>"
    '<html lang="pt-br">'
    "<head>"
    '<meta name="viewport" '
    'content="width=device-width, initial-scale=1">'
    '<meta charset="UTF-8">'
    "<title></title>"
    "<style></style>"
    "</head>"
    "<body>"
    "<header></header>"
    "<main></main>"
    "<footer></footer>"
    "</body>"
    "</html>"
)

modelfile = Path.home().joinpath("infosaj", "model.yaml")

fake = Faker("pt_BR")
# Faker.seed(13)
aniversariantes = [(fake.date_this_month(), fake.name()) for x in range(20)]
datamodel = {
    "infodate": fake.date_this_month(),
    "infonum": randint(1, 10),
    "title": "Informativo SAJ",
    "header": "IMG/header2.2.svg",
    "footer": [None, "IMG/Logo-CEJ.svg", None],
    "stylecss": ["css/color.css", "css/layout.css"],
    "soupname": "index.html",
    "aniversariantes": aniversariantes,
    "decisões": [
        {
            "title": f"ADI {x} Medida Cautelar",
            "relator": fake.name(),
            "resumo": fake.sentence(),
            "message": None,
            "linkaddress": "#",
            "linktext": fake.uri(),
        }
        for x in range(1, 6)
    ],
    "neofitos": [
        'José Francisco da Silva',
        'José da Silva',
        'Francisco da Silva'
    ]
}


def gen_model_conf(filecf: Union[str, Path] = ''):
    """
    Generate infosaj/model.yaml with encode ISO8859-1.

    If setted INCOLUMEPY_INFOSAJ, the model.yaml will generate into same
    directory; else into $HOME/infosaj/model.yaml.
    """
    temp = os.environ.get("INCOLUMEPY_INFOSAJ")
    # filecf = Path(temp).with_name("model.yaml") if temp else modelfile
    filecf = filecf if filecf else temp or modelfile
    filecf = Path(filecf)
    filecf.parent.mkdir(parents=True, exist_ok=True)
    result = "#! Arquivo de configuração para o 'informativo SAJ'\n".encode(
        "iso8859-1"
    )
    result += yaml.dump(datamodel, sort_keys=False, encoding="iso8859-1")
    logging.debug(filecf)
    filecf.write_bytes(result)
    logging.debug(result)
    return filecf


def meses(mes: int = 0):
    """Get month name in portuguese language."""
    months = {
        1: "jan",
        2: "fev",
        3: "mar",
        4: "abr",
        5: "mai",
        6: "jun",
        7: "jul",
        8: "ago",
        9: "set",
        10: "out",
        11: "nov",
        12: "dez",
    }
    if mes not in months:
        raise ValueError("Invalid month.")
    return months.get(mes)


def stylecss(soup: BeautifulSoup, content: Dict[str, Any]):
    """Set style soup."""
    for css in content["stylecss"]:
        logging.debug(f'{inspect.stack()[0][3]}: Adding style file {css}.')
        soup.style.append(f'@import url("{css}");')
    return soup


def section_decisoes(soup: BeautifulSoup, content: Dict[str, Any]):
    """Set decisoes section."""
    if not content.get('decisões'):
        return soup

    soup.select_one('.decisoes').append(soup.new_tag("h2"))
    soup.select_one('.decisoes').h2.string = (
        "Decisões Judiciais Relevantes"
    )
    soup.select_one('.decisoes').append(
        soup.new_tag('div', attrs={'class': 'row'})
    )
    for i, decisoes in enumerate(content["decisões"], start=1):
        logging.debug(i, decisoes)
        col = soup.new_tag('div', attrs={'class': 'column'})
        card = soup.new_tag('div', attrs={'class': 'decisao'})
        card.append(soup.new_tag('h3'))
        card.h3.string = decisoes["title"]
        card.append(soup.new_tag("span", attrs={"id": "relator"}))
        card.span.string = f'Relator(a): {decisoes["relator"]}'
        card.append(soup.new_tag("p"))
        card.p.string = decisoes["resumo"]
        link = decisoes.get("linkaddress")
        msg = decisoes.get("message")
        if link:
            card.append(soup.new_tag("span", attrs={"id": "link"}))
            a = soup.new_tag("a", attrs={"href": link})
            a.string = decisoes.get("linktext")
            card.select_one("#link").append("Para leitura completa acesse:")
            if msg:
                card.select_one("#link").string = msg
            card.select_one("#link").append(a)

        col.append(card)
        # col.append(soup.new_tag("hr"))
        soup.select_one('.decisoes').select_one('.row').append(col)
    return soup


def section_aniver(soup: BeautifulSoup, content: Dict[str, Any]):
    """Set aniversariantes table."""

    if not content.get('aniversariantes'):
        return soup

    soup.body.select_one(".aniversariantes").append(soup.new_tag("h2"))
    soup.body.select_one(
        ".aniversariantes"
    ).h2.string = "Aniversariantes do Mês"

    # table
    soup.body.select_one(".aniversariantes").append(soup.new_tag("table"))
    tabletitle = soup.new_tag("thead")
    tabletitle.append(soup.new_tag("tr"))
    tabletitle.tr.append(soup.new_tag("th"))
    tabletitle.tr.append(soup.new_tag("th"))
    soup.select_one(".aniversariantes").table.append(tabletitle)
    # soup.select_one(".aniversariantes").table.append(soup.new_tag("caption"))
    # soup.body.select_one(".aniversariantes").table.caption.string = (
    #     "Aniversariantes SAJ — "
    #     f'{meses(content["infodate"].month)}/{content["infodate"].year}'
    # )
    soup.select_one(".aniversariantes").table.append(soup.new_tag("tbody"))
    soup.select_one(".aniversariantes").table.append(soup.new_tag("tfoot"))
    for date, name in sorted(content["aniversariantes"]):
        logging.debug(
            f'{inspect.stack()[0][3]} {date.strftime("%d/%m")} {name}'
        )
        row = soup.new_tag("tr")
        row.append(soup.new_tag("td"))
        row.append(soup.new_tag("td"))
        row.select_one("td:nth-of-type(1)").append(date.strftime("%d/%m"))
        row.select_one("td:nth-of-type(2)").append(name)
        soup.select_one(".aniversariantes").table.tbody.append(row)
    return soup


def section_neofitos(soup: BeautifulSoup, content: List[str]):
    """Set neofitos table"""
    if not content.get('neofitos'):
        return soup

    logging.debug('section_neofitos')
    soup.body.select_one(".neofitos").append(soup.new_tag("h2"))
    soup.body.select_one(
        ".neofitos"
    ).h2.string = "Bem vindos à SAJ"

    # Table
    soup.body.select_one(".neofitos").append(soup.new_tag("table"))
    tabletitle = soup.new_tag("thead")
    tabletitle.append(soup.new_tag("tr"))
    tabletitle.tr.append(soup.new_tag("th"))
    tabletitle.tr.append(soup.new_tag("th"))
    soup.select_one(".neofitos").table.append(tabletitle)
    # soup.select_one(".neofitos").table.append(soup.new_tag("caption"))
    # soup.body.select_one(".neofitos").table.caption.string = (
    #     "Bem vindo à SAJ — "
    #     f'{meses(content["infodate"].month)}/{content["infodate"].year}'
    # )
    soup.select_one(".neofitos").table.append(soup.new_tag("tbody"))
    soup.select_one(".neofitos").table.append(soup.new_tag("tfoot"))

    for neofito in sorted(content['neofitos']):
        row = soup.new_tag('tr')
        row.append(soup.new_tag("td"))
        row.append(soup.new_tag("td"))
        img = soup.new_tag(
            'img',
            attrs={
                'src': "IMG/funcio-07.png",
                'alt': 'icone de funcionário',
                'width': 35,
                'height': 35,
            }
        )
        logging.debug(f'{neofito}')
        row.select_one("td:nth-of-type(1)").append(img)
        row.select_one("td:nth-of-type(2)").append(neofito)
        soup.select_one(".neofitos").table.tbody.append(row)
    return soup


def set_entrance(fileconf: Union[str, Path] = ""):
    temp = fileconf or os.environ.get("INCOLUMEPY_INFOSAJ")
    temp = Path(temp)
    if temp.suffix not in ['.yml', '.yaml']:
        raise TypeError('Type File not yaml')

    try:
        _ = temp.read_bytes()
        return temp
    except (FileNotFoundError, FileExistsError):
        pass
    return gen_model_conf()


def gen_infosaj(fileconfig: Union[str, Path] = '', ):
    """Generate infosaj soup file."""
    fin = set_entrance(fileconfig)
    content = yaml.full_load(fin.read_text(encoding="iso8859-1"))
    logging.debug(content)
    soup = BeautifulSoup(HTMLSKEL, "html5lib")
    stylecss(soup, content)
    soup.title.string = content.get('title')
    soup.header.append(soup.new_tag("figure"))
    soup.header.figure.append(
        soup.new_tag(
            "img", attrs={"src": f"{content['header']}", "width": "100%"}
        )
    )
    soup.header.append(soup.new_tag("span", attrs={"class": "num"}))
    soup.header.span.string = (
        "Brasília/DF, "
        f"{meses(content['infodate'].month)} "
        f"{content['infodate'].year} - Nº {content['infonum']}"
    )

    # decisoes
    soup.main.append(soup.new_tag("div", attrs={"class": "decisoes"}))
    section_decisoes(soup, content)

    # Aniversariantes
    soup.main.append(soup.new_tag("div", attrs={"class": "aniversariantes"}))
    section_aniver(soup, content)

    # Neofitos
    soup.main.append(soup.new_tag("div", attrs={"class": "neofitos"}))
    section_neofitos(soup, content)

    # Footer
    # soup.body.append(soup.new_tag("footer"))
    for i, elem in enumerate(content["footer"], start=1):
        # print(i, elem)
        soup.footer.append(soup.new_tag("div"))
        if elem:
            soup.footer.select_one(f"div:nth-of-type({i})").append(
                soup.new_tag("figure")
            )
            soup.footer.select_one(f"div:nth-of-type({i})").figure.append(
                soup.new_tag("img", attrs={"src": elem})
            )

    filename = fin.with_name(content.get("soupname") or "index.html")
    filename.write_bytes(soup.prettify(encoding="iso8859-1"))
    return filename.as_posix()


def home_validate():
    print(Path.home().joinpath('infosaj', 'model.yaml').is_file())
    print(
        Path(os.environ.get('USERPROFILE'))
            .joinpath('infosaj', 'model.yaml')
            .is_file()
    )
    print(
        Path(os.environ.get('HOMEPATH'))
            .joinpath('infosaj', 'model.yaml')
            .is_file()
    )


if __name__ == "__main__":  # pragma: no cover
    # gen_infosaj(Path('/tmp/test_load_model_envvar/model.yaml'))
    # print(gen_model_conf())
    # print(gen_infosaj())
    # print(gen_infosaj(Path.home().joinpath('infosaj', 'model.yml')))
    # model = Path('/tmp/test_load_model_envvar/model.yml')
    # gen_infosaj(model)
    # model = Path(__file__).parents[2].joinpath('model.yml')
    model = Path(__file__).parent.joinpath('model.yml')
    gen_model_conf(model)
    logging.debug(model)
    logging.debug(gen_infosaj(model))

