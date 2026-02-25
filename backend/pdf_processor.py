from typing import Any
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableStructureOptions,
    TableFormerMode,
    PictureDescriptionApiOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import ImageRefMode

import config
from prompts import VLM_PROMPT

def create_picture_description_options() -> PictureDescriptionApiOptions:
    return PictureDescriptionApiOptions(
        url=f"{config.OLLAMA_BASE_URL}/v1/chat/completions",
        params=dict[str, Any](model=config.VLM_MODEL, **config.VLM_API_PARAMS),
        prompt=VLM_PROMPT,
        timeout=config.VLM_TIMEOUT,
    )

def create_pdf_pipeline_options() -> PdfPipelineOptions:
    return PdfPipelineOptions(
        enable_remote_services=True,
        do_ocr=config.DOCLING_DO_OCR,
        do_table_structure=config.DOCLING_DO_TABLE_STRUCTURE,
        generate_picture_images=config.DOCLING_GENERATE_PICTURE_IMAGES,
        do_picture_description=config.DOCLING_DO_PICTURE_DESCRIPTION,
        table_structure_options=TableStructureOptions(
            mode=TableFormerMode(config.TABLE_STRUCTURE_MODE),
        ),
        picture_description_options=create_picture_description_options(),
    )

def process_document(pdf_path: str) -> str:
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=create_pdf_pipeline_options(),
                backend=PyPdfiumDocumentBackend,
            )
        }
    )
    result = converter.convert(pdf_path)
    doc = result.document

    content = doc.export_to_markdown(
        image_mode=ImageRefMode.PLACEHOLDER,
        image_placeholder="",
        page_break_placeholder=config.PAGE_BREAK_PLACEHOLDER,
        include_annotations=True,
        mark_annotations=True,
    )

    content = content.replace(
        '<!--<annotation kind="description">-->', config.IMAGE_DESCRIPTION_START
    )
    content = content.replace('<!--<annotation/>-->', config.IMAGE_DESCRIPTION_END)
    return content