
(cl:in-package :asdf)

(defsystem "assessment_package-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "weed_location" :depends-on ("_package_weed_location"))
    (:file "_package_weed_location" :depends-on ("_package"))
  ))