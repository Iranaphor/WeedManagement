// Auto-generated. Do not edit!

// (in-package assessment_package.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class WeedList {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.id = null;
      this.plant_type = null;
      this.weeds = null;
    }
    else {
      if (initObj.hasOwnProperty('id')) {
        this.id = initObj.id
      }
      else {
        this.id = 0;
      }
      if (initObj.hasOwnProperty('plant_type')) {
        this.plant_type = initObj.plant_type
      }
      else {
        this.plant_type = '';
      }
      if (initObj.hasOwnProperty('weeds')) {
        this.weeds = initObj.weeds
      }
      else {
        this.weeds = new std_msgs.msg.Float64MultiArray();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type WeedList
    // Serialize message field [id]
    bufferOffset = _serializer.uint8(obj.id, buffer, bufferOffset);
    // Serialize message field [plant_type]
    bufferOffset = _serializer.string(obj.plant_type, buffer, bufferOffset);
    // Serialize message field [weeds]
    bufferOffset = std_msgs.msg.Float64MultiArray.serialize(obj.weeds, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type WeedList
    let len;
    let data = new WeedList(null);
    // Deserialize message field [id]
    data.id = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [plant_type]
    data.plant_type = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [weeds]
    data.weeds = std_msgs.msg.Float64MultiArray.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.plant_type.length;
    length += std_msgs.msg.Float64MultiArray.getMessageSize(object.weeds);
    return length + 5;
  }

  static datatype() {
    // Returns string type for a message object
    return 'assessment_package/WeedList';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '588c1046d234341b634ae5542e1e9e02';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint8 id
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
    # dim[0].label  = "height"
    # dim[0].size   = 480
    # dim[0].stride = 3*640*480 = 921600  (note dim[0] stride is just size of image)
    # dim[1].label  = "width"
    # dim[1].size   = 640
    # dim[1].stride = 3*640 = 1920
    # dim[2].label  = "channel"
    # dim[2].size   = 3
    # dim[2].stride = 3
    #
    # multiarray(i,j,k) refers to the ith row, jth column, and kth channel.
    
    ================================================================================
    MSG: std_msgs/MultiArrayDimension
    string label   # label of given dimension
    uint32 size    # size of given dimension (in type units)
    uint32 stride  # stride of given dimension
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new WeedList(null);
    if (msg.id !== undefined) {
      resolved.id = msg.id;
    }
    else {
      resolved.id = 0
    }

    if (msg.plant_type !== undefined) {
      resolved.plant_type = msg.plant_type;
    }
    else {
      resolved.plant_type = ''
    }

    if (msg.weeds !== undefined) {
      resolved.weeds = std_msgs.msg.Float64MultiArray.Resolve(msg.weeds)
    }
    else {
      resolved.weeds = new std_msgs.msg.Float64MultiArray()
    }

    return resolved;
    }
};

module.exports = WeedList;