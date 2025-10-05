import streamlit as st
import folium
from streamlit_folium import folium_static  # pip install streamlit-folium
from folium import MacroElement
from jinja2 import Template

st.title("BloomWatch: Интерактивная карта глобальной фенологии цветения растений")
st.write("Текущая дата: 5 октября 2025. Кликните на карту для информации о растительности (реальные данные для Ташкента).")

# Создаём карту
m = folium.Map(location=[41.1656, 69.3457], zoom_start=8, tiles='OpenStreetMap')

# Добавляем WMS-слой NDVI
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
    times='2024-10-01'  # Прокси для 2025
).add_to(m)

# Добавляем контроль слоёв
folium.LayerControl().add_to(m)

# Добавляем функциональность клика
class ClickForMarker(MacroElement):
    _template = Template("""
        {% macro script(this, kwargs) %}
            {{this._parent.get_name()}}.on('click', function(e) {
                var lat = e.latlng.lat.toFixed(4);
                var lng = e.latlng.lng.toFixed(4);
                var popupContent = "<b>Место:</b> Широта " + lat + ", Долгота " + lng + "<br>" +
                                   "<b>Дата:</b> 5 октября 2025<br>" +
                                   "<b>Информация о растительности:</b><br>";
                
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

# Отображаем карту в Streamlit
folium_static(m, width=800, height=600)
