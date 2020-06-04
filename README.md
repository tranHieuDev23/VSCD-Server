# Vietnamese Speech Command Dataset - Backend

This is the backend used for the [Vietnamese Speech Command Dataset](https://vscd.now.sh), but it was written as a RESTful API server, which means that it can be used for any clients that follow its API.

## Dependencies
- Flask 1.1.2+
- python-dotenv 0.13.0+
- Flask-Cors 3.0.8+
- Flask-Compress 1.5.0+
- mysql-connector 2.2.9+
- requests 2.23.0+

A MySQL server to manage collected data is also required, with the username, password and database can be configured via an `.env` file.

## API

- POST `/api/speak-submit`: take in a `multipart/form-data` request with a field `authorId` - the user ID of the user who created the request - and serveral audio files, each file is in a field named after its class.
- POST `/api/get-validation-requests`: take in a JSON request with a field `userId` - the user ID of the user who created the request. It returns a JSON array of the form:
  ```
  [{"validationId": "...", "label": "..."},...]
  ```
  Each item in this array represents an audio file to be validated. Responding like this helps mitigate audio loading time - the user can load each audio file one by one with `/api/get-validation-audio`.
- POST `/api/get-validation-audio`: take in a JSON request with a field `validationId` - the ID of one item in the response of `/api/get-validation-requests`. If the audio of the item with that ID hasn't been validated yet, it returns the gzipped binary data of the audio.
- POST `/api/validation-submit`: take in a JSON array of the form:
  ```
  [{"validationId": "...", "result": true/false},...]
  ```
  that is the validation result of the validation items with corresponding IDs.

## LICENSE

MIT License