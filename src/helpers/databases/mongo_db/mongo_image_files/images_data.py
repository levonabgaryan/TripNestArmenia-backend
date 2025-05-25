import asyncio
from typing import cast
from pathlib import Path

BASE_DIR = Path(__file__).parent / "images"

from src.helpers.databases.mongo_db.mongo_fs_file_manager import upload_local_file_in_db, PlaceMetadata

# latitude - 0, longitude-1
GYUMRI: PlaceMetadata = {
    'place_name': 'Գյումրի',
    'description': """Գյումրին՝ Հայաստանի երկրորդ խոշոր քաղաքը, հիացնում է իր յուրօրինակ ճարտարապետությամբ, հումորով լի միջավայրով և հարուստ մշակութային ժառանգությամբ։ Տուրի ընթացքում դուք կայցելեք պատմական Կումայրի արգելոցը, կտեսնեք Ռուսական եկեղեցին և Սուրբ Ամենափրկիչ տաճարը, ինչպես նաև կծանոթանաք Գյումրու արվեստագետների և արհեստավորների ստեղծագործություններին։
                      Տեղում կզգաք գյումրեցու անկեղծ հյուրընկալությունն ու յուրահատուկ կենսախնդություն։ Թարմ օդ, համեղ տեղական խոհանոց, և անկրկնելի հումոր՝ սա է Գյումրին։
                    """,
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
    'description': '',
    'region': 'Shirak',
    'location': 'Գյումրի',
    'local_image_path': str(BASE_DIR / "sev-amroc.jpg"),
    'visited_tours_count_by_location': 0,
}

GYUMRI_DZITOXCYAN: PlaceMetadata = {
    'place_name': 'Ձիթողցյան',
    'description': '',
    'region': 'Shirak',
    'location': 'Գյումրի',
    'local_image_path': str(BASE_DIR / "dzitoxcyanc.jpg"),
    'visited_tours_count_by_location': 0,
}

VANADZOR: PlaceMetadata = {
    'place_name': 'Վանաձոր',
    'description': 'Վանաձորը՝ Լոռու մարզի վարչական կենտրոնը և Հայաստանի երրորդ խոշոր քաղաքը, հայտնի է իր հյուրընկալությամբ, մեղմ կլիմայով և հանգստյան գոտիներով։ Գտնվելով շրջապատված կանաչապատ լեռներով՝ քաղաքը հիանալի վայր է բնության սիրահարների համար։ Այստեղ կարելի է վայելել հանգիստ մթնոլորտ, այցելել սովետական շրջանի ճարտարապետական ժառանգությունը, ինչպես նաև բացահայտել ժամանակակից մշակութային կենտրոններն ու զբոսայգիները։',
    'region': 'Lori',
    'location': 'Վանաձոր',
    'local_image_path': str(BASE_DIR / "VANADZOR.png"),
    'location_in_map': (40.807400, 44.497028)
}

VANADZOR_KAMAKATAR: PlaceMetadata = {
    'place_name': 'Կամակատար',
    'description': '',
    'region': 'Lori',
    'location': 'Վանաձոր',
    'local_image_path': str(BASE_DIR / "kamakatar.png"),
}

VANADZOR_SURB_GRIGOR_NAREKACI: PlaceMetadata = {
    'place_name': 'Սուրբ Գրիգոր Նարեկացի',
    'description': '',
    'region': 'Lori',
    'location': 'Վանաձոր',
    'local_image_path': str(BASE_DIR / "surb-grigor-narekaci.png"),
}

GARNU_TACHAR: PlaceMetadata = {
    'place_name': 'Գառնու տաճար',
    'description': 'Գառնու հեթանոսական տաճար, հին հայկական արևապաշտական տաճար Կոտայքի մարզի Գառնի գյուղում, Ազատ գետի աջ ափին։ Հայաստանի պատմության և մշակույթի անշարժ հուշարձան է: Ելնելով ավանդություններից՝ Մովսես Խորենացին Գառնու հիմնադրումը վերագրում է Հայկ նահապետի ծոռ Գեղամին, որի թոռան՝ Գառնիկի անունով էլ, իբրև, կոչվել է Գառնի',
    'region': 'Kotayq',
    'location': 'Գառնու տաճար',
    'local_image_path': str(BASE_DIR / "GARNI.png"),
    'location_in_map': (40.11833286, 44.720497)
}

SYUNIQ_TATEVI_VANQ : PlaceMetadata = {
    'place_name': 'Տաթևի վանք',
    'description': 'Տաթևի վանք, միջնադարյան վանական համալիր Հայաստանում։ Գտնվում է Սյունիքի մարզի Տաթև գյուղի հարավում՝ Որոտան գետի վտակի ձորի աջափնյա եզերքին։ Ավանդության համաձայն՝ վանքը կոչվել է Թադեոս առաքյալի աշակերտ Եվստաթեոսի անունով:',
    'region': 'Syunik',
    'location': 'Տաթևի վանք',
    'local_image_path': str(BASE_DIR / "tatevi_vanq.jpg"),
    'location_in_map': (39.38166670, 46.24000000)
}

DATA = (
    GYUMRI, GYUMRI_AMENAPRKICH_1, GYUMR_SEV_AMROC, GYUMRI_DZITOXCYAN,
    VANADZOR, VANADZOR_KAMAKATAR, VANADZOR_SURB_GRIGOR_NAREKACI,
    GARNU_TACHAR,
    SYUNIQ_TATEVI_VANQ
)


async def upload_data() -> None:
    tasks = [
        upload_local_file_in_db(
            local_file_path=data['local_image_path'],
            metadata=cast(PlaceMetadata, {k: v for k, v in data.items() if k != 'local_image_path'})
        )
        for data in DATA
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"❌ Error in task {i}: {result}")
        else:
            print(f"✅ Task {i} completed successfully")


if __name__ == "__main__":
    asyncio.run(upload_data())
