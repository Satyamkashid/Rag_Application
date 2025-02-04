# controllers/llumo_controller.py

from flask import jsonify, request
import logging
from services.llumo_service import evaluate_with_llumo
from services.model_service import get_model_response

def llumo_eval():
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        file_path = data.get("filePath")

        if not prompt or not file_path:
            return jsonify({"error": "Prompt and file path are required"}), 400

        # Use the centralized function
        context, output, error = get_model_response(file_path, prompt)
        
        if error:
            return jsonify({"error": f"Failed to get model response: {error}"}), 500

        # Evaluate using LLUMO
        evaluation, success = evaluate_with_llumo(prompt, context, output)
        if not success:
            return jsonify({"error": "Failed to evaluate with LLUMO"}), 500

        return jsonify({
            "evaluation": evaluation,
        }), 200

    except Exception as e:
        logging.error(f"Error in LLUMO evaluation: {e}")
        return jsonify({"error": str(e)}), 500