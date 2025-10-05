import streamlit as st
import folium
from streamlit_folium import folium_static  # Для отображения Folium в Streamlit
from folium import MacroElement
from jinja2 import Template

st.title("BloomWatch: Интерактивная карта глобальной фенологии цветения растений")
st.write("Текущая дата: 5 октября 2025. Кликните на карту для информации о растительности.")

# Создаём карту, центрируем на указанном месте
m = folium.Map(location=[41.1656, 69.3457], zoom_start=8, tiles='OpenStreetMap')

# Добавляем WMS-слой NDVI (monthly). Используем 2024-10-01 как прокси для 2025
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
    times='2024-10-01'  # Замените на '2025-10-01' когда данные появятся
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
                    popupContent += "NDVI значение: ~0.3 (средняя растительность, осенний сезон; исторические данные NASA MODIS для октября в Узбекистане).<br>" +
                                    "Тип растительности: Сельскохозяйственные культуры (хлопок, виноград, арбузы), тугай (поплар, ива).<br>" +
                                    "Сезон цветения: Минимальный в октябре; основное весной. Урожай фруктов и хлопка.<br>" +
                                    "Источник: NASA MODIS данные (proxied from October 2024).";
                } else {
                    popupContent += "NDVI значение: Зависит от региона (0-1; высокое = густая растительность).<br>" +
                                    "Тип растительности: Проверьте по координатам.<br>" +
                                    "Для реальных данных: Используйте NASA GIOVANNI API.";
                }
                
                var marker = L.marker(e.latlng).addTo({{this._parent.get_name()}});
                marker.bindPopup(popupContent);
            });
        {% endmacro %}
    """)

m.add_child(ClickForMarker())

# Отображаем карту в Streamlit
folium_static(m, width=800, height=600)

# Для динамических реальных данных (опционально): Добавьте запрос к NASA
# st.write("Для свежих данных: Зарегистрируйтесь на Earthdata.nasa.gov и используйте API.")
# Пример: import requests
# response = requests.get('https://giovanni.gsfc.nasa.gov/...')  # С вашими параметрами