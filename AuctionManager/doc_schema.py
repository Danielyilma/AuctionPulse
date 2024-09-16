auction_creation_schema = {
  "type": "object",
  "properties": {
    "item": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "example": "Guitar"
        },
        "condition": {
          "type": "string",
          "enum": ["new", "used", "refurbished"],
          "example": "used"
        },
        "main_image": {
          "type": "string",
          "example": "image_url_or_base64"
        }
      },
      "required": ["name", "condition", "main_image"]
    },
    "title": {
      "type": "string",
      "example": "Vintage Guitar"
    },
    "description": {
      "type": "string",
      "example": "A beautiful vintage guitar from the 1960s, in excellent condition."
    },
    "duration": {
      "type": "integer",
      "example": 1, 
      "description": "Duration in days (example: 1 day)"
    },
    "start_time": {
      "type": "string",
      "format": "date-time",
      "example": "2024-09-16 10:33:12"
    },
    "starting_price": {
      "type": "string",
      "pattern": "^[0-9]+(\.[0-9]{1,2})?$",
      "example": "200.35",
      "description": "Starting price with up to two decimal places."
    },
    "timezone": {
        "type": "string",
        "example": "Africa/Addis_Ababa"
    },
    "images": {
        "type": "array",
        "description": "List of images to upload for the auction",
        "example": ["image1.jpg", "image2.jpg"]
    }

  },
  "required": ["item", "title", "duration", "start_time", "starting_price", 'timezone', 'images']
}
