"""
地理计算工具函数
包含距离计算、边界框计算等
"""
import math
from geopy.distance import geodesic

def calculate_bounding_box(lat, lon, radius_miles):
    """
    计算搜索范围的边界框
    
    原理:
    - 纬度变化: 1度 ≈ 69英里
    - 经度变化: 1度 ≈ 69 * cos(纬度) 英里
    
    返回: (min_lat, max_lat, min_lon, max_lon)
    """
    lat_delta = radius_miles / 69.0
    lon_delta = radius_miles / (69.0 * math.cos(math.radians(lat)))
    
    return (
        lat - lat_delta,  # min_lat
        lat + lat_delta,  # max_lat
        lon - lon_delta,  # min_lon
        lon + lon_delta   # max_lon
    )

def calculate_distance(point1, point2):
    """
    计算两点间距离（英里）
    
    参数:
        point1: (latitude, longitude)
        point2: (latitude, longitude)
    
    返回: 距离（英里）
    """
    return geodesic(point1, point2).miles

def validate_coordinates(lat, lon):
    """验证经纬度合法性"""
    return -90 <= lat <= 90 and -180 <= lon <= 180

def validate_hours_format(hours):
    """
    验证营业时间格式
    
    有效格式:
    - "08:00-22:00"
    - "closed"
    """
    if not hours:
        return False
    
    hours = hours.lower().strip()
    if hours == 'closed':
        return True
    
    try:
        if '-' not in hours:
            return False
        parts = hours.split('-')
        for t in parts:
            h, m = map(int, t.strip().split(':'))
            if not (0 <= h <= 23 and 0 <= m <= 59):
                return False
        return True
    except:
        return False