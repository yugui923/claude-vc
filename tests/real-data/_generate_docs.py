"""Generate DOCX and PDF files from markdown text for synthetic test data.

Uses only Python stdlib — no third-party dependencies.

DOCX: Proper Open XML with styles (Calibri font, styled headings, bullet
      lists, bold/italic runs, table rendering with borders).
PDF:  Multi-page PDF 1.4 with Helvetica, proper text flow, page breaks,
      and correct xref table.
"""

from __future__ import annotations

import re
import textwrap
import zipfile
from io import BytesIO
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════
# DOCX generation — professional Open XML
# ═══════════════════════════════════════════════════════════════════════════

_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

_CONTENT_TYPES = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
      <Default Extension="rels"
        ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
      <Default Extension="xml" ContentType="application/xml"/>
      <Override PartName="/word/document.xml"
        ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
      <Override PartName="/word/styles.xml"
        ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
    </Types>""")

_TOP_RELS = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1"
        Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
        Target="word/document.xml"/>
    </Relationships>""")

_WORD_RELS = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1"
        Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"
        Target="styles.xml"/>
    </Relationships>""")

_STYLES_XML = textwrap.dedent(f"""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:styles xmlns:w="{_W}">
      <w:docDefaults>
        <w:rPrDefault>
          <w:rPr>
            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>
            <w:sz w:val="22"/>
            <w:szCs w:val="22"/>
          </w:rPr>
        </w:rPrDefault>
        <w:pPrDefault>
          <w:pPr>
            <w:spacing w:after="120" w:line="276" w:lineRule="auto"/>
          </w:pPr>
        </w:pPrDefault>
      </w:docDefaults>
      <w:style w:type="paragraph" w:styleId="Normal">
        <w:name w:val="Normal"/>
        <w:qFormat/>
      </w:style>
      <w:style w:type="paragraph" w:styleId="Heading1">
        <w:name w:val="heading 1"/>
        <w:qFormat/>
        <w:pPr>
          <w:spacing w:before="360" w:after="120"/>
        </w:pPr>
        <w:rPr>
          <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
          <w:b/>
          <w:color w:val="1F3864"/>
          <w:sz w:val="36"/>
          <w:szCs w:val="36"/>
        </w:rPr>
      </w:style>
      <w:style w:type="paragraph" w:styleId="Heading2">
        <w:name w:val="heading 2"/>
        <w:qFormat/>
        <w:pPr>
          <w:spacing w:before="240" w:after="80"/>
        </w:pPr>
        <w:rPr>
          <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
          <w:b/>
          <w:color w:val="2E75B6"/>
          <w:sz w:val="28"/>
          <w:szCs w:val="28"/>
        </w:rPr>
      </w:style>
      <w:style w:type="paragraph" w:styleId="Heading3">
        <w:name w:val="heading 3"/>
        <w:qFormat/>
        <w:pPr>
          <w:spacing w:before="200" w:after="60"/>
        </w:pPr>
        <w:rPr>
          <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
          <w:b/>
          <w:color w:val="404040"/>
          <w:sz w:val="24"/>
          <w:szCs w:val="24"/>
        </w:rPr>
      </w:style>
      <w:style w:type="paragraph" w:styleId="ListBullet">
        <w:name w:val="List Bullet"/>
        <w:pPr>
          <w:ind w:left="720" w:hanging="360"/>
          <w:spacing w:after="60"/>
        </w:pPr>
      </w:style>
      <w:style w:type="paragraph" w:styleId="HorizontalRule">
        <w:name w:val="Horizontal Rule"/>
        <w:pPr>
          <w:pBdr>
            <w:bottom w:val="single" w:sz="6" w:space="1" w:color="CCCCCC"/>
          </w:pBdr>
          <w:spacing w:before="120" w:after="120"/>
        </w:pPr>
        <w:rPr><w:sz w:val="4"/></w:rPr>
      </w:style>
    </w:styles>""")


def _escape_xml(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _make_run_xml(text: str, *, bold: bool = False, italic: bool = False) -> str:
    rpr = ""
    if bold or italic:
        parts = []
        if bold:
            parts.append("<w:b/>")
        if italic:
            parts.append("<w:i/>")
        rpr = f"<w:rPr>{''.join(parts)}</w:rPr>"
    return f'<w:r>{rpr}<w:t xml:space="preserve">{_escape_xml(text)}</w:t></w:r>'


def _parse_inline(text: str) -> str:
    """Convert **bold** and *italic* markdown to runs."""
    runs: list[str] = []
    i = 0
    while i < len(text):
        if text[i : i + 2] == "**":
            end = text.find("**", i + 2)
            if end != -1:
                runs.append(_make_run_xml(text[i + 2 : end], bold=True))
                i = end + 2
                continue
        if text[i] == "*" and (i + 1 < len(text) and text[i + 1] != "*"):
            end = text.find("*", i + 1)
            if end != -1:
                runs.append(_make_run_xml(text[i + 1 : end], italic=True))
                i = end + 1
                continue
        # Collect plain text until next marker
        j = i + 1
        while j < len(text):
            if text[j] == "*":
                break
            j += 1
        runs.append(_make_run_xml(text[i:j]))
        i = j
    return "".join(runs)


def _make_table_xml(rows: list[str]) -> str:
    """Build a DOCX table from markdown pipe-delimited rows."""
    parsed: list[list[str]] = []
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        # Skip separator rows (---|---|---)
        if all(set(c.strip()) <= {"-", ":"} for c in cells):
            continue
        parsed.append(cells)
    if not parsed:
        return ""
    num_cols = max(len(r) for r in parsed)
    col_width = 9000 // num_cols  # twips, ~6.25 inches total

    border = (
        "<w:tblBorders>"
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="AAAAAA"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="AAAAAA"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="AAAAAA"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="AAAAAA"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="AAAAAA"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="AAAAAA"/>'
        "</w:tblBorders>"
    )

    xml = f'<w:tbl><w:tblPr><w:tblW w:w="9000" w:type="dxa"/>{border}</w:tblPr>'
    for ri, row_cells in enumerate(parsed):
        xml += "<w:tr>"
        for ci in range(num_cols):
            cell_text = row_cells[ci] if ci < len(row_cells) else ""
            is_header = ri == 0
            shading = ""
            if is_header:
                shading = '<w:shd w:val="clear" w:color="auto" w:fill="2E75B6"/>'
            cell_rpr = ""
            if is_header:
                cell_rpr = (
                    '<w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="20"/></w:rPr>'
                )
            else:
                cell_rpr = '<w:rPr><w:sz w:val="20"/></w:rPr>'
            xml += (
                f"<w:tc>"
                f'<w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/>{shading}'
                f'<w:tcMar><w:top w:w="40" w:type="dxa"/><w:bottom w:w="40" w:type="dxa"/>'
                f'<w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tcMar>'
                f"</w:tcPr>"
                f'<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
                f"<w:r>{cell_rpr}"
                f'<w:t xml:space="preserve">{_escape_xml(cell_text)}</w:t></w:r></w:p>'
                f"</w:tc>"
            )
        xml += "</w:tr>"
    xml += "</w:tbl>"
    return xml


def markdown_to_docx(md_text: str, path: str | Path) -> None:
    """Convert markdown text to a professionally formatted .docx file."""
    body_parts: list[str] = []
    lines = md_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Horizontal rule
        if stripped in ("---", "***", "___"):
            body_parts.append(
                '<w:p><w:pPr><w:pStyle w:val="HorizontalRule"/></w:pPr></w:p>'
            )
            i += 1
            continue

        # Table: collect consecutive pipe-delimited lines
        if stripped.startswith("|") and "|" in stripped[1:]:
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            body_parts.append(_make_table_xml(table_lines))
            continue

        # Headings
        if stripped.startswith("### "):
            body_parts.append(
                f'<w:p><w:pPr><w:pStyle w:val="Heading3"/></w:pPr>'
                f"{_parse_inline(stripped[4:])}</w:p>"
            )
        elif stripped.startswith("## "):
            body_parts.append(
                f'<w:p><w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
                f"{_parse_inline(stripped[3:])}</w:p>"
            )
        elif stripped.startswith("# "):
            body_parts.append(
                f'<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
                f"{_parse_inline(stripped[2:])}</w:p>"
            )
        # Bullet list
        elif stripped.startswith("- ") or stripped.startswith("* "):
            bullet_text = stripped[2:]
            body_parts.append(
                f'<w:p><w:pPr><w:pStyle w:val="ListBullet"/></w:pPr>'
                f"{_make_run_xml(chr(0x2022) + ' ')}{_parse_inline(bullet_text)}</w:p>"
            )
        # Numbered list
        elif re.match(r"^\d+\.\s", stripped):
            num_match = re.match(r"^(\d+\.)\s(.*)", stripped)
            if num_match:
                body_parts.append(
                    f'<w:p><w:pPr><w:pStyle w:val="ListBullet"/></w:pPr>'
                    f"{_make_run_xml(num_match.group(1) + ' ')}"
                    f"{_parse_inline(num_match.group(2))}</w:p>"
                )
        # Empty line
        elif stripped == "":
            body_parts.append(
                '<w:p><w:pPr><w:spacing w:after="0" w:line="120" '
                'w:lineRule="auto"/></w:pPr></w:p>'
            )
        # Normal paragraph
        else:
            body_parts.append(f"<w:p>{_parse_inline(stripped)}</w:p>")

        i += 1

    body_xml = "".join(body_parts)
    doc_xml = (
        f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:document xmlns:w="{_W}" xmlns:r="{_R}">'
        f"<w:body>"
        f"{body_xml}"
        f"<w:sectPr>"
        f'<w:pgSz w:w="12240" w:h="15840"/>'
        f'<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
        f"</w:sectPr>"
        f"</w:body></w:document>"
    )

    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", _CONTENT_TYPES)
        zf.writestr("_rels/.rels", _TOP_RELS)
        zf.writestr("word/_rels/document.xml.rels", _WORD_RELS)
        zf.writestr("word/document.xml", doc_xml)
        zf.writestr("word/styles.xml", _STYLES_XML)

    Path(path).write_bytes(buf.getvalue())


# ═══════════════════════════════════════════════════════════════════════════
# PDF generation — multi-page PDF 1.4 with proper text flow
# ═══════════════════════════════════════════════════════════════════════════

_PDF_PAGE_W = 612  # US Letter
_PDF_PAGE_H = 792
_PDF_MARGIN_L = 54  # 0.75 inch
_PDF_MARGIN_R = 54
_PDF_MARGIN_T = 54
_PDF_MARGIN_B = 54
_PDF_USABLE_W = _PDF_PAGE_W - _PDF_MARGIN_L - _PDF_MARGIN_R


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _wrap_text(text: str, font_size: float, max_width: float) -> list[str]:
    """Wrap text to fit within max_width using approximate char widths."""
    avg_char_w = font_size * 0.48  # rough Helvetica average
    chars_per_line = max(20, int(max_width / avg_char_w))
    if len(text) <= chars_per_line:
        return [text]
    return textwrap.wrap(text, width=chars_per_line) or [""]


def markdown_to_pdf(md_text: str, path: str | Path) -> None:
    """Convert markdown text to a multi-page PDF with proper text flow."""
    lines = md_text.split("\n")

    # Pre-process lines into styled segments
    segments: list[tuple[str, float, float]] = []  # (text, font_size, spacing_after)
    for line in lines:
        s = line.strip()
        # Strip markdown bold/italic markers for PDF (we don't have font variants)
        clean = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", s)
        if s.startswith("### "):
            segments.append((clean[4:] if clean.startswith("### ") else clean, 13, 6))
        elif s.startswith("## "):
            segments.append((clean[3:] if clean.startswith("## ") else clean, 15, 8))
        elif s.startswith("# "):
            segments.append((clean[2:] if clean.startswith("# ") else clean, 18, 10))
        elif s in ("---", "***", "___"):
            segments.append(("", 4, 8))  # will draw a rule
        elif s == "":
            segments.append(("", 10, 6))
        elif s.startswith("- ") or s.startswith("* "):
            segments.append(("  \u2022 " + clean[2:], 10, 4))
        elif re.match(r"^\d+\.\s", s):
            segments.append(("  " + clean, 10, 4))
        elif s.startswith("|"):
            # Table row — render as monospaced-ish text
            segments.append((clean, 8.5, 2))
        else:
            segments.append((clean, 10, 4))

    # Layout into pages
    pages: list[list[str]] = []  # list of content-stream strings per page
    current_page: list[str] = []
    y = _PDF_PAGE_H - _PDF_MARGIN_T

    def _new_page() -> None:
        nonlocal y, current_page
        if current_page:
            pages.append(current_page)
        current_page = []
        y = _PDF_PAGE_H - _PDF_MARGIN_T

    for text, font_size, spacing in segments:
        line_h = font_size * 1.3

        # Horizontal rule
        if font_size == 4 and text == "":
            if y - 12 < _PDF_MARGIN_B:
                _new_page()
            rule_y = y - 4
            current_page.append(
                f"0.75 0.75 0.75 RG\n"
                f"0.5 w\n"
                f"{_PDF_MARGIN_L} {rule_y} m "
                f"{_PDF_PAGE_W - _PDF_MARGIN_R} {rule_y} l S\n"
                f"0 0 0 RG"
            )
            y -= 12
            continue

        # Empty line
        if text == "":
            y -= spacing
            if y < _PDF_MARGIN_B:
                _new_page()
            continue

        # Wrap long text
        wrapped = _wrap_text(text, font_size, _PDF_USABLE_W)

        # Check if we need a new page
        needed = len(wrapped) * line_h + spacing
        if y - needed < _PDF_MARGIN_B:
            _new_page()

        for wline in wrapped:
            safe = _pdf_escape(wline)
            current_page.append(
                f"BT\n/F1 {font_size:.1f} Tf\n"
                f"{_PDF_MARGIN_L} {y:.1f} Td\n"
                f"({safe}) Tj\nET"
            )
            y -= line_h

        y -= spacing

    # Don't forget the last page
    if current_page:
        pages.append(current_page)

    if not pages:
        pages = [[""]]

    # Build PDF objects
    obj_strings: list[str] = []
    obj_id = 0

    def _add_obj(content: str) -> int:
        nonlocal obj_id
        obj_id += 1
        obj_strings.append(f"{obj_id} 0 obj\n{content}\nendobj")
        return obj_id

    # 1: Catalog (will reference Pages)
    catalog_id = _add_obj("<< /Type /Catalog /Pages 2 0 R >>")

    # 2: Pages — placeholder, update after creating page objects
    pages_id = _add_obj("")  # updated below

    # 3: Font
    font_id = _add_obj(
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
        "/Encoding /WinAnsiEncoding >>"
    )

    # Create page objects
    page_obj_ids: list[int] = []
    for page_content in pages:
        stream = "\n".join(page_content)
        stream_bytes = stream.encode("latin-1", errors="replace")
        content_id = _add_obj(
            f"<< /Length {len(stream_bytes)} >>\nstream\n{stream}\nendstream"
        )
        page_id = _add_obj(
            f"<< /Type /Page /Parent {pages_id} 0 R "
            f"/MediaBox [0 0 {_PDF_PAGE_W} {_PDF_PAGE_H}] "
            f"/Contents {content_id} 0 R "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> >>"
        )
        page_obj_ids.append(page_id)

    # Update Pages object
    kids = " ".join(f"{pid} 0 R" for pid in page_obj_ids)
    obj_strings[pages_id - 1] = (
        f"{pages_id} 0 obj\n"
        f"<< /Type /Pages /Kids [{kids}] /Count {len(page_obj_ids)} >>\n"
        f"endobj"
    )

    # Assemble PDF byte stream
    output = bytearray()
    output.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")  # binary comment for PDF-awareness

    offsets: list[int] = []
    for obj_str in obj_strings:
        offsets.append(len(output))
        output.extend(obj_str.encode("latin-1", errors="replace"))
        output.extend(b"\n")

    xref_offset = len(output)
    output.extend(f"xref\n0 {len(obj_strings) + 1}\n".encode())
    output.extend(b"0000000000 65535 f \n")
    for off in offsets:
        output.extend(f"{off:010d} 00000 n \n".encode())
    output.extend(b"trailer\n")
    output.extend(
        f"<< /Size {len(obj_strings) + 1} /Root {catalog_id} 0 R >>\n".encode()
    )
    output.extend(b"startxref\n")
    output.extend(f"{xref_offset}\n".encode())
    output.extend(b"%%EOF\n")

    Path(path).write_bytes(bytes(output))


# ═══════════════════════════════════════════════════════════════════════════
# CLI / batch generation
# ═══════════════════════════════════════════════════════════════════════════


def regenerate_all() -> None:
    """Regenerate all .docx and .pdf from synthetic .md files."""
    base = Path(__file__).parent
    count = 0
    for md_file in sorted(base.rglob("synthetic-*.md")):
        text = md_file.read_text()
        docx_path = md_file.with_suffix(".docx")
        pdf_path = md_file.with_suffix(".pdf")
        markdown_to_docx(text, docx_path)
        markdown_to_pdf(text, pdf_path)
        count += 2
        print(f"  {md_file.parent.name}/{md_file.stem}  (.docx + .pdf)")
    print(f"\nRegenerated {count} files ({count // 2} documents)")


if __name__ == "__main__":
    import sys

    if "--all" in sys.argv:
        regenerate_all()
    else:
        test_md = "# Test Document\n## Section One\nHello world paragraph.\n\n- Bullet one\n- Bullet two\n\n| Col A | Col B |\n|-------|-------|\n| 1 | 2 |\n| 3 | 4 |\n\n---\n\n### Sub-section\nSome **bold** and *italic* text here.\n"
        markdown_to_docx(test_md, "/tmp/test.docx")
        markdown_to_pdf(test_md, "/tmp/test.pdf")
        print("Generated test.docx and test.pdf in /tmp/")
