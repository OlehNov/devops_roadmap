from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from glamp.filters import CustomBaseFilterBackend
from glamp.models import AttributeGlamp, Glamp
from glamp.serializers import GlampSerializer


@extend_schema(
    description='Retrieve a list of glamps with optional filters. '
    'Filters are applied dynamically based on query parameters. \n\n'
    '**!!! Warning !!!** \n\n'
    '**Filters without special keyword and operators do not work. In this case, you will always receive an empty list.** \n\n'
    'Supported keywords: \n\n'
    '`filters` - **Keyword that define a filter functionality**\n\n'
    'Supported operators: \n\n'
    '`$eq` - **Equal**\n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[name][$eq]=Glemp 14` \n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[type_glamp__name][$eq]=Тент` \n\n'
    '`$eqi` - **Equal (case-insensitive)**\n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[name][$eqi]=glemp 14` \n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[type_glamp__name][$eqi]=тент` \n\n'
    '`$lt` - **Less than**\n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[capacity][$lt]=5` \n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[price][$lt]=1400` \n\n'
    '`$lte` - **Less than or equal to**\n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[capacity][$lte]=10` \n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[price][$lte]=10000` \n\n'
    '`$gt` - **Greater than**\n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[capacity][$gt]=5` \n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[price][$gt]=1400` \n\n'
    '`$gte` - **Greater than or equal to**\n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[capacity][$gte]=5` \n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[price][$gte]=1400` \n\n'
    '`$in` - **Included in an array**\n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[address__city][$in]=Kyiv,lviv,Odessa` \n\n'
    '`$null` - **Empty value**\n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[attribute__description][$null]` \n\n'
    '`$notnull` - **Not Empty value**\n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[attribute__description][$notnull]` \n\n'
    '`$contains` - **Contains**\n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[name][$contains]=Glemp` \n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[description][$contains]=Luxury` \n\n'
    '`$containsi` - **Contains (case-insensitive)**\n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[name][$containsi]=gLeMp` \n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[description][$containsi]=LuXuRy` \n\n'
    '`$between` - **in range(1, 2)**\n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[price][$between]=1000,5000` \n\n'
    '`$startsWith` - **Starts with**\n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[name][$startsWith]=Glemp` \n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[type_glamp__name][$startsWith]=Eco` \n\n'
    '`$startsWithi` - **Starts with (case-insensitive)**\n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[name][$startsWithi]=GleMP` \n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[type_glamp__name][$startsWithi]=eCo` \n\n'
    '`$endsWith` - **Ends with**\n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[name][$endsWith]=Welcome` \n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[type_glamp__name][$endsWith]=See you` \n\n'
    '`$endsWithi` - **Ends with (case-insensitive)**\n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[name][$endsWithi]=WeLcomE` \n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[type_glamp__name][$endsWithi]=sEE yoU` \n\n'
    'There are specific fields to which you can apply a filter. Access to some fields must be done using a double underscore "__" \n\n'
    'Suported fields: \n\n'
    '`name` - **Glamp name** \n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[name][$eq]=Glemp 14` \n\n'
    '`description` - **Glamp description** \n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[description][$contains]=Luxury` \n\n'
    '`capacity` - **Glamp capacity** \n\n'
    '  - `GET http://localhost:8181/glamp/glamp/?filters[capacity][$gte]=5` \n\n<br>'
    'Suported fields with double underscore "__": \n\n'
    '`type_glamp` - **Glamp Type** \n\n'
    '  - `name` - **Type name** \n\n'
    '  -  - `GET http://localhost:8181/glamp/glamp/?filters[type_glamp__name][$eq]=Тент` \n\n'
    '`address` - **Glamp address** \n\n'
    '  - `street` - **Address street** \n\n'
    '  -  - `GET http://localhost:8181/glamp/glamp/?filters[address__street][$contains]=Набережна` \n\n'
    '  - `house` - **Address house** \n\n'
    '  -  - `GET http://localhost:8181/glamp/glamp/?filters[address__house][$eq]=10` \n\n'
    '  - `apartment` - **Address apartment** \n\n'
    '  - - `GET http://localhost:8181/glamp/glamp/?filters[address__apartment][$eq]=7` \n\n'
    '  - `city` - **Address city** \n\n'
    '  - - `GET http://localhost:8181/glamp/glamp/?filters[address__city][$eqi]=львiв` \n\n'
    '  - `region` - **Address region** \n\n'
    '  - - `GET http://localhost:8181/glamp/glamp/?filters[address__region][$containsi]=Днiпро` \n\n'
    '  - `latitude` - **Address latitude** \n\n'
    '  - - `GET http://localhost:8181/glamp/glamp/?filters[address__latitude][$eq]=49.2123` \n\n'
    '  - `longitude` - **Address longitude** \n\n'
    '  - - `GET http://localhost:8181/glamp/glamp/?filters[address__longitude][$eq]=28.5108` \n\n'
    '`attribute` - **Glamp attributes** \n\n'
    ' - `attribute` - **Attributes** \n\n'
    '  - - `name` - **Attribute name** \n\n'
    '  -  -  - `GET http://localhost:8181/glamp/glamp/?filters[attribute__attribute__name][$eq]=Зручності` \n\n'
    '  - `attribute_name` - **Attribute name** \n\n'
    '  -  - `GET http://localhost:8181/glamp/glamp/?filters[attribute__attribute_name][$eqi]=Телевізор` \n\n'
    'You can also combine fields with "&" symbol for more precise filtering: \n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[type_glamp__name][$startsWithi]=еКо&filters[price][$between]=1200,10000` \n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[attribute__attribute_name][$containsi]=Озеро&filters[attribute__attribute_name][$containsi]=Водоспад` \n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[address__city][$in]=с. Агрономічне,с. Крижанівка&filters[price][$between]=1200,1400` \n\n'
    '- `GET http://localhost:8181/glamp/glamp/?filters[type_glamp__name][$eqi]=Тент&filters[address__street][$eqi]=вул. Набережна&filters[attribute__attribute__name][$eqi]=Транспорт&filters[attribute__attribute_name][$eqi]=Можна замовити трансфер` \n\n'
)
class GlampListView(ReadOnlyModelViewSet):
    queryset = Glamp.objects.select_related(
        'type_glamp', 'address', 'owner'
    ).prefetch_related(
        Prefetch('attribute', queryset=AttributeGlamp.objects.all())
    )
    permission_classes = [AllowAny]
    serializer_class = GlampSerializer
    filter_backends = [CustomBaseFilterBackend]
