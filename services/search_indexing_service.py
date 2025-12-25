import logging
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import json

logger = logging.getLogger(__name__)

@dataclass
class IndexedDocument:
    doc_id: str
    title: str
    content: str
    metadata: Dict[str, Any]
    indexed_at: datetime
    relevance_score: float = 0.0

class SearchIndexingService:
    def __init__(self):
        self.index = {}  # inverted index: term -> set of doc_ids
        self.documents = {}  # doc_id -> IndexedDocument
        self.index_stats = {
            'total_docs': 0,
            'total_terms': 0,
            'last_index_time': None
        }
    
    def index_document(self, 
                      doc_id: str,
                      title: str,
                      content: str,
                      metadata: Optional[Dict] = None) -> bool:
        """Index a document for full-text search"""
        try:
            document = IndexedDocument(
                doc_id=doc_id,
                title=title,
                content=content,
                metadata=metadata or {},
                indexed_at=datetime.now()
            )
            
            # Remove old document if exists
            if doc_id in self.documents:
                self._remove_document_terms(doc_id)
            
            # Extract and index terms from title and content
            text = f"{title} {content}".lower()
            terms = self._tokenize(text)
            
            for term in terms:
                if term not in self.index:
                    self.index[term] = set()
                self.index[term].add(doc_id)
            
            self.documents[doc_id] = document
            self.index_stats['total_docs'] = len(self.documents)
            self.index_stats['total_terms'] = len(self.index)
            self.index_stats['last_index_time'] = datetime.now()
            
            logger.info(f'Document indexed: {doc_id}')
            return True
        except Exception as e:
            logger.error(f'Indexing error: {str(e)}')
            return False
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into searchable terms"""
        import re
        # Simple tokenization: lowercase, remove punctuation, split
        words = re.findall(r'\b\w+\b', text.lower())
        # Filter stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        return [w for w in words if w not in stop_words and len(w) > 2]
    
    def _remove_document_terms(self, doc_id: str) -> None:
        """Remove a document from index"""
        if doc_id in self.documents:
            terms_to_remove = []
            for term, doc_ids in self.index.items():
                if doc_id in doc_ids:
                    doc_ids.discard(doc_id)
                    if not doc_ids:
                        terms_to_remove.append(term)
            
            for term in terms_to_remove:
                del self.index[term]
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search documents using query terms"""
        try:
            query_terms = self._tokenize(query)
            if not query_terms:
                return []
            
            # Find documents matching all query terms (AND search)
            matching_docs = None
            for term in query_terms:
                if term in self.index:
                    if matching_docs is None:
                        matching_docs = set(self.index[term])
                    else:
                        matching_docs &= self.index[term]
                else:
                    matching_docs = set()
                    break
            
            if not matching_docs:
                return []
            
            # Score and rank results
            results = []
            for doc_id in matching_docs:
                doc = self.documents[doc_id]
                # Calculate relevance based on term frequency
                score = sum(1 for term in query_terms if term in doc.content.lower())
                results.append({
                    'doc_id': doc.doc_id,
                    'title': doc.title,
                    'relevance_score': score,
                    'metadata': doc.metadata
                })
            
            # Sort by relevance and return top results
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            logger.info(f'Search query executed: {query}, results: {len(results[:limit])}')
            return results[:limit]
        except Exception as e:
            logger.error(f'Search error: {str(e)}')
            return []
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from index"""
        try:
            if doc_id in self.documents:
                self._remove_document_terms(doc_id)
                del self.documents[doc_id]
                self.index_stats['total_docs'] -= 1
                logger.info(f'Document deleted: {doc_id}')
                return True
            return False
        except Exception as e:
            logger.error(f'Delete error: {str(e)}')
            return False
    
    def bulk_index(self, documents: List[Dict]) -> Dict:
        """Index multiple documents"""
        indexed = 0
        failed = 0
        
        for doc in documents:
            if self.index_document(
                doc['id'],
                doc.get('title', ''),
                doc.get('content', ''),
                doc.get('metadata')
            ):
                indexed += 1
            else:
                failed += 1
        
        logger.info(f'Bulk indexing: {indexed} indexed, {failed} failed')
        return {'indexed': indexed, 'failed': failed}
    
    def get_index_stats(self) -> Dict:
        """Get indexing statistics"""
        return {
            'total_documents': self.index_stats['total_docs'],
            'total_terms': self.index_stats['total_terms'],
            'last_index_time': self.index_stats['last_index_time'].isoformat() if self.index_stats['last_index_time'] else None,
            'index_size_mb': sum(len(self.documents[doc_id].content) for doc_id in self.documents) / (1024 * 1024)
        }
