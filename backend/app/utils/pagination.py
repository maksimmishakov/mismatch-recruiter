"""Advanced pagination utilities for list endpoints."""

from flask import request
from typing import Dict, List, Any, Optional


class PaginationParams:
    """Pagination parameters extractor."""
    
    # Default values
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100
    
    def __init__(self):
        """Initialize pagination parameters from request."""
        self.page = self._get_page()
        self.per_page = self._get_per_page()
        self.sort_by = self._get_sort_by()
        self.sort_order = self._get_sort_order()
        self.search = self._get_search()
        self.filters = self._get_filters()
    
    @staticmethod
    def _get_page() -> int:
        """Extract page number from request."""
        try:
            page = int(request.args.get('page', PaginationParams.DEFAULT_PAGE))
            return max(1, page)  # Ensure page >= 1
        except (ValueError, TypeError):
            return PaginationParams.DEFAULT_PAGE
    
    @staticmethod
    def _get_per_page() -> int:
        """Extract items per page from request."""
        try:
            per_page = int(request.args.get('per_page', PaginationParams.DEFAULT_PER_PAGE))
            # Ensure per_page is within bounds
            per_page = max(1, min(per_page, PaginationParams.MAX_PER_PAGE))
            return per_page
        except (ValueError, TypeError):
            return PaginationParams.DEFAULT_PER_PAGE
    
    @staticmethod
    def _get_sort_by() -> Optional[str]:
        """Extract sort field from request."""
        return request.args.get('sort_by')
    
    @staticmethod
    def _get_sort_order() -> str:
        """Extract sort order from request."""
        order = request.args.get('sort_order', 'asc').lower()
        return 'asc' if order == 'asc' else 'desc'
    
    @staticmethod
    def _get_search() -> Optional[str]:
        """Extract search query from request."""
        return request.args.get('search')
    
    @staticmethod
    def _get_filters() -> Dict[str, Any]:
        """Extract filter parameters from request."""
        filters = {}
        # Extract common filters
        for key in ['status', 'role', 'experience_level', 'job_type']:
            value = request.args.get(key)
            if value:
                filters[key] = value
        return filters
    
    def get_offset(self) -> int:
        """Calculate database offset."""
        return (self.page - 1) * self.per_page


class PaginationResponse:
    """Format pagination response."""
    
    @staticmethod
    def create_response(
        items: List[Dict],
        total: int,
        page: int,
        per_page: int,
        **kwargs
    ) -> Dict[str, Any]:
        """Create formatted pagination response.
        
        Args:
            items: List of items for current page
            total: Total number of items
            page: Current page number
            per_page: Items per page
            **kwargs: Additional data to include in response
            
        Returns:
            Formatted pagination response dictionary
        """
        total_pages = (total + per_page - 1) // per_page  # Ceiling division
        
        response = {
            'data': items,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1,
            }
        }
        
        # Add any additional data
        response.update(kwargs)
        
        return response
