from flask import render_template, request, session, redirect, url_for, flash
from app import app
from app.games.crosswind_funcs import calculate_crosswind, determine_crosswind_direction, generate_scenario

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/crosswind_game", methods=["GET", "POST"])
def crosswind_game():
    if 'score' not in session:
        session['score'] = {"correct": 0, "attempts": 0}


    def render_new_scenario():
        wind_direction, wind_speed, runway_direction = generate_scenario()
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
        
    
    if request.method == "GET" or "next" in request.form or "restart" in request.form:
        if "restart" in request.form:
            # Reset the score
            session['score'] = {"correct": 0, "attempts": 0}
        return render_new_scenario()
    
    if request.method == "POST":
        # Handle form submission
        wind_direction = int(request.form.get("wind_direction"))
        wind_speed = int(request.form.get("wind_speed"))
        runway_direction = int(request.form.get("runway_direction"))
        user_choice = request.form.get("choice")
        
        try:
            user_crosswind = float(request.form.get("crosswind"))
        except (ValueError, TypeError):
            flash("Please enter a valid number for the crosswind component.")
            return redirect(url_for("index"))

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
            session['score']["correct"] += 1
        session['score']['attempts'] += 1
        session.modified = True

        # Render feedback
        return render_template(
            "crosswind_game.html",
            wind_direction=wind_direction,
            wind_speed=wind_speed,
            runway_direction=runway_direction,
            score=session['score'],
            result=result,
            feedback="\n".join(feedback) if feedback else f"You got everything correct! Correct crosswind was {correct_crosswind}",
            user_choice=user_choice,
            correct_choice=correct_choice,
            user_crosswind=user_crosswind,
            allow_next=True,
        )


@app.route("/dega_game", methods=["GET", "POST"])
def dega_game():
    return render_template("dega_game.html")