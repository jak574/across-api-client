# Copyright © 2023 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.

from typing import List

from ..base.schema import PlanEntryBase, PlanSchemaBase, UserSchema


class NuSTARPlanEntry(PlanEntryBase):
    obsid: str
    comment: str


class NuSTARPlanSchema(PlanSchemaBase):
    entries: List[NuSTARPlanEntry]  # type: ignore


class NuSTARPlanPutSchema(UserSchema):
    entries: List[NuSTARPlanEntry]  # type: ignore
