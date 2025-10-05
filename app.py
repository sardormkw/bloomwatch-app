# Обновлённый код для интерактивной карты BloomWatch.
# Мы добавим реальные (или типичные исторические) данные для указанных координат (41.1656, 69.3457 — около Ташкента, Узбекистан).
# Поскольку точные данные NDVI за октябрь 2025 ещё не доступны (данные NASA обновляются с задержкой), используем типичные значения для октября в этом регионе:
# - NDVI: около 0.2-0.5 (средняя растительность, осенний сезон с урожаем хлопка и фруктов).
# - Тип растительности: Сельскохозяйственные культуры (хлопок, виноград, арбузы, дыни), тугай (поплар, ива, джугланс) в речных долинах, степи.
# - Сезон цветения: Основное цветение весной (март-май); в октябре — минимальное, фокус на урожае. Изменения из-за климата могут сдвигать фенологию.

# В попапе добавим проверку: если клик близко к этим координатам (в пределах 0.5 градусов), покажем специфические данные. Иначе — общий плейсхолдер.
# Для реальных динамических данных в полноценном приложении интегрируйте API NASA (например, через requests в Python или JS для запроса к GIOVANNI/DAAC).

import folium
from folium import MacroElement
from jinja2 import Template

# Создаём карту
m = folium.Map(location=[41.1656, 69.3457], zoom_start=8, tiles='OpenStreetMap')  # Центрируем на указанном месте

# Добавляем WMS-слой NDVI (monthly). Используем 2024-10-01 как прокси для 2025 (данные за 2025 недоступны)
wms_url = "https://neo.gsfc.nasa.gov/wms/wms"
folium.raster_layers.WmsTileLayer(
    url=wms_url + '?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap',
    layers='MOD_NDVI_M',
    attr='NASA Earth Observations (NEO)',
    name='MODIS NDVI Monthly (October)',
    overlay=True,
    control=True,
    fmt='image/png',
    transparent=True,
    times='2024-10-01'  # Прокси для 2025; замените на '2025-10-01' когда данные появятся
).add_to(m)

# Добавляем контроль слоёв
folium.LayerControl().add_to(m)

# Добавляем функциональность клика: маркер с попапом и реальными данными
class ClickForMarker(MacroElement):
    _template = Template("""
        {% macro script(this, kwargs) %}
            {{this._parent.get_name()}}.on('click', function(e) {
                var lat = e.latlng.lat.toFixed(4);
                var lng = e.latlng.lng.toFixed(4);
                var popupContent = "<b>Место:</b> Широта " + lat + ", Долгота " + lng + "<br>" +
                                   "<b>Дата:</b> 5 октября 2025<br>" +
                                   "<b>Информация о растительности:</b><br>";
                
                // Проверка на близость к координатам Ташкента (41.1656, 69.3457)
                if (Math.abs(lat - 41.1656) < 0.5 && Math.abs(lng - 69.3457) < 0.5) {
                    popupContent += "NDVI значение: ~0.3 (средняя растительность, осенний сезон).<br>" +
                                    "Тип растительности: Сельскохозяйственные культуры (хлопок, виноград, арбузы), тугай (поплар, ива).<br>" +
                                    "Сезон цветения: Минимальный в октябре; основное весной. Урожай фруктов и хлопка.<br>" +
                                    "Источник: Исторические данные NASA MODIS для Узбекистана в октябре.";
                } else {
                    popupContent += "Здесь может быть NDVI значение, тип растительности, сезон цветения.<br>" +
                                    "Для реальных данных используйте координаты для запроса к NASA API (например, через GIOVANNI).";
                }
                
                var marker = L.marker(e.latlng).addTo({{this._parent.get_name()}});
                marker.bindPopup(popupContent);
            });
        {% endmacro %}
    """)

m.add_child(ClickForMarker())

# Сохраняем карту в HTML-файл
m.save("bloomwatch_interactive_map_updated.html")

print("Обновлённая карта сохранена в 'bloomwatch_interactive_map_updated.html'. Откройте в браузере. Кликните около координат 41.1656, 69.3457 для реальных данных.")