import asyncio
from typing import cast
from pathlib import Path

BASE_DIR = Path(__file__).parent / "images"

from src.helpers.databases.mongo_db.mongo_file_manager import upload_local_file_in_db, PlaceMetadata

GYUMRI: PlaceMetadata = {
    'place_name': 'Գյումրի',
    'description': '',
    'region': 'Shirak',
    'location': 'Գյումրի',
    'local_image_path': str(BASE_DIR / "GYUMRI.webp"),
    'visited_tours_count_by_location': 0,
    'location_in_map': (40.7942, 43.84528)
}

GYUMRI_AMENAPRKICH_1: PlaceMetadata = {
    'place_name': 'Ամենափրկիչ',
    'description': '',
    'region': 'Shirak',
    'location': 'Գյումրի',
    'local_image_path': str(BASE_DIR / "amenaprkich-1.jpg"),
    'visited_tours_count_by_location': 0,
}

GYUMR_SEV_AMROC: PlaceMetadata = {
    'place_name': 'Սև ամրոց',
    'description': '․․․',
    'region': 'Shirak',
    'location': 'Գյումրի',
    'local_image_path': str(BASE_DIR / "sev-amroc.jpg"),
    'visited_tours_count_by_location': 0,
}

GYUMRI_DZITOXCYAN: PlaceMetadata = {
    'place_name': 'Ձիթողցյան',
    'description': '․․․',
    'region': 'Shirak',
    'location': 'Գյումրի',
    'local_image_path': str(BASE_DIR / "dzitoxcyanc.jpg"),
    'visited_tours_count_by_location': 0,
}

DATA = (GYUMRI, GYUMRI_AMENAPRKICH_1, GYUMR_SEV_AMROC, GYUMRI_DZITOXCYAN)


async def upload_data() -> None:
    tasks = [
        upload_local_file_in_db(
            local_file_path=data['local_image_path'],
            metadata=cast(PlaceMetadata, {k: v for k, v in data.items() if k != 'local_image_path'})
        )
        for data in DATA
    ]

    await asyncio.gather(*tasks)
