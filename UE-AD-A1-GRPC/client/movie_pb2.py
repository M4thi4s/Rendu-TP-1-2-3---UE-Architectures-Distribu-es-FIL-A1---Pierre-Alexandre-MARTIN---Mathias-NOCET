# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: movie.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bmovie.proto\"\x15\n\x07MovieID\x12\n\n\x02id\x18\x01 \x01(\t\"+\n\x08\x45\x64itData\x12\x0f\n\x07movieID\x18\x01 \x01(\t\x12\x0e\n\x06rating\x18\x02 \x01(\x02\"\x1b\n\nMovieTitle\x12\r\n\x05title\x18\x01 \x01(\t\"H\n\tMovieData\x12\r\n\x05title\x18\x01 \x01(\t\x12\x0e\n\x06rating\x18\x02 \x01(\x02\x12\x10\n\x08\x64irector\x18\x03 \x01(\t\x12\n\n\x02id\x18\x04 \x01(\t\"\x07\n\x05\x45mpty2\xf9\x01\n\x05Movie\x12&\n\x0cGetMovieByID\x12\x08.MovieID\x1a\n.MovieData\"\x00\x12,\n\x0fGetMovieByTitle\x12\x0b.MovieTitle\x1a\n.MovieData\"\x00\x12\'\n\rGetListMovies\x12\x06.Empty\x1a\n.MovieData\"\x00\x30\x01\x12$\n\x08\x41\x64\x64Movie\x12\n.MovieData\x1a\n.MovieData\"\x00\x12%\n\x0b\x44\x65leteMovie\x12\x08.MovieID\x1a\n.MovieData\"\x00\x12$\n\tEditMovie\x12\t.EditData\x1a\n.MovieData\"\x00\x62\x06proto3')



_MOVIEID = DESCRIPTOR.message_types_by_name['MovieID']
_EDITDATA = DESCRIPTOR.message_types_by_name['EditData']
_MOVIETITLE = DESCRIPTOR.message_types_by_name['MovieTitle']
_MOVIEDATA = DESCRIPTOR.message_types_by_name['MovieData']
_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
MovieID = _reflection.GeneratedProtocolMessageType('MovieID', (_message.Message,), {
  'DESCRIPTOR' : _MOVIEID,
  '__module__' : 'movie_pb2'
  # @@protoc_insertion_point(class_scope:MovieID)
  })
_sym_db.RegisterMessage(MovieID)

EditData = _reflection.GeneratedProtocolMessageType('EditData', (_message.Message,), {
  'DESCRIPTOR' : _EDITDATA,
  '__module__' : 'movie_pb2'
  # @@protoc_insertion_point(class_scope:EditData)
  })
_sym_db.RegisterMessage(EditData)

MovieTitle = _reflection.GeneratedProtocolMessageType('MovieTitle', (_message.Message,), {
  'DESCRIPTOR' : _MOVIETITLE,
  '__module__' : 'movie_pb2'
  # @@protoc_insertion_point(class_scope:MovieTitle)
  })
_sym_db.RegisterMessage(MovieTitle)

MovieData = _reflection.GeneratedProtocolMessageType('MovieData', (_message.Message,), {
  'DESCRIPTOR' : _MOVIEDATA,
  '__module__' : 'movie_pb2'
  # @@protoc_insertion_point(class_scope:MovieData)
  })
_sym_db.RegisterMessage(MovieData)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'movie_pb2'
  # @@protoc_insertion_point(class_scope:Empty)
  })
_sym_db.RegisterMessage(Empty)

_MOVIE = DESCRIPTOR.services_by_name['Movie']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MOVIEID._serialized_start=15
  _MOVIEID._serialized_end=36
  _EDITDATA._serialized_start=38
  _EDITDATA._serialized_end=81
  _MOVIETITLE._serialized_start=83
  _MOVIETITLE._serialized_end=110
  _MOVIEDATA._serialized_start=112
  _MOVIEDATA._serialized_end=184
  _EMPTY._serialized_start=186
  _EMPTY._serialized_end=193
  _MOVIE._serialized_start=196
  _MOVIE._serialized_end=445
# @@protoc_insertion_point(module_scope)
