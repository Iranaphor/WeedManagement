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
      this.weed_id = null;
      this.row_id = null;
      this.x = null;
      this.y = null;
    }
    else {
      if (initObj.hasOwnProperty('weed_id')) {
        this.weed_id = initObj.weed_id
      }
      else {
        this.weed_id = 0;
      }
      if (initObj.hasOwnProperty('row_id')) {
        this.row_id = initObj.row_id
      }
      else {
        this.row_id = 0;
      }
      if (initObj.hasOwnProperty('x')) {
        this.x = initObj.x
      }
      else {
        this.x = 0;
      }
      if (initObj.hasOwnProperty('y')) {
        this.y = initObj.y
      }
      else {
        this.y = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type weed_location
    // Serialize message field [weed_id]
    bufferOffset = _serializer.uint32(obj.weed_id, buffer, bufferOffset);
    // Serialize message field [row_id]
    bufferOffset = _serializer.uint8(obj.row_id, buffer, bufferOffset);
    // Serialize message field [x]
    bufferOffset = _serializer.uint8(obj.x, buffer, bufferOffset);
    // Serialize message field [y]
    bufferOffset = _serializer.uint8(obj.y, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type weed_location
    let len;
    let data = new weed_location(null);
    // Deserialize message field [weed_id]
    data.weed_id = _deserializer.uint32(buffer, bufferOffset);
    // Deserialize message field [row_id]
    data.row_id = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [x]
    data.x = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [y]
    data.y = _deserializer.uint8(buffer, bufferOffset);
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
    return 'fc8bc5e93d03fc0fbc549a0dab8e8013';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint32 weed_id
    uint8 row_id
    uint8 x
    uint8 y
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new weed_location(null);
    if (msg.weed_id !== undefined) {
      resolved.weed_id = msg.weed_id;
    }
    else {
      resolved.weed_id = 0
    }

    if (msg.row_id !== undefined) {
      resolved.row_id = msg.row_id;
    }
    else {
      resolved.row_id = 0
    }

    if (msg.x !== undefined) {
      resolved.x = msg.x;
    }
    else {
      resolved.x = 0
    }

    if (msg.y !== undefined) {
      resolved.y = msg.y;
    }
    else {
      resolved.y = 0
    }

    return resolved;
    }
};

module.exports = weed_location;
