from sqlalchemy import (Column, Integer, String, Float, ForeignKey, DateTime, Boolean)
from sqlalchemy.orm import relationship, declarative_base
from db import Base
import random

# Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    requests = relationship("ClientRequest", back_populates="customer")
    
class ClientRequest(Base):
    __tablename__ = "client_requests"
    id = Column(Integer, primary_key=True, index=True)
    product_type = Column(String)
    specifications = Column(String)
    color_spec = Column(String)
    quantity = Column(Integer)
    deadline = Column(DateTime)
    is_custom = Column(Boolean, default=False)
    
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="requests")
    rfqs_sent = relationship("RFQSent", back_populates="client_request")


class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    performance_score = Column(Float)  # Simulated value between 0.0 and 5.0
    supported_products = Column(String)

    rfqs_received = relationship("RFQSent", back_populates="supplier")


class RFQSent(Base):
    __tablename__ = "rfqs_sent"
    id = Column(Integer, primary_key=True)
    client_request_id = Column(Integer, ForeignKey("client_requests.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    sent_at = Column(DateTime)
    status = Column(String, default="sent") 

    client_request = relationship("ClientRequest", back_populates="rfqs_sent")
    supplier = relationship("Supplier", back_populates="rfqs_received")
    rfq_details = relationship("RFQDetails", back_populates="rfq", uselist=False)
    quotation_response = relationship("QuotationResponse", back_populates="rfq", uselist=False)


class RFQDetails(Base):
    __tablename__ = "rfq_details"
    id = Column(Integer, primary_key=True)
    rfq_id = Column(Integer, ForeignKey("rfqs_sent.id"))
    expected_format = Column(String)
    payment_terms = Column(String)
    response_deadline = Column(DateTime)
    notes = Column(String)

    product_type = Column(String)
    specifications = Column(String)
    color_spec = Column(String)

    rfq = relationship("RFQSent", back_populates="rfq_details")


class QuotationResponse(Base):
    __tablename__ = "quotation_responses"
    id = Column(Integer, primary_key=True)
    rfq_id = Column(Integer, ForeignKey("rfqs_sent.id"))
    unit_price = Column(Float)
    delivery_days = Column(Integer)
    received_at = Column(DateTime)

    rfq = relationship("RFQSent", back_populates="quotation_response")
    score = relationship("QuoteScore", back_populates="quotation", uselist=False)


class QuoteScore(Base):
    __tablename__ = "quote_scores"
    id = Column(Integer, primary_key=True)
    quotation_id = Column(Integer, ForeignKey("quotation_responses.id"))
    heuristic_score = Column(Float)
    ml_score = Column(Float)

    quotation = relationship("QuotationResponse", back_populates="score")


class TrainingQuotation(Base):
    __tablename__ = "training_quotations"
    id = Column(Integer, primary_key=True)
    unit_price = Column(Float)
    delivery_days = Column(Integer)
    performance_score = Column(Float)
    response_time = Column(Float)
    rfq_complexity_score = Column(Float)
    is_urgent = Column(Boolean)
    is_custom = Column(Boolean)
    won = Column(Boolean)

class RealQuotationData(Base):
    __tablename__ = "real_quotation_data"
    id = Column(Integer, primary_key=True)
    unit_price = Column(Float)
    delivery_days = Column(Integer)
    performance_score = Column(Float)
    response_time = Column(Float)
    rfq_complexity_score = Column(Float)
    is_urgent = Column(Boolean)
    is_custom = Column(Boolean)
    won = Column(Boolean)
    
class FinalQuote(Base):
    __tablename__ = "final_quotes"
    id = Column(Integer, primary_key=True)
    client_request_id = Column(Integer, ForeignKey("client_requests.id"))
    selected_supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    finalized_price = Column(Float)


class CustomerFeedback(Base):
    __tablename__ = "customer_feedback"
    id = Column(Integer, primary_key=True)
    final_quote_id = Column(Integer, ForeignKey("final_quotes.id"))
    accepted = Column(Boolean)
    reason = Column(String)


class PredictedOutcomes(Base):
    __tablename__ = "predicted_outcomes"
    id = Column(Integer, primary_key=True)
    client_request_id = Column(Integer, ForeignKey("client_requests.id"))
    predicted_supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    confidence_score = Column(Float)
