from fastapi import APIRouter

from meridian_api.feature_flags import load_feature_flags
from meridian_api.schemas import FeatureFlagsResponse

router = APIRouter(prefix="/feature-flags", tags=["feature-flags"])


@router.get("", response_model=FeatureFlagsResponse)
def get_feature_flags():
    return FeatureFlagsResponse(flags=load_feature_flags())