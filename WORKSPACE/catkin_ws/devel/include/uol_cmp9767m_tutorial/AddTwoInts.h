// Generated by gencpp from file uol_cmp9767m_tutorial/AddTwoInts.msg
// DO NOT EDIT!


#ifndef UOL_CMP9767M_TUTORIAL_MESSAGE_ADDTWOINTS_H
#define UOL_CMP9767M_TUTORIAL_MESSAGE_ADDTWOINTS_H

#include <ros/service_traits.h>


#include <uol_cmp9767m_tutorial/AddTwoIntsRequest.h>
#include <uol_cmp9767m_tutorial/AddTwoIntsResponse.h>


namespace uol_cmp9767m_tutorial
{

struct AddTwoInts
{

typedef AddTwoIntsRequest Request;
typedef AddTwoIntsResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct AddTwoInts
} // namespace uol_cmp9767m_tutorial


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::uol_cmp9767m_tutorial::AddTwoInts > {
  static const char* value()
  {
    return "6a2e34150c00229791cc89ff309fff21";
  }

  static const char* value(const ::uol_cmp9767m_tutorial::AddTwoInts&) { return value(); }
};

template<>
struct DataType< ::uol_cmp9767m_tutorial::AddTwoInts > {
  static const char* value()
  {
    return "uol_cmp9767m_tutorial/AddTwoInts";
  }

  static const char* value(const ::uol_cmp9767m_tutorial::AddTwoInts&) { return value(); }
};


// service_traits::MD5Sum< ::uol_cmp9767m_tutorial::AddTwoIntsRequest> should match 
// service_traits::MD5Sum< ::uol_cmp9767m_tutorial::AddTwoInts > 
template<>
struct MD5Sum< ::uol_cmp9767m_tutorial::AddTwoIntsRequest>
{
  static const char* value()
  {
    return MD5Sum< ::uol_cmp9767m_tutorial::AddTwoInts >::value();
  }
  static const char* value(const ::uol_cmp9767m_tutorial::AddTwoIntsRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::uol_cmp9767m_tutorial::AddTwoIntsRequest> should match 
// service_traits::DataType< ::uol_cmp9767m_tutorial::AddTwoInts > 
template<>
struct DataType< ::uol_cmp9767m_tutorial::AddTwoIntsRequest>
{
  static const char* value()
  {
    return DataType< ::uol_cmp9767m_tutorial::AddTwoInts >::value();
  }
  static const char* value(const ::uol_cmp9767m_tutorial::AddTwoIntsRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::uol_cmp9767m_tutorial::AddTwoIntsResponse> should match 
// service_traits::MD5Sum< ::uol_cmp9767m_tutorial::AddTwoInts > 
template<>
struct MD5Sum< ::uol_cmp9767m_tutorial::AddTwoIntsResponse>
{
  static const char* value()
  {
    return MD5Sum< ::uol_cmp9767m_tutorial::AddTwoInts >::value();
  }
  static const char* value(const ::uol_cmp9767m_tutorial::AddTwoIntsResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::uol_cmp9767m_tutorial::AddTwoIntsResponse> should match 
// service_traits::DataType< ::uol_cmp9767m_tutorial::AddTwoInts > 
template<>
struct DataType< ::uol_cmp9767m_tutorial::AddTwoIntsResponse>
{
  static const char* value()
  {
    return DataType< ::uol_cmp9767m_tutorial::AddTwoInts >::value();
  }
  static const char* value(const ::uol_cmp9767m_tutorial::AddTwoIntsResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // UOL_CMP9767M_TUTORIAL_MESSAGE_ADDTWOINTS_H
