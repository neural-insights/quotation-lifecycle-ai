from sqlalchemy import (Column, Integer, String, Float, ForeignKey, DateTime, Boolean)
from sqlalchemy.orm import relationship, declarative_base
from utils.db import Base
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
    id = Column(Integer, ForeignKey("quotation_responses.id"), primary_key=True)
    performance_score  = Column(Float)
    won = Column(Float)

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
    
class MergedQuote(Base):
    __tablename__ = "merged_quotes"

    id = Column(Integer, primary_key=True, autoincrement=True) 
    client_request_id = Column(Integer, nullable=False)
    customer_id = Column(String, nullable=True)  
    supplier_id = Column(Integer, nullable=False)
    supplier_name = Column(String, nullable=False)
    supplier_performance_score = Column(Float, nullable=True)
    quotation_response_id = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    delivery_days = Column(Integer, nullable=False)
    rfq_sent_at = Column(DateTime, nullable=False)
    ml_score = Column(Float, nullable=True)
    heuristic_score = Column(Float, nullable=True)


class SelectedQuote(Base):
    __tablename__ = "selected_quotes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_request_id = Column(Integer, nullable=False)
    customer_id = Column(String, nullable=True)
    supplier_id = Column(Integer, nullable=False)
    supplier_name = Column(String, nullable=False)
    supplier_performance_score = Column(Float, nullable=True)
    quotation_response_id = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    profit_margin = Column(Float, nullable=True)
    delivery_days = Column(Integer, nullable=False)
    rfq_sent_at = Column(DateTime, nullable=False)
    heuristic_score = Column(Float, nullable=True)
