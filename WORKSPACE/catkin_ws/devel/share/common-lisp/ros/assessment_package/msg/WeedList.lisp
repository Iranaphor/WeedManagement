; Auto-generated. Do not edit!


(cl:in-package assessment_package-msg)


;//! \htmlinclude WeedList.msg.html

(cl:defclass <WeedList> (roslisp-msg-protocol:ros-message)
  ((id
    :reader id
    :initarg :id
    :type cl:fixnum
    :initform 0)
   (plant_type
    :reader plant_type
    :initarg :plant_type
    :type cl:string
    :initform "")
   (weeds
    :reader weeds
    :initarg :weeds
    :type std_msgs-msg:Float64MultiArray
    :initform (cl:make-instance 'std_msgs-msg:Float64MultiArray)))
)

(cl:defclass WeedList (<WeedList>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <WeedList>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'WeedList)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name assessment_package-msg:<WeedList> is deprecated: use assessment_package-msg:WeedList instead.")))

(cl:ensure-generic-function 'id-val :lambda-list '(m))
(cl:defmethod id-val ((m <WeedList>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader assessment_package-msg:id-val is deprecated.  Use assessment_package-msg:id instead.")
  (id m))

(cl:ensure-generic-function 'plant_type-val :lambda-list '(m))
(cl:defmethod plant_type-val ((m <WeedList>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader assessment_package-msg:plant_type-val is deprecated.  Use assessment_package-msg:plant_type instead.")
  (plant_type m))

(cl:ensure-generic-function 'weeds-val :lambda-list '(m))
(cl:defmethod weeds-val ((m <WeedList>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader assessment_package-msg:weeds-val is deprecated.  Use assessment_package-msg:weeds instead.")
  (weeds m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <WeedList>) ostream)
  "Serializes a message object of type '<WeedList>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'plant_type))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'plant_type))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'weeds) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <WeedList>) istream)
  "Deserializes a message object of type '<WeedList>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'plant_type) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'plant_type) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'weeds) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<WeedList>)))
  "Returns string type for a message object of type '<WeedList>"
  "assessment_package/WeedList")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'WeedList)))
  "Returns string type for a message object of type 'WeedList"
  "assessment_package/WeedList")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<WeedList>)))
  "Returns md5sum for a message object of type '<WeedList>"
  "588c1046d234341b634ae5542e1e9e02")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'WeedList)))
  "Returns md5sum for a message object of type 'WeedList"
  "588c1046d234341b634ae5542e1e9e02")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<WeedList>)))
  "Returns full string definition for message of type '<WeedList>"
  (cl:format cl:nil "uint8 id~%string plant_type~%std_msgs/Float64MultiArray weeds~%~%================================================================================~%MSG: std_msgs/Float64MultiArray~%# Please look at the MultiArrayLayout message definition for~%# documentation on all multiarrays.~%~%MultiArrayLayout  layout        # specification of data layout~%float64[]         data          # array of data~%~%~%================================================================================~%MSG: std_msgs/MultiArrayLayout~%# The multiarray declares a generic multi-dimensional array of a~%# particular data type.  Dimensions are ordered from outer most~%# to inner most.~%~%MultiArrayDimension[] dim # Array of dimension properties~%uint32 data_offset        # padding elements at front of data~%~%# Accessors should ALWAYS be written in terms of dimension stride~%# and specified outer-most dimension first.~%# ~%# multiarray(i,j,k) = data[data_offset + dim_stride[1]*i + dim_stride[2]*j + k]~%#~%# A standard, 3-channel 640x480 image with interleaved color channels~%# would be specified as:~%#~%# dim[0].label  = \"height\"~%# dim[0].size   = 480~%# dim[0].stride = 3*640*480 = 921600  (note dim[0] stride is just size of image)~%# dim[1].label  = \"width\"~%# dim[1].size   = 640~%# dim[1].stride = 3*640 = 1920~%# dim[2].label  = \"channel\"~%# dim[2].size   = 3~%# dim[2].stride = 3~%#~%# multiarray(i,j,k) refers to the ith row, jth column, and kth channel.~%~%================================================================================~%MSG: std_msgs/MultiArrayDimension~%string label   # label of given dimension~%uint32 size    # size of given dimension (in type units)~%uint32 stride  # stride of given dimension~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'WeedList)))
  "Returns full string definition for message of type 'WeedList"
  (cl:format cl:nil "uint8 id~%string plant_type~%std_msgs/Float64MultiArray weeds~%~%================================================================================~%MSG: std_msgs/Float64MultiArray~%# Please look at the MultiArrayLayout message definition for~%# documentation on all multiarrays.~%~%MultiArrayLayout  layout        # specification of data layout~%float64[]         data          # array of data~%~%~%================================================================================~%MSG: std_msgs/MultiArrayLayout~%# The multiarray declares a generic multi-dimensional array of a~%# particular data type.  Dimensions are ordered from outer most~%# to inner most.~%~%MultiArrayDimension[] dim # Array of dimension properties~%uint32 data_offset        # padding elements at front of data~%~%# Accessors should ALWAYS be written in terms of dimension stride~%# and specified outer-most dimension first.~%# ~%# multiarray(i,j,k) = data[data_offset + dim_stride[1]*i + dim_stride[2]*j + k]~%#~%# A standard, 3-channel 640x480 image with interleaved color channels~%# would be specified as:~%#~%# dim[0].label  = \"height\"~%# dim[0].size   = 480~%# dim[0].stride = 3*640*480 = 921600  (note dim[0] stride is just size of image)~%# dim[1].label  = \"width\"~%# dim[1].size   = 640~%# dim[1].stride = 3*640 = 1920~%# dim[2].label  = \"channel\"~%# dim[2].size   = 3~%# dim[2].stride = 3~%#~%# multiarray(i,j,k) refers to the ith row, jth column, and kth channel.~%~%================================================================================~%MSG: std_msgs/MultiArrayDimension~%string label   # label of given dimension~%uint32 size    # size of given dimension (in type units)~%uint32 stride  # stride of given dimension~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <WeedList>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'plant_type))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'weeds))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <WeedList>))
  "Converts a ROS message object to a list"
  (cl:list 'WeedList
    (cl:cons ':id (id msg))
    (cl:cons ':plant_type (plant_type msg))
    (cl:cons ':weeds (weeds msg))
))
