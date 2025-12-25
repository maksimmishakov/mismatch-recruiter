import stripe
import logging
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)
stripe.api_key = 'sk_live_...'  # Load from env

class PaymentStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'

@dataclass
class Payment:
    id: str
    amount: float
    currency: str
    status: PaymentStatus
    user_id: str
    candidate_id: Optional[str]
    created_at: datetime
    metadata: Dict

class PaymentService:
    def __init__(self):
        self.stripe = stripe
        self.payments = {}
    
    def create_payment_intent(self, 
                            amount: float, 
                            currency: str, 
                            user_id: str,
                            candidate_id: Optional[str] = None,
                            metadata: Optional[Dict] = None) -> Dict:
        """Create Stripe payment intent"""
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency=currency,
                metadata={
                    'user_id': user_id,
                    'candidate_id': candidate_id,
                    **(metadata or {})
                }
            )
            payment = Payment(
                id=intent.id,
                amount=amount,
                currency=currency,
                status=PaymentStatus.PENDING,
                user_id=user_id,
                candidate_id=candidate_id,
                created_at=datetime.now(),
                metadata=intent.metadata
            )
            self.payments[intent.id] = payment
            logger.info(f'Payment intent created: {intent.id}')
            return {'success': True, 'payment_intent': intent}
        except stripe.error.StripeError as e:
            logger.error(f'Stripe error: {str(e)}')
            return {'success': False, 'error': str(e)}
    
    def confirm_payment(self, payment_intent_id: str) -> Dict:
        """Confirm payment after client authorization"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            if intent.status == 'succeeded':
                self.payments[payment_intent_id].status = PaymentStatus.COMPLETED
                logger.info(f'Payment confirmed: {payment_intent_id}')
                return {'success': True, 'status': 'completed'}
            return {'success': False, 'status': intent.status}
        except Exception as e:
            logger.error(f'Payment confirmation error: {str(e)}')
            return {'success': False, 'error': str(e)}
    
    def refund_payment(self, payment_intent_id: str, amount: Optional[float] = None) -> Dict:
        """Refund payment (full or partial)"""
        try:
            if amount:
                refund = stripe.Refund.create(
                    payment_intent=payment_intent_id,
                    amount=int(amount * 100)
                )
            else:
                refund = stripe.Refund.create(payment_intent=payment_intent_id)
            
            self.payments[payment_intent_id].status = PaymentStatus.REFUNDED
            logger.info(f'Payment refunded: {payment_intent_id}')
            return {'success': True, 'refund_id': refund.id}
        except Exception as e:
            logger.error(f'Refund error: {str(e)}')
            return {'success': False, 'error': str(e)}
    
    def get_payment(self, payment_id: str) -> Optional[Payment]:
        """Get payment details"""
        return self.payments.get(payment_id)
    
    def get_payments_by_user(self, user_id: str) -> List[Payment]:
        """Get all payments for a user"""
        return [p for p in self.payments.values() if p.user_id == user_id]
    
    def get_payments_by_candidate(self, candidate_id: str) -> List[Payment]:
        """Get all payments related to a candidate"""
        return [p for p in self.payments.values() if p.candidate_id == candidate_id]
    
    def handle_webhook(self, event: Dict) -> Dict:
        """Handle Stripe webhook events"""
        event_type = event.get('type')
        
        if event_type == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            payment_id = payment_intent['id']
            if payment_id in self.payments:
                self.payments[payment_id].status = PaymentStatus.COMPLETED
            logger.info(f'Webhook: Payment succeeded {payment_id}')
        
        elif event_type == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            payment_id = payment_intent['id']
            if payment_id in self.payments:
                self.payments[payment_id].status = PaymentStatus.FAILED
            logger.error(f'Webhook: Payment failed {payment_id}')
        
        elif event_type == 'charge.refunded':
            charge = event['data']['object']
            logger.info(f'Webhook: Charge refunded {charge["id"]}')
        
        return {'success': True}
    
    def get_payment_analytics(self) -> Dict:
        """Get payment analytics"""
        total_revenue = sum(p.amount for p in self.payments.values() 
                          if p.status == PaymentStatus.COMPLETED)
        total_payments = len(self.payments)
        successful = len([p for p in self.payments.values() 
                         if p.status == PaymentStatus.COMPLETED])
        failed = len([p for p in self.payments.values() 
                     if p.status == PaymentStatus.FAILED])
        
        return {
            'total_revenue': total_revenue,
            'total_payments': total_payments,
            'successful_payments': successful,
            'failed_payments': failed,
            'success_rate': (successful / total_payments * 100) if total_payments > 0 else 0
        }
