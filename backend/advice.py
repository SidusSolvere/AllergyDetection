from litellm import completion
from pydantic import BaseModel

class AllergyAdvice(BaseModel):
    explanation: str
    care_tips: list[str]
    see_doctor: bool

def generate_advice(result: str, percentage: float) -> AllergyAdvice:
    r = completion(
        model="gemini/gemini-3.6-flash",
        messages=[{
            "role": "user",
            "content": f"A skin image was classified as: '{result}' ({percentage}% confidence). "
                       f"Give a short, non-diagnostic explanation and 2-3 practical care tips. "
                       f"Never state a definite diagnosis. Return JSON: "
                       f"explanation, care_tips (list of strings), see_doctor (bool)."
        }],
        response_format={"type": "json_object"},
    )
    return AllergyAdvice.model_validate_json(r.choices[0].message.content)