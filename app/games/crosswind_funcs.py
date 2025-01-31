from flask import render_template, session
import random
import math


def calculate_crosswind(wind_direction, runway_direction, wind_speed):
    """Calculate the crosswind component of the wind.

    This function calculates the crosswind component given the wind direction,
    runway direction, and wind speed.

    Args:
        wind_direction (int): The direction the wind is coming from in degrees.
        runway_direction (int): The direction of the runway in degrees.
        wind_speed (int): The speed of the wind in knots.

    Returns:
        float: The crosswind component in knots, rounded to one decimal place.
    """
    angle_diff = (wind_direction - runway_direction + 360) % 360
    crosswind = abs(wind_speed * math.sin(math.radians(angle_diff)))
    return round(crosswind, 1)


def determine_crosswind_direction(wind_direction, runway_direction):
    """Calculate the crosswind component of the wind.

    This function calculates the crosswind component given the wind direction,
    runway direction, and wind speed.

    Args:
        wind_direction (int): The direction the wind is coming from in degrees.
        runway_direction (int): The direction of the runway in degrees.
        wind_speed (int): The speed of the wind in knots.

    Returns:
        float: The crosswind component in knots, rounded to one decimal place.
    """
    angle_diff = (wind_direction - runway_direction + 360) % 360  # Normalize to 0–360
    return "Right" if 0 < angle_diff < 180 else "Left"


def generate_scenario():
    """Generate a random wind direction, wind speed, and runway direction.

    The wind direction is rounded to the nearest 10 degrees, the wind speed is
    in knots, and the runway direction is also rounded to the nearest 10 degrees.
    The runway direction is guaranteed to not be the same as the wind direction
    or 180 degrees opposite.

    Returns:
        tuple: A tuple containing the wind direction, wind speed, and runway direction.
    """
    wind_direction = random.randint(0, 35) * 10  # Rounded to nearest 10°
    wind_speed = random.randint(0, 30)  # Knots

    while True:
        runway_direction = random.randint(0, 35) * 10
        # Ensure runway_direction is not the same as wind_direction or 180° opposite
        if runway_direction not in {wind_direction, (wind_direction + 180) % 360}:
            break  # Valid runway_direction found

    return render_template(
            "crosswind_game.html",
            wind_direction=wind_direction,
            wind_speed=wind_speed,
            runway_direction=runway_direction,
            score=session['score'],
            result=None,
            feedback=None,
            user_choice=None,
            correct_choice=None,
            user_crosswind=None,
            allow_next=False,
        )