// Auto-generated. Do not edit!

// (in-package assessment_package.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class weed_location {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.id = null;
      this.row = null;
      this.xpos = null;
      this.ypos = null;
    }
    else {
      if (initObj.hasOwnProperty('id')) {
        this.id = initObj.id
      }
      else {
        this.id = 0;
      }
      if (initObj.hasOwnProperty('row')) {
        this.row = initObj.row
      }
      else {
        this.row = 0;
      }
      if (initObj.hasOwnProperty('xpos')) {
        this.xpos = initObj.xpos
      }
      else {
        this.xpos = 0;
      }
      if (initObj.hasOwnProperty('ypos')) {
        this.ypos = initObj.ypos
      }
      else {
        this.ypos = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type weed_location
    // Serialize message field [id]
    bufferOffset = _serializer.uint32(obj.id, buffer, bufferOffset);
    // Serialize message field [row]
    bufferOffset = _serializer.uint8(obj.row, buffer, bufferOffset);
    // Serialize message field [xpos]
    bufferOffset = _serializer.uint8(obj.xpos, buffer, bufferOffset);
    // Serialize message field [ypos]
    bufferOffset = _serializer.uint8(obj.ypos, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type weed_location
    let len;
    let data = new weed_location(null);
    // Deserialize message field [id]
    data.id = _deserializer.uint32(buffer, bufferOffset);
    // Deserialize message field [row]
    data.row = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [xpos]
    data.xpos = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [ypos]
    data.ypos = _deserializer.uint8(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 7;
  }

  static datatype() {
    // Returns string type for a message object
    return 'assessment_package/weed_location';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '7f660f9d4b49f000c880a057d53b40c1';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint32 id
    uint8 row
    uint8 xpos
    uint8 ypos
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new weed_location(null);
    if (msg.id !== undefined) {
      resolved.id = msg.id;
    }
    else {
      resolved.id = 0
    }

    if (msg.row !== undefined) {
      resolved.row = msg.row;
    }
    else {
      resolved.row = 0
    }

    if (msg.xpos !== undefined) {
      resolved.xpos = msg.xpos;
    }
    else {
      resolved.xpos = 0
    }

    if (msg.ypos !== undefined) {
      resolved.ypos = msg.ypos;
    }
    else {
      resolved.ypos = 0
    }

    return resolved;
    }
};

module.exports = weed_location;
