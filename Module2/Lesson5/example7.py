import json

# GOOD: Safely processing JSON from a request body
@app.post("/process_json/")
async def process_json(data: dict): # FastAPI/Pydantic handle JSON parsing safely
    # data is already a Python dict, parsed safely from JSON
    print(f"Received safe JSON data: {data}")
    return {"status": "processed", "data": data}

# BAD: This is purely for demonstration of what NOT to do with pickle.
# DO NOT USE THIS IN PRODUCTION WITH UNTRUSTED INPUT.
import pickle
import base64

class DangerousObject:
    def __reduce__(self):
        # This is a hypothetical dangerous action upon deserialization
        # In a real attack, this could be os.system('rm -rf /')
        return (print, ("Executing dangerous code on deserialization!",))

@app.post("/process_pickle_unsafe/")
async def process_pickle_unsafe(encoded_data: str):
    # This endpoint is HIGHLY INSECURE and for demonstration ONLY
    try:
        # Decode the base64 string
        decoded_data = base64.b64decode(encoded_data)
        # Attempt to deserialize the pickle data
        deserialized_object = pickle.loads(decoded_data)
        return {"status": "deserialized (DANGEROUS)", "data_type": str(type(deserialized_object))}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Deserialization failed: {e}")

# To exploit the "/process_pickle_unsafe/" endpoint:
# d = DangerousObject()
# pickled_data = pickle.dumps(d)
# base64_encoded = base64.b64encode(pickled_data).decode('utf-8')
# Then send a POST request with this base64_encoded string to the endpoint.