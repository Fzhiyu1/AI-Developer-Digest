"""ArXiv paper info tool."""

import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET


ATOM_NS = "{http://www.w3.org/2005/Atom}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m tools.arxiv_info <paper_id>")
        print("Example: python -m tools.arxiv_info 2602.10999")
        sys.exit(1)

    paper_id = sys.argv[1]
    url = f"http://export.arxiv.org/api/query?id_list={paper_id}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AI-Daily-Paper/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read().decode()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    root = ET.fromstring(xml_data)
    entry = root.find(f"{ATOM_NS}entry")
    if entry is None:
        print(f"Error: no entry found for paper '{paper_id}'")
        sys.exit(1)

    title_el = entry.find(f"{ATOM_NS}title")
    title = " ".join(title_el.text.split()) if title_el is not None and title_el.text else "unknown"

    authors = []
    for author_el in entry.findall(f"{ATOM_NS}author"):
        name_el = author_el.find(f"{ATOM_NS}name")
        if name_el is not None and name_el.text:
            authors.append(name_el.text.strip())
    if len(authors) > 3:
        authors_str = ", ".join(authors[:3]) + " et al."
    else:
        authors_str = ", ".join(authors) if authors else "unknown"

    published_el = entry.find(f"{ATOM_NS}published")
    published = published_el.text[:10] if published_el is not None and published_el.text else "unknown"

    categories = []
    for cat_el in entry.findall(f"{ATOM_NS}category"):
        term = cat_el.get("term")
        if term:
            categories.append(term)
    if not categories:
        for cat_el in entry.findall("{http://arxiv.org/schemas/atom}primary_category"):
            term = cat_el.get("term")
            if term:
                categories.append(term)
    categories_str = ", ".join(categories) if categories else "unknown"

    summary_el = entry.find(f"{ATOM_NS}summary")
    abstract = ""
    if summary_el is not None and summary_el.text:
        abstract = " ".join(summary_el.text.split())
        if len(abstract) > 200:
            abstract = abstract[:200] + "..."

    print(f"title: {title}")
    print(f"authors: {authors_str}")
    print(f"published: {published}")
    print(f"categories: {categories_str}")
    print(f"abstract: {abstract}")


if __name__ == "__main__":
    main()
