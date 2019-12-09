;; Auto-generated. Do not edit!


(when (boundp 'assessment_package::WeedList)
  (if (not (find-package "ASSESSMENT_PACKAGE"))
    (make-package "ASSESSMENT_PACKAGE"))
  (shadow 'WeedList (find-package "ASSESSMENT_PACKAGE")))
(unless (find-package "ASSESSMENT_PACKAGE::WEEDLIST")
  (make-package "ASSESSMENT_PACKAGE::WEEDLIST"))

(in-package "ROS")
;;//! \htmlinclude WeedList.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass assessment_package::WeedList
  :super ros::object
  :slots (_id _plant_type _weeds ))

(defmethod assessment_package::WeedList
  (:init
   (&key
    ((:id __id) 0)
    ((:plant_type __plant_type) "")
    ((:weeds __weeds) (instance std_msgs::Float64MultiArray :init))
    )
   (send-super :init)
   (setq _id (round __id))
   (setq _plant_type (string __plant_type))
   (setq _weeds __weeds)
   self)
  (:id
   (&optional __id)
   (if __id (setq _id __id)) _id)
  (:plant_type
   (&optional __plant_type)
   (if __plant_type (setq _plant_type __plant_type)) _plant_type)
  (:weeds
   (&rest __weeds)
   (if (keywordp (car __weeds))
       (send* _weeds __weeds)
     (progn
       (if __weeds (setq _weeds (car __weeds)))
       _weeds)))
  (:serialization-length
   ()
   (+
    ;; uint8 _id
    1
    ;; string _plant_type
    4 (length _plant_type)
    ;; std_msgs/Float64MultiArray _weeds
    (send _weeds :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _id
       (write-byte _id s)
     ;; string _plant_type
       (write-long (length _plant_type) s) (princ _plant_type s)
     ;; std_msgs/Float64MultiArray _weeds
       (send _weeds :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _id
     (setq _id (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; string _plant_type
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _plant_type (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; std_msgs/Float64MultiArray _weeds
     (send _weeds :deserialize buf ptr-) (incf ptr- (send _weeds :serialization-length))
   ;;
   self)
  )

(setf (get assessment_package::WeedList :md5sum-) "588c1046d234341b634ae5542e1e9e02")
(setf (get assessment_package::WeedList :datatype-) "assessment_package/WeedList")
(setf (get assessment_package::WeedList :definition-)
      "uint8 id
string plant_type
std_msgs/Float64MultiArray weeds

================================================================================
MSG: std_msgs/Float64MultiArray
# Please look at the MultiArrayLayout message definition for
# documentation on all multiarrays.

MultiArrayLayout  layout        # specification of data layout
float64[]         data          # array of data


================================================================================
MSG: std_msgs/MultiArrayLayout
# The multiarray declares a generic multi-dimensional array of a
# particular data type.  Dimensions are ordered from outer most
# to inner most.

MultiArrayDimension[] dim # Array of dimension properties
uint32 data_offset        # padding elements at front of data

# Accessors should ALWAYS be written in terms of dimension stride
# and specified outer-most dimension first.
# 
# multiarray(i,j,k) = data[data_offset + dim_stride[1]*i + dim_stride[2]*j + k]
#
# A standard, 3-channel 640x480 image with interleaved color channels
# would be specified as:
#
# dim[0].label  = \"height\"
# dim[0].size   = 480
# dim[0].stride = 3*640*480 = 921600  (note dim[0] stride is just size of image)
# dim[1].label  = \"width\"
# dim[1].size   = 640
# dim[1].stride = 3*640 = 1920
# dim[2].label  = \"channel\"
# dim[2].size   = 3
# dim[2].stride = 3
#
# multiarray(i,j,k) refers to the ith row, jth column, and kth channel.

================================================================================
MSG: std_msgs/MultiArrayDimension
string label   # label of given dimension
uint32 size    # size of given dimension (in type units)
uint32 stride  # stride of given dimension
")



(provide :assessment_package/WeedList "588c1046d234341b634ae5542e1e9e02")


