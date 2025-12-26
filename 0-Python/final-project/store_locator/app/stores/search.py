from typing import Optional, List
from sqlalchemy import and_
from store_locator.app.models import Store, Service
from store_locator.app.extensions import db, cache
from store_locator.app.stores.utils import calculate_bounding_box, calculate_distance
from geopy.geocoders import Nominatim
import ssl
import certifi
import os

class StoreSearchService:
    """
    店铺搜索服务类
    功能:
    1. 地理编码（地址→坐标）
    2. Bounding Box预过滤
    3. Haversine精确距离计算
    4. 多条件过滤
    """

    def __init__(self):
        """初始化地理编码器"""
        user_agent = os.getenv('NOMINATIM_USER_AGENT', 'store-locator/1.0')
        
        # 使用 certifi 提供的受信任 CA
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        self.geocoder = Nominatim(user_agent=user_agent, ssl_context=ssl_context)

    def search_stores(
        self,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        address: Optional[str] = None,
        postal_code: Optional[str] = None,
        radius_miles: float = 10,
        services: Optional[List[str]] = None,
        store_types: Optional[List[str]] = None,
        open_now: bool = False,
        limit: int = 20
    ):
        """
        搜索店铺主函数
        """
        # Step 1: 获取搜索中心点坐标
        search_lat, search_lon = self._get_coordinates(latitude, longitude, address, postal_code)

        if search_lat is None or search_lon is None:
            return {
                'error': 'Unable to determine search location',
                'stores': []
            }

        # Step 2: 计算边界框
        min_lat, max_lat, min_lon, max_lon = calculate_bounding_box(search_lat, search_lon, radius_miles)

        # Step 3: SQL预过滤（利用索引）
        query = Store.query.filter(
            and_(
                Store.latitude.between(min_lat, max_lat),
                Store.longitude.between(min_lon, max_lon),
                Store.status == 'active'
            )
        )

        # Step 4: 服务过滤（AND逻辑）
        if services:
            for service_name in services:
                query = query.filter(Store.services.any(Service.name == service_name))

        # Step 5: 店铺类型过滤（OR逻辑）
        if store_types:
            query = query.filter(Store.store_type.in_(store_types))

        stores = query.all()

        # Step 6: 精确距离计算并过滤
        results = []
        for store in stores:
            distance = calculate_distance((search_lat, search_lon), (float(store.latitude), float(store.longitude)))
            if distance <= radius_miles:
                if open_now and not store.is_open_now():
                    continue
                results.append({'store': store, 'distance': distance})

        # Step 7: 按距离排序
        results.sort(key=lambda x: x['distance'])

        # Step 8: 限制返回数量
        results = results[:limit]

        # Step 9: 返回结构化结果
        return {
            'stores': [
                {**r['store'].to_dict(include_distance=True, distance=r['distance'])}
                for r in results
            ],
            'search_location': {
                'latitude': search_lat,
                'longitude': search_lon,
                'input': address or postal_code or 'coordinates'
            },
            'filters_applied': {
                'radius_miles': radius_miles,
                'services': services or [],
                'store_types': store_types or [],
                'open_now': open_now
            },
            'total_results': len(results)
        }

    def _get_coordinates(self, lat, lon, address, postal):
        """
        获取搜索中心点坐标
        优先级: 直接坐标 > 地址 > 邮编
        """
        # 优先使用直接坐标
        if lat is not None and lon is not None:
            return lat, lon

        # 地址 geocoding
        if address:
            coords = self._geocode_cached(address)
            if coords:
                return coords

        # 邮编 geocoding（加上国家防止解析失败）
        if postal:
            coords = self._geocode_cached(f"{postal}, USA")
            if coords:
                return coords

        # 如果都失败，返回 None
        return None, None

    @cache.memoize(timeout=30*24*60*60)  # 30天缓存
    def _geocode_cached(self, address):
        """
        带缓存的地理编码
        """
        try:
            location = self.geocoder.geocode(address, timeout=10)
            if location:
                print(f"[Geocode] {address} -> {location.latitude}, {location.longitude}")
                return location.latitude, location.longitude
            else:
                print(f"[Geocode failed] {address} returned None")
        except Exception as e:
            print(f"[Geocoding error] {address}: {e}")
        return None, None
