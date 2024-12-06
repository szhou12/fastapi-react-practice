from fastapi import FastAPI
from pydantic import BaseModel

"""
What it does: This creates an instance of the FastAPI application, which will serve as the core of your backend.
Why it's needed: The app object is where you define all your routes (URLs) and their corresponding logic. It acts as the central “brain” of the application.
"""
app = FastAPI()

# tutorial -> tutorial.py
# app -> FastAPI instance name defined above
# --reload -> to reflect code changes automatically
# uvicorn tutorial:app --reload

# http://127.0.0.1:8000/docs -> test out your defined routes

# pydantic model -> used to define the type of data we are gonna accept in json. it helps: 1. auto data type validation. 2. auto data parsing from JSON to a python object
# similar to Table Schema you design for database 

"""
What it does:
- This defines a Pydantic model named Data with a single attribute name, which must be a string.
- BaseModel is a Pydantic class used to create data validation and parsing models.

Why use Pydantic here:
- It ensures that the incoming data (e.g., JSON payload from the client) adheres to the defined schema.
- If the incoming data is invalid (e.g., name is missing or is not a string), FastAPI automatically returns a 422 Unprocessable Entity error to the client with details about the validation failure.
"""
class Data(BaseModel):
    name: str


"""
What it does:
- This defines a FastAPI route /create/ that handles POST requests.
- The data: Data parameter tells FastAPI to expect a JSON payload in the request body that matches the Data model.

What happens under the hood:
- FastAPI parses the incoming JSON payload into an instance of the Data model.
- It validates the payload to ensure it matches the schema defined by Data.
- If the payload is valid, the function proceeds with the data object. Otherwise, it returns an error response.
"""
@app.post("/create/")
async def create(data: Data):
    # This returns the validated data object as the response, nested inside another dictionary.
    # FastAPI automatically converts the data (a Pydantic model instance) back into JSON format for the client.
    return {"data": data}

"""
What it does: This is a route decorator. It defines a URL path (/test/) and specifies that this route responds to GET HTTP requests. 

Path Parameter (item_id):
- The item_id is a path parameter because it is part of the URL path (/test/{item_id}).
- The {item_id} placeholder in the route definition makes this parameter mandatory. Every request to this endpoint must include a value for item_id in the path.
- Role: Specifies the resource being accessed.
- Example Use Case:
	•	Retrieving a specific resource (e.g., user by ID, product by SKU).
	•	Example: /test/123 → Refers to the resource with item_id = 123.
- Required: Path parameters are always required because they define the endpoint’s URL structure.

Query Parameter (query):
- The query parameter is a query parameter because it is expected in the query string of the URL (the part after the ?).
- Query parameters are optional unless explicitly defined as required. In this case, FastAPI makes query mandatory because it has no default value.
- For example:
	•	URL: /test/123?query=456 → query will be 456.
	•	URL: /test/123 → This will raise an error because query is missing.
- Role: Provides additional information or filters for the request.
- Example Use Case:
	•	Filtering or modifying the resource response.
	•	Example: /test/123?query=456 → Refers to item_id = 123 but also includes query = 456 to provide extra context or apply filters.
- Optional/Required:
	•	By default, query parameters are optional. You can make them required by not providing a default value in the function signature (query: int makes it required here).

How They Work Together
- In this context, the path parameter (item_id) identifies the main resource being accessed.
- The query parameter (query) provides additional context or customization for how the resource is processed or retrieved.
- Example: Suppose /test/{item_id} fetches information about a product.
	•	/test/123?query=5 might mean:
	•	Fetch the product with ID 123 (path parameter).
	•	Apply a filter or setting based on the query value of 5 (query parameter).

Why it's needed: When a client (e.g., a browser, a mobile app, or another server) sends a GET request to the endpoint /test/, the function below the decorator is executed.
"""
@app.get("/test/{item_id}")
async def test(item_id: str, query: int):
    # returns a JSON response containing the item_id path parameter value.
    return {"hello": item_id}

