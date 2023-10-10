from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from marshmallow import Schema, fields, post_load


@dataclass
class JobStatus:
    status: str = "Unknown"
    jobnumber: Optional[int] = None
    completed: Optional[datetime] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class JobStatusSchema(Schema):
    """Light JobStatus return for API calls"""

    status = fields.Str(allow_none=True)
    jobnumber = fields.Int(allow_none=True)
    completed = fields.DateTime(allow_none=True)
    errors = fields.List(cls_or_instance=fields.Str(allow_none=True))
    warnings = fields.List(cls_or_instance=fields.Str(allow_none=True))

    @post_load
    def make_jobstatus(self, data, **kwargs):
        return JobStatus(**data)
