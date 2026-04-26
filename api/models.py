from companies.models import Company, StaffProfile
from fishing_bases.models import (
    Fish,
    FishInFishingBase,
    FishingBase,
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
    "FishingSession",
    "StaffProfile",
    "User",
    "fishing_base_photo_path",
]
