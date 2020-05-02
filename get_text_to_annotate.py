from lxml import etree
import argparse


def get_text(xmlin, txtout):
    """
    Creates a txt-file from an xml-file with the part to annotate.

    Args:
        xmlin [file-like object]
        textout [file-like object]
    """
    tree = etree.parse(xmlin)
    excerpt = tree.xpath("//div[@class='excerpt']")[0]
    txtout.write(etree.tostring(excerpt, pretty_print=False,
                                encoding='utf8').decode('utf8'))


def main():
    parser = argparse.ArgumentParser(
        description='extract txt from an xml to feed to brat')
    parser.add_argument('-x', '--xmlfile', type=str,
                        help='path to xml to extract excerpt from')
    parser.add_argument('-t', '--txtfile', type=str,
                        help='Path to txt to write the excerpt to')
    args = parser.parse_args()

    with open(args.xmlfile, 'r', encoding="utf8") as xmlin:
        with open(args.txtfile, 'w', encoding="utf8") as txtout:
            get_text(xmlin, txtout)


if __name__ == "__main__":
    main()
