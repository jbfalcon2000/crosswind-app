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
    
    if request.method == "GET" or "next" in request.form:
        # Generate a new scenario
        generate_scenario()
    
    if "restart" in request.form:
        # Reset the score
        session['score']["correct"] = 0
        session['score']["attempts"] = 0
        # Generate a new scenario
        generate_scenario()

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
            
        if not feedback:
            result = "Correct"
            session['score']['correct'] += 1
        session['score']['attempts'] += 1

        # Update score if everything is correct
        if not feedback:
            result = "Correct"
            session['score']["correct"] += 1
        session['score']["attempts"] += 1

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