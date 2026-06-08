import json
from typing import Any

from flask_restx import fields

from libs.helper import TimestampField


class StringListField(fields.Raw):
    def format(self, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                return [value] if value else []
        if isinstance(value, list):
            return [str(item) for item in value]
        return []


child_chunk_fields = {
    "id": fields.String,
    "segment_id": fields.String,
    "content": fields.String,
    "position": fields.Integer,
    "word_count": fields.Integer,
    "type": fields.String,
    "created_at": TimestampField,
    "updated_at": TimestampField,
}

attachment_fields = {
    "id": fields.String,
    "name": fields.String,
    "size": fields.Integer,
    "extension": fields.String,
    "mime_type": fields.String,
    "source_url": fields.String,
}

segment_fields = {
    "id": fields.String,
    "position": fields.Integer,
    "document_id": fields.String,
    "content": fields.String,
    "sign_content": fields.String,
    "answer": fields.String,
    "word_count": fields.Integer,
    "tokens": fields.Integer,
    "keywords": StringListField,
    "index_node_id": fields.String,
    "index_node_hash": fields.String,
    "hit_count": fields.Integer,
    "enabled": fields.Boolean,
    "disabled_at": TimestampField,
    "disabled_by": fields.String,
    "status": fields.String,
    "created_by": fields.String,
    "created_at": TimestampField,
    "updated_at": TimestampField,
    "updated_by": fields.String,
    "indexing_at": TimestampField,
    "completed_at": TimestampField,
    "error": fields.String,
    "stopped_at": TimestampField,
    "child_chunks": fields.List(fields.Nested(child_chunk_fields)),
    "attachments": fields.List(fields.Nested(attachment_fields)),
    "summary": fields.String,  # Summary content for the segment
}
