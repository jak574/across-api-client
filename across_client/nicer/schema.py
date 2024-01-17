from typing import List

from ..base.schema import (
    BaseSchema,
    PlanEntryBase,
    PlanSchemaBase,
    UserSchema,
    VisWindow,
)


class NICERPlanEntry(PlanEntryBase):
    targetid: int
    obsid: int
    mode: str


class NICERPlanPutSchema(UserSchema):
    entries: List[NICERPlanEntry]


class NICERPlanSchema(PlanSchemaBase):
    entries: List[NICERPlanEntry]  # type: ignore


class NICERVisWindow(VisWindow):
    initial: str
    final: str


class NICERVisibilitySchema(BaseSchema):
    entries: List[NICERVisWindow]
