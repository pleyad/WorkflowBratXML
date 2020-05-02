from lxml import etree
import argparse


def txtann2xml(intxt, inann, from_online=False):
    """
    Builds a new excerpt, combining the original XML with the annotations
    Args:
        intxt (file-like object)
        inann (file-like object)
    """

    taglist = []
    for line in inann:
        tag, start, end = line.split("\t")[1].split(" ")
        taglist.append((f"<annotation class='{tag.lower()}'>", start))
        taglist.append(("</annotation>", end))
    taglist = sorted(taglist, key=lambda item: int(item[1]))

    new_xml = ""
    i = 0
    for line in intxt:
        for c in line:
            if from_online:
                if len(taglist) > 0 and i == int(taglist[0][1])-2:
                    new_xml += taglist.pop(0)[0]
            else:
                if len(taglist) > 0 and i == int(taglist[0][1]):
                    new_xml += taglist.pop(0)[0]
            new_xml += c
            i += 1

        # Oddly, the local version of brat counts newline-characters as two
        # characters, while the online-version doesnt
        # (At least this would explain the behaviour I encountered)
        # Thats why here, we increase the character-counter by one if its
        if not from_online:
            i += 1

    return etree.fromstring(new_xml)


def reintegrate(old_xml, new_excerpt, new_xml):
    """Replaces an excerpt-element in an xml-file and writes the product the a new file.

    Args:
        old_xml ([type]): [description]
        new_excerpt ([type]): [description]
        new_xml ([type]): [description]
    """
    old_xml = etree.parse(old_xml)

    root = old_xml.getroot()
    old_excerpt = old_xml.xpath("//div[@class='excerpt']")[0]

    root.replace(old_excerpt, new_excerpt)

    old_xml.write(new_xml, encoding="utf8",
                  pretty_print=True, xml_declaration=True)


def main():

    parser = argparse.ArgumentParser(
        description='reintegrate the annotation to the original xml')
    parser.add_argument('-x', '--xmlfile', type=str,
                        help='path to the original xml')
    parser.add_argument('-t', '--txtfile', type=str,
                        help='Path to the annotated txt')
    parser.add_argument('-a', '--annfile', type=str,
                        help='Path to the annotation file')
    parser.add_argument('-n', '--newfile', type=str,
                        help='Path to the new, annotated xml file')
    parser.add_argument('-o', '--fromonline', default=False, action='store_true',
                        help='Set if ann comes from online with one character as title')
    args = parser.parse_args()

    with open(args.txtfile, "r", encoding="utf8") as intxt:
        with open(args.annfile, "r", encoding="utf8") as inann:
            new_excerpt = txtann2xml(intxt, inann, args.fromonline)

    with open(args.xmlfile, 'r', encoding="utf8") as old_xml:
        with open(args.newfile, 'wb') as new_xml:
            reintegrate(old_xml, new_excerpt, new_xml)


if __name__ == "__main__":
    main()
