; Auto-generated. Do not edit!


(cl:in-package assessment_package-msg)


;//! \htmlinclude weed_location.msg.html

(cl:defclass <weed_location> (roslisp-msg-protocol:ros-message)
  ((id
    :reader id
    :initarg :id
    :type cl:integer
    :initform 0)
   (row
    :reader row
    :initarg :row
    :type cl:fixnum
    :initform 0)
   (xpos
    :reader xpos
    :initarg :xpos
    :type cl:fixnum
    :initform 0)
   (ypos
    :reader ypos
    :initarg :ypos
    :type cl:fixnum
    :initform 0))
)

(cl:defclass weed_location (<weed_location>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <weed_location>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'weed_location)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name assessment_package-msg:<weed_location> is deprecated: use assessment_package-msg:weed_location instead.")))

(cl:ensure-generic-function 'id-val :lambda-list '(m))
(cl:defmethod id-val ((m <weed_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader assessment_package-msg:id-val is deprecated.  Use assessment_package-msg:id instead.")
  (id m))

(cl:ensure-generic-function 'row-val :lambda-list '(m))
(cl:defmethod row-val ((m <weed_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader assessment_package-msg:row-val is deprecated.  Use assessment_package-msg:row instead.")
  (row m))

(cl:ensure-generic-function 'xpos-val :lambda-list '(m))
(cl:defmethod xpos-val ((m <weed_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader assessment_package-msg:xpos-val is deprecated.  Use assessment_package-msg:xpos instead.")
  (xpos m))

(cl:ensure-generic-function 'ypos-val :lambda-list '(m))
(cl:defmethod ypos-val ((m <weed_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader assessment_package-msg:ypos-val is deprecated.  Use assessment_package-msg:ypos instead.")
  (ypos m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <weed_location>) ostream)
  "Serializes a message object of type '<weed_location>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'row)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'xpos)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'ypos)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <weed_location>) istream)
  "Deserializes a message object of type '<weed_location>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'row)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'xpos)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'ypos)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<weed_location>)))
  "Returns string type for a message object of type '<weed_location>"
  "assessment_package/weed_location")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'weed_location)))
  "Returns string type for a message object of type 'weed_location"
  "assessment_package/weed_location")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<weed_location>)))
  "Returns md5sum for a message object of type '<weed_location>"
  "7f660f9d4b49f000c880a057d53b40c1")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'weed_location)))
  "Returns md5sum for a message object of type 'weed_location"
  "7f660f9d4b49f000c880a057d53b40c1")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<weed_location>)))
  "Returns full string definition for message of type '<weed_location>"
  (cl:format cl:nil "uint32 id~%uint8 row~%uint8 xpos~%uint8 ypos~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'weed_location)))
  "Returns full string definition for message of type 'weed_location"
  (cl:format cl:nil "uint32 id~%uint8 row~%uint8 xpos~%uint8 ypos~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <weed_location>))
  (cl:+ 0
     4
     1
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <weed_location>))
  "Converts a ROS message object to a list"
  (cl:list 'weed_location
    (cl:cons ':id (id msg))
    (cl:cons ':row (row msg))
    (cl:cons ':xpos (xpos msg))
    (cl:cons ':ypos (ypos msg))
))
