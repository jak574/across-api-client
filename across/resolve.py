from .base import ACROSSBase
from .user import ACROSSUser
from typing import Optional
from .jobstatus import JobStatus, JobStatusSchema
from .user import UserArgSchema
from marshmallow import fields, Schema, post_load


class ResolveArgSchema(UserArgSchema):
    name = fields.Str(required=True)


class ResolveSchema(Schema):
    ra = fields.Float(allow_none=True)
    dec = fields.Float(allow_none=True)
    resolver = fields.Str(allow_none=True)
    status = fields.Nested(JobStatusSchema)

    @post_load
    def resolve(self, data, **kwargs):
        return Resolve(**data)


class Resolve(ACROSSBase, ACROSSUser):
    # Type hints
    name: Optional[str]
    ra: Optional[float]
    dec: Optional[float]
    resolver: Optional[str]
    status: JobStatus

    _mission = "ACROSS"
    _api_name = "Resolve"
    _schema = ResolveSchema()
    _get_schema = ResolveArgSchema()

    def __init__(self, name: Optional[str] = None, **kwargs):
        self.status = JobStatus()
        self.name = name
        [setattr(self, k, a) for k, a in kwargs.items()]


class ACROSSResolveName:
    """_summary_

    Returns
    -------
    _type_
        _description_
    """

    ra: Optional[float]
    dec: Optional[float]
    _name: str

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, targname: str):
        """Set name

        Parameters
        ----------
        targname : str
            Target name that can be resolved by the Resolve class
        """
        self._name = targname
        if hasattr(self, "ra") is False or self.ra is None:
            r = Resolve(name=targname)
            r.get()
            if r.status.status == "Accepted":
                self.ra = r.ra
                self.dec = r.dec
