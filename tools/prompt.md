# Chapter Extraction & Documentation Prompt

## Overview

Convert a PDF chapter into structured, cross-linked markdown documentation. Output should be comprehensive, internally consistent, and well-organized.

---

## Input

- **PDF Name:** `<PDF_FILENAME>`
- **PDF Chapters Location:** `<PDF_CHAPTERS_DIR>`
- **Output Location:** `<OUTPUT_DIR>`
- **Chapter Number:** proceed with all chapters in the PDF chapters location, one by one, in order, one at a time.

---

## Objectives

1. **Extract:** Read the full chapter from the PDF source
2. **Synthesize:** Identify all primary items (pragmas, commands, concepts, sections, etc)
3. **Document:** Create comprehensive markdown with consistent structure across all items
4. **Link:** Cross-reference related content within and across chapters
5. **Validate:** Ensure completeness, accuracy, and production quality

---

## Output Specification

### File Format

- **Name Convention:** same as PDF filename
- **Location:** `<OUTPUT_DIR>`
- **Format:** Markdown with proper heading hierarchy, tables, code blocks, links

### Document Structure

**All chapters should follow this consistent template (apply your own criteria in case some chapters require a different structure):**

1. **Chapter Header** — Title and overview (2–3 sentences on scope/purpose)
2. **Table of Contents** — List all primary items with brief descriptions
3. **Item Sections** — For each major item, document:
   - Main concepts and definitions
   - Syntax/Format (code block with language tag)
   - Options/Parameters (table with defaults)
   - Behavior & Details (explanation, constraints, edge cases)
   - Examples (concrete code samples)
   - See Also (links to related items)
4. **Best Practices** — Key principles and recommendations (numbered list)
5. **Quick Reference** — Summary table if chapter has many similar items
6. **Source Attribution** — PDF source reference

### Formatting Standards

**Headings:**
- `#` = Chapter title
- `##` = Major sections (Overview, individual items, Best Practices)
- `###` = Subsections (Syntax, Options, Behavior, Examples, See Also)

**Code & Syntax:**
- All code blocks tagged with language: `` ```tcl ``, `` ```c ``, `` ```python ``
- Preserve exact syntax as shown in PDF

**Tables:**
- Pipe-delimited markdown format
- Always include "Default" column for option/parameter tables
- Group related options logically

**Emphasis:**
- `**bold**` for key concepts
- `` `code` `` for variables/symbols
- `⚠️` for warnings/cautions
- `>` blockquote for important notes
- `[text](file.md#anchor)` for cross-document links (workspace-relative paths only)

---

## Quality Criteria

**Completeness:**
- Every primary item from the chapter is documented
- No items omitted or merged without explanation
- Item count matches table of contents

**Consistency:**
- All items use same structural template
- All tables follow same format
- All code examples are syntactically correct

**Connectivity:**
- Cross-references between related items (See Also sections)
- Links are functional and use correct markdown syntax

**Accuracy:**
- Content matches PDF source exactly
- Defaults and constraints documented as stated in PDF
- Device-specific requirements (e.g., Versal-only) clearly marked

**Presentation:**
- Markdown renders cleanly without syntax errors
- No broken links, misaligned tables, or formatting issues
- Logical flow and readability

---

## Success Checklist

- [ ] All items from chapter documented (count verified with TOC)
- [ ] Each item has: Syntax, Options/Parameters, Behavior, Examples, See Also
- [ ] Option tables include defaults
- [ ] Examples are executable and correct
- [ ] All cross-references use proper markdown link syntax
- [ ] No absolute file paths or `file://` URIs
- [ ] Tables render correctly in markdown preview
- [ ] Heading hierarchy is consistent
- [ ] Warnings/cautions clearly marked with ⚠️ or `>`
- [ ] Source attribution included at end of document

---

## Notes

- Batch reading may be necessary for large chapters to manage token budget
- Documentation should be created immediately after full chapter is read
- Temp extraction files should be removed after markdown is complete

---

**Version:** 2.0  
**Last Updated:** March 29, 2026
