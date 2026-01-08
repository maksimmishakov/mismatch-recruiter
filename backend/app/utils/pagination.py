from flask import request

class Pagination:
    """Pagination utility for list endpoints"""
    
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100
    
    @staticmethod
    def get_pagination_params():
        """Extract pagination parameters from request"""
        try:
            page = int(request.args.get('page', Pagination.DEFAULT_PAGE))
            per_page = int(request.args.get('per_page', Pagination.DEFAULT_PER_PAGE))
            
            # Validate
            page = max(1, page)
            per_page = min(per_page, Pagination.MAX_PER_PAGE)
            per_page = max(1, per_page)
            
            return page, per_page
        except (ValueError, TypeError):
            return Pagination.DEFAULT_PAGE, Pagination.DEFAULT_PER_PAGE
    
    @staticmethod
    def paginate_response(items, total_count, page, per_page):
        """Format paginated response"""
        total_pages = (total_count + per_page - 1) // per_page
        
        return {
            'items': items,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_count,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }
