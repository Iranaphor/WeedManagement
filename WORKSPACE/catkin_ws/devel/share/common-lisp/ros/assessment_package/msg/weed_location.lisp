; Auto-generated. Do not edit!


(cl:in-package assessment_package-msg)


;//! \htmlinclude weed_location.msg.html

(cl:defclass <weed_location> (roslisp-msg-protocol:ros-message)
  ((weed_id
    :reader weed_id
    :initarg :weed_id
    :type cl:integer
    :initform 0)
   (row_id
    :reader row_id
    :initarg :row_id
    :type cl:fixnum
    :initform 0)
   (x
    :reader x
    :initarg :x
    :type cl:fixnum
    :initform 0)
   (y
    :reader y
    :initarg :y
    :type cl:fixnum
    :initform 0))
)

(cl:defclass weed_location (<weed_location>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <weed_location>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'weed_location)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name assessment_package-msg:<weed_location> is deprecated: use assessment_package-msg:weed_location instead.")))

(cl:ensure-generic-function 'weed_id-val :lambda-list '(m))
(cl:defmethod weed_id-val ((m <weed_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader assessment_package-msg:weed_id-val is deprecated.  Use assessment_package-msg:weed_id instead.")
  (weed_id m))

(cl:ensure-generic-function 'row_id-val :lambda-list '(m))
(cl:defmethod row_id-val ((m <weed_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader assessment_package-msg:row_id-val is deprecated.  Use assessment_package-msg:row_id instead.")
  (row_id m))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <weed_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader assessment_package-msg:x-val is deprecated.  Use assessment_package-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <weed_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader assessment_package-msg:y-val is deprecated.  Use assessment_package-msg:y instead.")
  (y m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <weed_location>) ostream)
  "Serializes a message object of type '<weed_location>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'weed_id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'weed_id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'weed_id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'weed_id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'row_id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'x)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'y)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <weed_location>) istream)
  "Deserializes a message object of type '<weed_location>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'weed_id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'weed_id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'weed_id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'weed_id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'row_id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'x)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'y)) (cl:read-byte istream))
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
  "fc8bc5e93d03fc0fbc549a0dab8e8013")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'weed_location)))
  "Returns md5sum for a message object of type 'weed_location"
  "fc8bc5e93d03fc0fbc549a0dab8e8013")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<weed_location>)))
  "Returns full string definition for message of type '<weed_location>"
  (cl:format cl:nil "uint32 weed_id~%uint8 row_id~%uint8 x~%uint8 y~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'weed_location)))
  "Returns full string definition for message of type 'weed_location"
  (cl:format cl:nil "uint32 weed_id~%uint8 row_id~%uint8 x~%uint8 y~%~%~%"))
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
    (cl:cons ':weed_id (weed_id msg))
    (cl:cons ':row_id (row_id msg))
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
))
