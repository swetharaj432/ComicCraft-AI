from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    story_prompt: str = Field(
        ...,
        min_length=3,
        max_length=5000
    )

    character_name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    setting: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    tone: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    art_style: str = Field(
        ...,
        min_length=1,
        max_length=100
    )