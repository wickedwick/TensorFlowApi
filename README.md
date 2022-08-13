# FastAPI TensorFlow API

## Introduction
A collection of API endpoints for that utilize TensorFlow to perform inference.

## How to use
- Command line:
    ```bash
    $ python3 image_classification/classifier.py --image_file ./house.jpeg --num_top_predictions 5
    ```
    Sample Response:
    ```
    [
      'picket fence, paling (score = 0.95398)',
      'worm fence, snake fence, snake-rail fence, Virginia fence (score = 0.03971)',
      'beacon, lighthouse, beacon light, pharos (score = 0.00019)',
      'boathouse (score = 0.00015)',
      'patio, terrace (score = 0.00007)'
    ]
    ```

- Run the API locally
  ```bash
  $ uvicorn app.main:app --reload
  ```
  and go to http://localhost:8000/docs to see the documentation.

## Run Tests
```bash
$ pytest
```
## Structure
```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── classify.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```
