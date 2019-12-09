
(cl:in-package :asdf)

(defsystem "assessment_package-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "WeedList" :depends-on ("_package_WeedList"))
    (:file "_package_WeedList" :depends-on ("_package"))
    (:file "weed_location" :depends-on ("_package_weed_location"))
    (:file "_package_weed_location" :depends-on ("_package"))
  ))