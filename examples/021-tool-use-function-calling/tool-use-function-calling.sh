# First, install the Google Generative AI library and requests
$ pip install google-genai requests

# Then run the program with Python
$ python function_calling_weather_calendar.py
--- Example 1: Basic Function Calling ---
Function to call: get_current_temperature
Arguments: {'location': 'London'}
Function result: {'location': 'London', 'temperature': 16, 'unit': 'Celsius'}
Model's final response: OK. The current temperature in London is 16 degrees Celsius.
--- Example 2: Parallel Function Calling (Weather and Appointments) ---
get_current_temperature(location=Paris)
Result: {'location': 'Paris', 'temperature': 18, 'unit': 'Celsius'}
check_appointment_availability(time=14:00, date=2024-07-04)
Result: {'available': False, 'message': 'The slot on 2024-07-04 at 14:00 is already booked.'}
Sending all function results back to the model...
Model's final response:
The current temperature in Paris is 18 degrees Celsius. The appointment slot on July 4th at 2 PM is not available.
