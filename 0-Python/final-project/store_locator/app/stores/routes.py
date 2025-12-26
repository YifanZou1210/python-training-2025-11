"""
店铺搜索路由
公开API端点
"""
from flask import Blueprint, request, jsonify
from store_locator.app.stores.search import StoreSearchService
from store_locator.app.extensions import limiter

stores_bp = Blueprint('stores', __name__, url_prefix='/api/stores')

@stores_bp.route('/search', methods=['POST'])
@limiter.limit("10 per minute")   # 短期限制
@limiter.limit("100 per hour")    # 长期限制
def search_stores():
    """
    店铺搜索端点（公开）
    
    请求体示例:
    {
        "postal_code": "02101",
        "radius_miles": 10,
        "services": ["pharmacy"],
        "open_now": false
    }
    
    或:
    {
        "latitude": 42.3601,
        "longitude": -71.0589,
        "radius_miles": 50
    }
    """
    data = request.get_json() or {}
    
    # 创建搜索服务实例
    service = StoreSearchService()
    
    # 执行搜索
    results = service.search_stores(
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        address=data.get('address'),
        postal_code=data.get('postal_code'),
        radius_miles=min(data.get('radius_miles', 10), 100),  # 最大100英里
        services=data.get('services', []),
        store_types=data.get('store_types', []),
        open_now=data.get('open_now', False),
        limit=data.get('limit', 20)
    )
    
    return jsonify(results), 200