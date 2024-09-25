import random
import typing as t

from django.core.management.base import BaseCommand

from glamp.models.attribute import Attribute
from glamp.models.attribute_glamp import AttributeGlamp
from glamp.models.category import Category
from glamp.models.glamp import Glamp
from glamp.models.type_glamp import TypeGlamp

TYPE_GLAMP = [
    "Еко-будиночок",
    "Тент",
    "Купольний будинок",
    "A-frame",
    "Шатро",
    "Юрта",
    "Будинок на колесах",
    "Будинок на дереві",
    "Сафарі-тент",
]

ACTIVITIES = [
    "Домашні тварини/Ферма",
    "Верхова їзда",
    "Піші прогулянки/Походи",
    "Риболовля",
    "Плавання",
    "Катання на човнах",
    "Гірськолижні активності",
    "Медитація/Йога",
    "Спортивна зона",
    "Ігрова зона",
    "Організовані заходи та екскурсії",
]

NATURE = [
    "Національний парк",
    "Море",
    "Озеро",
    "Річка/Струмок",
    "Водоспад",
    "Термальні джерела",
    "Гори",
    "Соляні печери",
    "Гарні краєвиди",
]

BOOKING = [
    "Миттєве бронювання",
    "Цілодобова стійка реєстрації",
    "Безкоштовне скасування",
]

BUSINESS = ["Проектор та екран", "Зона для проведення заходів"]

CONDITIONS = [
    "Дозволено з тваринами",
    "Підходить для дітей",
    "Підходить для груп",
]

TRANSPORT = [
    "Можна замовити трансфер",
    "Станція для заряджання електричних автомобілів",
    "Місце для авто",
]

FOOD = [
    "Сніданок включено",
    "Обід включено",
    "Вечерю включено",
    "Все включено",
    "Обслуговування номерів",
    "Бар",
    "Ресторан",
]

SAFETY = [
    "Територія під охороною",
    "Камера схову",
]

ACCESSIBILITY = [
    "Без порогів",
    "Без сходинок",
    "Ванна з поручнями",
    "Туалет з поручнями",
    "Стілець для душу",
    "Приміщення придатне для гостей на інвалідних візках",
    "Приміщення повністю знаходиться на першому поверсі",
]

ATTR_GLAMP = {
    "Зручності": {
        "Базові зручності": [
            "Система обігріву",
            "Система охолодження",
            "Інтернет",
            "Послуги пральні",
            "Телевізор",
            "Праска",
            "Робоче місце",
        ],
        "Додаткові зручності": [
            "Басейн",
            "Спа",
            "Джакузі",
            "Чан",
            "Сауна",
            "Камін",
            "Альтанка",
            "Тераса",
            "Зона для барбекю",
            "Гамаки",
            "Садові меблі",
        ],
    },
    "Активності": {"": ACTIVITIES},
    "Природа й околиці": {"": NATURE},
    "Опції бронювання": {"": BOOKING},
    "Кімнати та спальні місця": {
        "Спальня": [
            "Кількість спалень",
            "Кількість ліжок",
            "Додати ліжечко для немовлят",
        ],
        "Ванна": [
            "Кількість ванних кімнат",
            "Ванна кімната в номері",
            "Ванна кімната на території",
        ],
        "Кухня і харчування": [
            "Кухня на території",
            "Кухня в номері",
            "Обідня зона",
            "Мікрохвильовка",
            "Плита",
            "Холодильник",
            "Без кухні",
        ],
    },
    "Бізнес і події": {"": BUSINESS},
    "Умови перебування": {"": CONDITIONS},
    "Транспорт": {"": TRANSPORT},
    "Харчування": {"": FOOD},
    "Безпека": {"": SAFETY},
    "Доступність": {"": ACCESSIBILITY},
}


class Command(BaseCommand):
    def _write(self, message: str) -> None:
        self.stdout.write(message)

    def handle(self, *args: t.Any, **options: t.Any) -> None:
        self.upload_data()
        self._write("Data has been uploaded successfully")

    def create_glamp_types(self) -> list[TypeGlamp]:
        glamp_types = [TypeGlamp(name=glamp) for glamp in TYPE_GLAMP]
        TypeGlamp.objects.bulk_create(glamp_types, ignore_conflicts=False)
        return glamp_types

    def create_attributes(self) -> list[Attribute]:
        attributes = [Attribute(name=attr) for attr in ATTR_GLAMP.keys()]
        Attribute.objects.bulk_create(attributes, ignore_conflicts=False)
        return attributes

    def create_attributes_glamp(self) -> list[AttributeGlamp]:
        glamps = Glamp.objects.all()

        attr_glamps = []
        for attr_name, category_name in ATTR_GLAMP.items():
            attribute = Attribute.objects.get(name=attr_name)
            for section in category_name.values():
                attr_glamp = [
                    AttributeGlamp(
                        attribute=attribute,
                        attribute_name=item,
                        glamp=random.choice(glamps),
                    )
                    for item in section
                ]
                attr_glamps.extend(attr_glamp)
        AttributeGlamp.objects.bulk_create(attr_glamps, ignore_conflicts=False)
        return attr_glamp

    def create_category_attribute(self) -> list[Category]:
        categories = []
        attribute_cache = {
            attr.attribute_name: attr for attr in AttributeGlamp.objects.all()
        }

        for category_name in ATTR_GLAMP.values():
            for item, elem in category_name.items():
                if item:
                    for attr in elem:
                        category = Category(name=item)
                        attribute = attribute_cache.get(attr)
                        if attribute:
                            category.attribute = attribute
                        categories.append(category)

        Category.objects.bulk_create(categories, ignore_conflicts=False)
        return categories

    def upload_data(self) -> None:
        self._write("Starting to upload --- TYPE_GLAMP ---")
        glamp_types = self.create_glamp_types()
        self._write("TypeGlamp items count: %s" % len(glamp_types))

        self._write("Starting to upload --- ATTRIBUTE ---")
        attributes = self.create_attributes()
        self._write("Attribute items count: %s" % len(attributes))

        self._write("Starting to upload --- ATTRIBUTE_GLAMP ---")
        attr = self.create_attributes_glamp()
        self._write("Attribute items count: %s" % len(attr))

        self._write("Starting to upload --- CATEGORY ---")
        category = self.create_category_attribute()
        self._write("Category items count: %s" % len(category))
