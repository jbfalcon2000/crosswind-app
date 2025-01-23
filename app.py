from flask import Flask, render_template, request
import random
import math

app = Flask(__name__)

# Keep track of score
score = {"correct": 0, "attempts": 0}


# Function to calculate crosswind
def calculate_crosswind(wind_direction, runway_direction, wind_speed):
    angle_diff = abs(wind_direction - runway_direction)
    if angle_diff > 180:
        angle_diff = 360 - angle_diff
    crosswind = abs(wind_speed * math.sin(math.radians(angle_diff)))
    return round(crosswind, 1)


def determine_crosswind_direction(wind_direction, runway_direction):
    """
    Determine if the crosswind is from the Left or Right.
    """
    angle_diff = (wind_direction - runway_direction + 360) % 360  # Normalize to 0–360
    if 0 < angle_diff < 180:
        return "Right"
    else:
        return "Left"


@app.route("/", methods=["GET", "POST"])
def index():
    global score

    if request.method == "GET":
        # Generate a new scenario
        wind_direction = random.randint(0, 35) * 10  # Rounded to nearest 10°
        wind_speed = random.randint(0, 30)  # Knots
        runway_direction = random.randint(0, 35) * 10
        return render_template(
            "index.html",
            wind_direction=wind_direction,
            wind_speed=wind_speed,
            runway_direction=runway_direction,
            score=score,
            result=None,
            feedback=None,
            user_choice=None,
            correct_choice=None,
            user_crosswind=None,
            allow_next=False,
        )

    if "next" in request.form:
        # Generate a new scenario
        wind_direction = random.randint(0, 35) * 10
        wind_speed = random.randint(0, 30)
        runway_direction = random.randint(0, 35) * 10
        return render_template(
            "index.html",
            wind_direction=wind_direction,
            wind_speed=wind_speed,
            runway_direction=runway_direction,
            score=score,
            result=None,
            feedback=None,
            user_choice=None,
            correct_choice=None,
            user_crosswind=None,
            allow_next=False,
        )

    if request.method == "POST":
        # Handle form submission
        wind_direction = int(request.form.get("wind_direction"))
        wind_speed = int(request.form.get("wind_speed"))
        runway_direction = int(request.form.get("runway_direction"))
        user_choice = request.form.get("choice")
        user_crosswind = request.form.get("crosswind", type=float)

        # Calculate correct crosswind and direction
        correct_crosswind = calculate_crosswind(wind_direction, runway_direction, wind_speed)
        correct_choice = determine_crosswind_direction(wind_direction, runway_direction)

        # Determine feedback
        result = "Incorrect"
        feedback = []
        if user_choice != correct_choice:
            feedback.append(f"Incorrect wind direction. The correct choice was {correct_choice}.")
        if user_crosswind is None or abs(user_crosswind - correct_crosswind) > 2:
            feedback.append(
                f"Incorrect crosswind component. The correct value was {correct_crosswind} knots."
            )

        # Update score if everything is correct
        if not feedback:
            result = "Correct"
            score["correct"] += 1
        score["attempts"] += 1

        # Render feedback
        return render_template(
            "index.html",
            wind_direction=wind_direction,
            wind_speed=wind_speed,
            runway_direction=runway_direction,
            score=score,
            result=result,
            feedback=" ".join(feedback) if feedback else "You got everything correct!",
            user_choice=user_choice,
            correct_choice=correct_choice,
            user_crosswind=user_crosswind,
            allow_next=True,
        )


if __name__ == "__main__":
    app.run(debug=True)
