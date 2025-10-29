from pydantic import BaseModel, Field

from app.common.schemas.mongo.icons.MutationWeight import MutationWeight


class IconBase(BaseModel):
    name: str
    base_svg: str = Field(alias="baseSvg")
    svg_template: str | None = Field(None, alias="svgTemplate")
    rotation_symmetry_angle: int | None = Field(None, alias="rotationSymmetryAngle")
    mutation_weight: MutationWeight | None = Field(None, alias="mutationWeight")
