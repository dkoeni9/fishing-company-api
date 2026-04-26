from companies.models import Company
from fishing_bases.models import (
    Fish,
    FishInFishingBase,
    FishingBase,
    FishingBaseStaff,
    fishing_base_photo_path,
)
from sessions.models import FishingSession
from users.models import User

# Historical migrations import this exact function name.
fishbase_photo_path = fishing_base_photo_path

__all__ = [
    "Company",
    "Fish",
    "FishInFishingBase",
    "FishingBase",
    "FishingBaseStaff",
    "FishingSession",
    "User",
    "fishing_base_photo_path",
]
