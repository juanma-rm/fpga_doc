#!/usr/bin/env python3
"""
Split PDF by chapter/section using Markdown Table of Contents.

Usage:
    python split_pdf_by_chapter.py <toc_file> [--pdf <pdf_path>] [--output <dir>]

TOC Format (required):
    ## Section I: Title (10)
    * Item description (11)
    
    ## Section II: Main (25)
    * **Chapter 1: First (24)**
    * **Chapter 2: Second (39)**
    
    ## Appendices
    * **Appendix A: Title (889)**

Rules:
    - Section headers: ## Section N: Title (page)
    - Chapter headers: * **Chapter N: Title (page)**
    - Appendix headers: * **Appendix X: Title (page)**
    - Page numbers required in parentheses
    - End page auto-calculated from next section/document
"""

import sys
import re
import os
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import io

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import fitz  # PyMuPDF


def parse_toc_markdown(toc_file: str) -> Dict[str, List[Dict]]:
    """
    Parse the TOC markdown file and extract chapter/section information.
    Supports two formats:
    1. Section-based: ## Section N: Title (page) with * **Chapter N: Title (page)**
    2. Chapter-only: ## Chapter N: Title (page) (flat structure)
    
    Returns:
        Dict with structure:
        {
            'section_name': {
                'type': 'section' or 'appendices',
                'number': 'Section I' or None,
                'title': 'Introduction',
                'page': 10,  # Starting page
                'chapters': [
                    {'number': 1, 'title': 'Chapter Title', 'page': 24, ...},
                    ...
                ]
            },
            ...
        }
    """
    sections = {}
    current_section = None
    current_section_key = None
    
    with open(toc_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    section_counter = 0
    appendix_counter = 1
    has_sections = False  # Track if we're using section-based format
    
    # First pass: detect format (section-based or chapter-only)
    for line in lines:
        if re.match(r'^## Section [IVX]+:', line):
            has_sections = True
            break
        elif re.match(r'^## Chapter\s+\d+:', line):
            has_sections = False
            break
    
    # For chapter-only format, create a virtual section to hold all chapters
    if not has_sections:
        virtual_section_key = 'chapters'
        sections[virtual_section_key] = {
            'type': 'section',
            'number': None,
            'title': 'Chapters',
            'page': None,
            'has_intro': False,
            'chapters': []
        }
    
    for i, line in enumerate(lines):
        line = line.rstrip()
        
        # Match section headers: ## Section I: ... (page)
        section_match = re.match(r'^## (Section [IVX]+):\s+(.+?)(?:\s*\((\d+)\))?$', line)
        if section_match:
            section_num = section_match.group(1)  # e.g., "Section I"
            section_title = section_match.group(2)  # e.g., "Introduction"
            page = int(section_match.group(3)) if section_match.group(3) else None
            
            section_counter += 1
            current_section = section_title
            current_section_key = f'section{section_counter}_{section_title.lower().replace(" ", "_").replace("/", "_").replace("&", "and")}'
            
            sections[current_section_key] = {
                'type': 'section',
                'number': section_num,
                'title': section_title,
                'page': page,
                'has_intro': False,
                'chapters': []
            }
            continue
        
        # Match chapter headers in section-based format: * **Chapter N: ... (page)**
        chapter_match = re.match(r'^\* \*\*Chapter\s+(\d+):\s+(.+?)\s*\((\d+)\)\*\*$', line)
        if chapter_match and current_section_key:
            chapter_num = int(chapter_match.group(1))
            chapter_title = chapter_match.group(2)
            page = int(chapter_match.group(3))
            
            sections[current_section_key]['chapters'].append({
                'number': chapter_num,
                'title': chapter_title,
                'page': page
            })
            continue
        
        # Match chapter headers in chapter-only format: ## Chapter N: ... (page)
        top_level_chapter_match = re.match(r'^## Chapter\s+(\d+):\s+(.+?)(?:\s*\((\d+)\))?$', line)
        if top_level_chapter_match and not has_sections:
            chapter_num = int(top_level_chapter_match.group(1))
            chapter_title = top_level_chapter_match.group(2)
            page = int(top_level_chapter_match.group(3)) if top_level_chapter_match.group(3) else None
            
            # Add to the virtual section
            sections['chapters']['chapters'].append({
                'number': chapter_num,
                'title': chapter_title,
                'page': page
            })
            continue
        
        # Match appendix headers: * **Appendix X: ... (page)**
        appendix_match = re.match(r'^\* \*\*(Appendix\s+([A-Z])):\s+(.+?)\s*(?:\((\d+)\))?\*\*$', line)
        if appendix_match:
            if 'appendices' not in sections:
                sections['appendices'] = {
                    'type': 'appendices',
                    'title': 'Appendices',
                    'page': None,
                    'has_intro': False,
                    'chapters': []
                }
            
            appendix_label = appendix_match.group(1)  # e.g., "Appendix A"
            appendix_letter = appendix_match.group(2)  # e.g., "A"
            appendix_title = appendix_match.group(3)
            page = int(appendix_match.group(4)) if appendix_match.group(4) else None
            
            sections['appendices']['chapters'].append({
                'number': appendix_label,
                'letter': appendix_letter,
                'title': appendix_title,
                'page': page
            })
            continue
        
        # Match top-level appendix headers: ## Appendix X: ... (page)
        top_level_appendix_match = re.match(r'^## (Appendix\s+([A-Z])):\s+(.+?)(?:\s*\((\d+)\))?$', line)
        if top_level_appendix_match:
            if 'appendices' not in sections:
                sections['appendices'] = {
                    'type': 'appendices',
                    'title': 'Appendices',
                    'page': None,
                    'has_intro': False,
                    'chapters': []
                }
            
            appendix_label = top_level_appendix_match.group(1)  # e.g., "Appendix A"
            appendix_letter = top_level_appendix_match.group(2)  # e.g., "A"
            appendix_title = top_level_appendix_match.group(3)
            page = int(top_level_appendix_match.group(4)) if top_level_appendix_match.group(4) else None
            
            sections['appendices']['chapters'].append({
                'number': appendix_label,
                'letter': appendix_letter,
                'title': appendix_title,
                'page': page
            })
            continue
    
    # POST-PROCESSING: Detect section introductions
    for section_key, section_data in sections.items():
        chapters = section_data.get('chapters', [])
        section_page = section_data.get('page')
        
        if chapters and section_page:
            # Check if section page is different from first chapter page
            first_chapter_page = chapters[0].get('page')
            if first_chapter_page and section_page < first_chapter_page:
                section_data['has_intro'] = True
    
    return sections


def extract_pdf_range(pdf_path: str, start_page: int, end_page: int, output_path: str) -> bool:
    """
    Extract a range of pages from PDF and save to a new file.
    Returns True if successful, False otherwise.
    """
    try:
        doc = fitz.open(pdf_path)
        output_doc = fitz.open()
        
        start_idx = max(0, start_page - 1)
        end_idx = min(len(doc), end_page)
        
        for page_num in range(start_idx, end_idx):
            output_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        
        output_doc.save(output_path)
        output_doc.close()
        doc.close()
        return True
    except Exception as e:
        print(f"[ERROR] {output_path}: {e}")
        return False


def create_folder_structure(sections: Dict, output_base_dir: str, pdf_path: str = None) -> None:
    """Create folder structure and split PDF by chapter/section."""
    
    # Auto-detect PDF if not provided
    if pdf_path is None:
        pdf_files = list(Path.cwd().glob('*.pdf'))
        if not pdf_files:
            print("Error: No PDF file found in current directory")
            sys.exit(1)
        pdf_path = str(pdf_files[0])
    
    # Get total page count
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        doc.close()
    except Exception as e:
        print(f"Error opening PDF: {e}")
        sys.exit(1)
    
    output_path = Path(output_base_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Detect if we have actual sections or just chapters (chapter-only format)
    has_actual_sections = any(
        s.get('type') == 'section' and s.get('number') and 'Section' in str(s.get('number', ''))
        for s in sections.values()
    )
    
    stats = {'total': 0, 'success': 0, 'skipped': 0, 'errors': []}
    
    for section_key, section_data in sections.items():
        chapters = section_data.get('chapters', [])
        section_page = section_data.get('page')
        has_intro = section_data.get('has_intro', False)
        
        # Create section folder only if we have actual sections
        if has_actual_sections:
            section_folder = output_path / section_key
            section_folder.mkdir(parents=True, exist_ok=True)
        else:
            # Use root output_path for chapter-only format
            section_folder = output_path
        
        # HANDLE SECTION INTRODUCTIONS
        if has_intro and chapters:
            first_chapter_page = chapters[0].get('page')
            if first_chapter_page and section_page and section_page < first_chapter_page:
                intro_end = first_chapter_page - 1
                filename = 'section_intro.pdf'
                output_file = section_folder / filename
                stats['total'] += 1
                
                if extract_pdf_range(pdf_path, section_page, intro_end, str(output_file)):
                    stats['success'] += 1
                else:
                    stats['errors'].append(f"Intro: {section_data.get('title', 'Unknown')}")
        
        # Handle sections without chapters
        if not chapters:
            if section_page:
                next_section_page = total_pages
                for other_key, other_data in sections.items():
                    other_page = other_data.get('page')
                    if other_page and other_page > section_page:
                        next_section_page = min(next_section_page, other_page - 1)
                
                filename = 'section_intro.pdf'
                output_file = section_folder / filename
                stats['total'] += 1
                
                if extract_pdf_range(pdf_path, section_page, next_section_page, str(output_file)):
                    stats['success'] += 1
                else:
                    stats['errors'].append(f"{section_data['title']}")
            else:
                stats['skipped'] += 1
            continue
        
        # Sort chapters by page number
        chapters = sorted(chapters, key=lambda x: x['page'] if x['page'] else 9999)
        
        # Generate PDFs for each chapter
        for i, chapter in enumerate(chapters):
            chapter_page = chapter['page']
            if chapter_page is None:
                stats['skipped'] += 1
                continue
            
            # Determine end page
            if i + 1 < len(chapters):
                next_page = chapters[i + 1]['page']
                end_page = next_page - 1 if next_page else total_pages
            else:
                end_page = total_pages
                section_start = section_data.get('page')
                for other_key, other_data in sections.items():
                    if other_key == section_key:
                        continue
                    other_page = other_data.get('page')
                    if other_page and other_page > (section_start or 0):
                        end_page = min(end_page, other_page - 1)
                end_page = max(chapter_page, min(end_page, total_pages))
            
            # Generate filename with "chapter" prefix for chapter-only format
            if has_actual_sections:
                num_prefix = str(chapter['number']).replace(' ', '_')
                filename_prefix = num_prefix
            else:
                # Use "chapterN_" format for chapter-only format
                # Handle different number types (int or string like "Appendix A")
                num = chapter.get('number', '')
                if isinstance(num, int):
                    filename_prefix = f"chapter{num}"
                else:
                    # For appendixes or other non-numeric labels
                    filename_prefix = f"chapter{str(num).replace(' ', '_').lower()}"
            
            chapter_title_clean = re.sub(r'[^\w\s-]', '', chapter['title'])
            chapter_title_clean = re.sub(r'\s+', '_', chapter_title_clean).lower()
            filename = f"{filename_prefix}_{chapter_title_clean}.pdf"
            output_file = section_folder / filename
            
            stats['total'] += 1
            if extract_pdf_range(pdf_path, chapter_page, end_page, str(output_file)):
                stats['success'] += 1
            else:
                stats['errors'].append(f"{chapter['number']}: {chapter['title']}")
    
    # Final output
    print(f"\nResults:")
    print(f"  Total: {stats['total']} | Success: {stats['success']} | Skipped: {stats['skipped']}")
    if stats['errors']:
        print(f"  Errors ({len(stats['errors'])}):")
        for err in stats['errors']:
            print(f"    - {err}")
    print(f"  Output: {output_path.absolute()}")


def main():
    parser = argparse.ArgumentParser(description='Split PDF by chapter/section using Markdown TOC')
    parser.add_argument('toc_file', help='Path to TOC markdown file')
    parser.add_argument('--pdf', help='Path to PDF file (auto-detected if in current dir)', default=None)
    parser.add_argument('--output', '-o', help='Output directory for split PDFs', default='pdf_chapters')
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.toc_file):
        print(f"Error: TOC file not found: {args.toc_file}")
        sys.exit(1)
    
    sections = parse_toc_markdown(args.toc_file)
    if not sections:
        print("Error: No sections found in TOC")
        sys.exit(1)
    
    # Determine PDF path
    pdf_path = args.pdf
    if not pdf_path:
        pdf_files = list(Path.cwd().glob('*.pdf'))
        if pdf_files:
            pdf_path = str(pdf_files[0])
    
    if not pdf_path or not os.path.isfile(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    print(f"Processing: {Path(args.toc_file).name} + {Path(pdf_path).name}")
    create_folder_structure(sections, args.output, pdf_path)


if __name__ == '__main__':
    main()
