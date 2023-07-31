from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from database import Base

class Employee(Base):
    __tablename__='employees'

    no_pegawai = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    no_hp = Column(String(100))
    alamat = Column(String(100))
    divisi_id = Column(Integer, ForeignKey("divisi.id"))

class Divisi(Base):
    __tablename__='divisi'

    id = Column(Integer, primary_key=True, index=True)
    divisi = Column(String(100))