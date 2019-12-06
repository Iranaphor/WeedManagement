;; Auto-generated. Do not edit!


(when (boundp 'assessment_package::weed_location)
  (if (not (find-package "ASSESSMENT_PACKAGE"))
    (make-package "ASSESSMENT_PACKAGE"))
  (shadow 'weed_location (find-package "ASSESSMENT_PACKAGE")))
(unless (find-package "ASSESSMENT_PACKAGE::WEED_LOCATION")
  (make-package "ASSESSMENT_PACKAGE::WEED_LOCATION"))

(in-package "ROS")
;;//! \htmlinclude weed_location.msg.html


(defclass assessment_package::weed_location
  :super ros::object
  :slots (_weed_id _row_id _x _y ))

(defmethod assessment_package::weed_location
  (:init
   (&key
    ((:weed_id __weed_id) 0)
    ((:row_id __row_id) 0)
    ((:x __x) 0)
    ((:y __y) 0)
    )
   (send-super :init)
   (setq _weed_id (round __weed_id))
   (setq _row_id (round __row_id))
   (setq _x (round __x))
   (setq _y (round __y))
   self)
  (:weed_id
   (&optional __weed_id)
   (if __weed_id (setq _weed_id __weed_id)) _weed_id)
  (:row_id
   (&optional __row_id)
   (if __row_id (setq _row_id __row_id)) _row_id)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:serialization-length
   ()
   (+
    ;; uint32 _weed_id
    4
    ;; uint8 _row_id
    1
    ;; uint8 _x
    1
    ;; uint8 _y
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint32 _weed_id
       (write-long _weed_id s)
     ;; uint8 _row_id
       (write-byte _row_id s)
     ;; uint8 _x
       (write-byte _x s)
     ;; uint8 _y
       (write-byte _y s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint32 _weed_id
     (setq _weed_id (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; uint8 _row_id
     (setq _row_id (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _x
     (setq _x (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _y
     (setq _y (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get assessment_package::weed_location :md5sum-) "fc8bc5e93d03fc0fbc549a0dab8e8013")
(setf (get assessment_package::weed_location :datatype-) "assessment_package/weed_location")
(setf (get assessment_package::weed_location :definition-)
      "uint32 weed_id
uint8 row_id
uint8 x
uint8 y

")



(provide :assessment_package/weed_location "fc8bc5e93d03fc0fbc549a0dab8e8013")


