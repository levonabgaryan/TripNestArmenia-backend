import asyncio
from typing import cast
from pathlib import Path

BASE_DIR = Path(__file__).parent / "images"

from src.helpers.databases.mongo_db.mongo_file_manager import upload_local_file_in_db, PlaceMetadata

AMENAPRKICH_1: PlaceMetadata = {
    'place_name': 'Ամենափրկիչ',
    'description': '',
    'region': 'Shirak',
    'location': 'Գյումրի',
    'local_image_path': str(BASE_DIR / "amenaprkich-1.jpg"),
    'visited_tours_count_by_location': 0
}

AMENAPRKICH_2: PlaceMetadata = {
    'place_name': 'Ամենափրկիչ',
    'description': 'Գյումրիի Սուրբ Ամենափրկիչ եկեղեցի, եկեղեցի Հայաստանի Շիրակի մարզի Գյումրի քաղաքում։ Կառուցվել է 1860-ական թվականներին, Անիի մայր տաճարի նմանությամբ։ Շինարարական աշխատանքներն ավարտվել են 1873 թվականին։ Շինարարության աշխատանքների ղեկավար Թադևոս Անտիկյանն է։',
    'region': 'Shirak',
    'location': 'Գյումրի',
    'local_image_path': str(BASE_DIR / "amenaprkich-2.jpg"),
    'visited_tours_count_by_location': 0
}

QAXAQAPETARAN: PlaceMetadata = {
    'place_name': 'Քաղաքապետարան',
    'description': 'Քաղաքապետարան ․․․',
    'region': 'Shirak',
    'location': 'Գյումրի',
    'local_image_path': str(BASE_DIR / "qaxaqapetaran-1.jpg"),
    'visited_tours_count_by_location': 0
}

CHULOCHNI: PlaceMetadata = {
    'place_name': 'Չուլոչնի',
    'description': 'Չուլոչնի ․․․',
    'region': 'Shirak',
    'location': 'Գյումրի',
    'local_image_path': str(BASE_DIR / "chulochni-1.jpg"),
    'visited_tours_count_by_location': 0
}

DATA = (AMENAPRKICH_1, AMENAPRKICH_2, QAXAQAPETARAN, CHULOCHNI)


async def upload_gyumri_data() -> None:
    tasks = [
        upload_local_file_in_db(
            local_file_path=data['local_image_path'],
            metadata=cast(PlaceMetadata, {k: v for k, v in data.items() if k != 'local_image_path'})
        )
        for data in DATA
    ]

    await asyncio.gather(*tasks)
