import os
import openai

openai.api_key = os.environ.get('OPENAI_API_KEY')
model_engine = os.environ.get('MODEL_ENGINE')


def openai_response(prompt,
                    model=model_engine,
                    temperature=0,
                    max_tokens=60,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    ).choices[0].text

    return response
