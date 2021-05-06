import codecs


def get_text_from_txt_file(filename):
    try:
        f = codecs.open(filename, encoding='utf-8')
        f.seek(0)
        text = f.read()
        f.close()
    except (UnicodeDecodeError, OSError, IOError) as e:
        pass
    return text


def get_text_from_epub_file(filename):
    book = epub.open_epub(filename)
    for item in book.opf.manifest.values():
        try:
            text = book.read_item(item)
        except KeyError as k:
            continue
        try:
            text = text.decode('utf-8')
        except UnicodeDecodeError as u:
            pass
    book.close()
    return text
