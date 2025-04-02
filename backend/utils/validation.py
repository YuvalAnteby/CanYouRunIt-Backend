import re
from typing import Optional
from fastapi import HTTPException


def validate_hardware_list(
        hardware: list,
        type_: str,
        brand: Optional[str] = None,
        model: Optional[str] = None,
):
    """
       Validates the list of CPUs/GPUs fetched from the database.

       - Raises 404 if the list is empty.
       - Raises 500 if any item is included in the list that wasn't supposed to according to filtering.
       (e.g. brand/ type)


       :param hardware: List of CPU/GPU dictionaries from the DB.
       :param type_: CPU or GPU type for check
       :param brand: Optional brand filter to validate against.
       :param model: Optional model regex to validate against.
       """
# If hardware list is empty count it as no CPU/GPU found error
    if not hardware:
        raise HTTPException(status_code=404, detail=f"No {type_} found")
    # Ensure only relevant CPUs have been fetched from DB
    model_pattern = re.compile(model, re.IGNORECASE) if model else None
    for item in hardware:
        # Check no GPUs were fetched
        if item.get("type", "").lower() != type_:
            raise HTTPException(status_code=500, detail=f"Non-{type_} hardware found in {type_} route")
        # Ensure only relevant brand's CPUs have been fetched
        if brand and item.get("brand", "").lower() != brand.lower():
            raise HTTPException(status_code=500, detail=f"Wrong brand found in {type_}s fetched")
        # Ensure only relevant CPU models have been fetched
        if model_pattern:
            if not (
                    model_pattern.search(item.get("model", "")) or
                    model_pattern.search(item.get("fullname", ""))
            ):
                raise HTTPException(status_code=500, detail=f"Wrong model regex found in {type_}s fetched")
