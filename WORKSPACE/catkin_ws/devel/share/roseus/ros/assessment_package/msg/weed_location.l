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
  :slots (_id _row _xpos _ypos ))

(defmethod assessment_package::weed_location
  (:init
   (&key
    ((:id __id) 0)
    ((:row __row) 0)
    ((:xpos __xpos) 0)
    ((:ypos __ypos) 0)
    )
   (send-super :init)
   (setq _id (round __id))
   (setq _row (round __row))
   (setq _xpos (round __xpos))
   (setq _ypos (round __ypos))
   self)
  (:id
   (&optional __id)
   (if __id (setq _id __id)) _id)
  (:row
   (&optional __row)
   (if __row (setq _row __row)) _row)
  (:xpos
   (&optional __xpos)
   (if __xpos (setq _xpos __xpos)) _xpos)
  (:ypos
   (&optional __ypos)
   (if __ypos (setq _ypos __ypos)) _ypos)
  (:serialization-length
   ()
   (+
    ;; uint32 _id
    4
    ;; uint8 _row
    1
    ;; uint8 _xpos
    1
    ;; uint8 _ypos
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint32 _id
       (write-long _id s)
     ;; uint8 _row
       (write-byte _row s)
     ;; uint8 _xpos
       (write-byte _xpos s)
     ;; uint8 _ypos
       (write-byte _ypos s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint32 _id
     (setq _id (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; uint8 _row
     (setq _row (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _xpos
     (setq _xpos (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _ypos
     (setq _ypos (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get assessment_package::weed_location :md5sum-) "7f660f9d4b49f000c880a057d53b40c1")
(setf (get assessment_package::weed_location :datatype-) "assessment_package/weed_location")
(setf (get assessment_package::weed_location :definition-)
      "uint32 id
uint8 row
uint8 xpos
uint8 ypos


")



(provide :assessment_package/weed_location "7f660f9d4b49f000c880a057d53b40c1")


