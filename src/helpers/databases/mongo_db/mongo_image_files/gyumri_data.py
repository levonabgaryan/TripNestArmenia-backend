import asyncio

from src.helpers.databases.mongo_db.mongo_file_manager import upload_local_file_in_db, PlaceMetadata

AMENAPRKICH: PlaceMetadata = {
    'place_name': 'Ամենափրկիչ',
    'description': 'Ամենափրկիչ ․․․',
    'region': 'Shirak',
    'location': 'Gyumri',
    'local_image_path': 'src/helpers/databases/mongo_db/mongo_image_files/places/images/amenaprkich-1.jpg'
}

QAXAQAPETARAN: PlaceMetadata = {
    'place_name': 'Քաղաքապետարան',
    'description': 'Քաղաքապետարան ․․․',
    'region': 'Shirak',
    'location': 'Gyumri',
    'local_image_path': 'src/helpers/databases/mongo_db/mongo_image_files/places/images/qaxaqapetaran-1.jpg'
}

CHULOCHNI: PlaceMetadata = {
    'place_name': 'Չուլոչնի',
    'description': 'Չուլոչնի ․․․',
    'region': 'Shirak',
    'location': 'Gyumri',
    'local_image_path': 'src/helpers/databases/mongo_db/mongo_image_files/places/images/chulochni-1.jpg'
}
DATA = (AMENAPRKICH, QAXAQAPETARAN, CHULOCHNI)


from typing import cast

async def upload_gyumri_data():
    tasks = [
        upload_local_file_in_db(
            data['local_image_path'],
            metadata=cast(PlaceMetadata, {k: v for k, v in data.items() if k != 'local_image_path'})
        )
        for data in DATA
    ]
    await asyncio.gather(*tasks)


