import pytest
import requests
import jsonschema
from tests.schemas import (CREATE_COMMAND_RESPONSE_SCHEMA, COMMAND_STATUS_RESPONSE_SCHEMA)

# Позитивный сценарий: создание команды
def test_positive_create_command(api_client):
    response = api_client.create_command("sensor-1","RESTART")

    assert response['status'] == 'NEW'
    jsonschema.validate(response, CREATE_COMMAND_RESPONSE_SCHEMA)
    
    final_status = api_client.wait_polling(response['id'], timeout=30)
    assert final_status['status'] == 'SUCCESS'
    assert final_status['result'] == 'OK'
    jsonschema.validate(final_status, COMMAND_STATUS_RESPONSE_SCHEMA)

@pytest.mark.parametrize("invalid_device_id, test_description", [
    ("", "empty string"),
    (None, "None value"),
    ("   ", "whitespace only"),
])

# Негативный сценарий
def test_negative(api_client, invalid_device_id, test_description):
    print(f"\nTest: {test_description} (device_id={repr(invalid_device_id)})")
    
    try:
        api_client.create_command(device_id=invalid_device_id, command="RESTART")
        pytest.fail(f"Waiting error 400 for device_id: {invalid_device_id}")

    except requests.HTTPError as err:
        assert err.response.status_code == 400, \
        f"Waiting status 400, got {err.response.status_code}"
        
        error_data = err.response.json()
        print(f"Got waiting error: {error_data}")
    
# Ассинхронность, polling, таймаут
def test_async_command_polling(api_client):
   command_response = api_client.create_command(
       device_id="sensor-1",
       command="RESTART"
   )
   
   command_id = command_response['id']
   print(f"Created command: {command_id}")
 
   final_status = api_client.wait_polling(
        command_id=command_id,
        timeout=30
    )
   
   assert final_status['status'] == 'SUCCESS'
   assert final_status['result'] == 'OK'
    
   print(f"Command {command_id} completed successfully for {30} seconds")