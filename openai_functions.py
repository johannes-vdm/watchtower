import os
import openai

openai.api_key = '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'
model_engine = "text-davinci-003"


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
